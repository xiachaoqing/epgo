#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语陪跑GO - 内容爬虫 v2 (改进版)
抓取KET/PET英语备考相关内容，写入 ep_news 表

用法：
  python3 crawler_v2.py              # 正式抓取入库
  python3 crawler_v2.py --dry        # 只抓取不入库（预览）
  python3 crawler_v2.py --ket        # 仅爬取KET相关
  python3 crawler_v2.py --pet        # 仅爬取PET相关

定时任务（服务器 crontab -e）：
  0 6 * * * cd /www/wwwroot/go.xiachaoqing.com/scripts && python3 crawler_v2.py >> /tmp/epgo_crawler.log 2>&1
"""

from __future__ import print_function
import sys
import re
import time
import random
import hashlib
import json
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
import pymysql
try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

# ========== 配置 ==========
DB = dict(
    host='localhost',
    user='xiachaoqing',
    password='07090218',
    db='epgo_db',
    charset='utf8mb4',
    port=3306
)

# 栏目ID映射
COLUMN_MAP = {
    'ket':       128,  # KET备考 - 总栏目
    'ket_exam':  111,  # KET真题解析
    'ket_word':  112,  # KET词汇速记
    'ket_write': 113,  # KET写作指导
    'ket_listen': 114, # KET听力技巧
    'pet':       115,  # PET备考 - 总栏目
    'pet_exam':  116,  # PET真题解析
    'reading':   103,  # 英语阅读
}
DEFAULT_COLUMN = 103

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
}

DRY_RUN = '--dry' in sys.argv
FILTER_TYPE = None
if '--ket' in sys.argv:
    FILTER_TYPE = 'ket'
elif '--pet' in sys.argv:
    FILTER_TYPE = 'pet'

# 高质量内容源配置
SOURCES = [
    # ============ KET备考源 ============
    {
        'name': '沪江英语KET真题',
        'list_url': 'https://www.hjenglish.com/tag/ket/',
        'list_item': 'div.article-item, li.item, div.news-item',
        'title_sel': 'h2 a, h3 a, a.title',
        'base': 'https://www.hjenglish.com',
        'content_sel': [
            'div.article-content',
            'div.read-box',
            'div.article__content',
            'div#ctl00_ContentPlaceHolder1_divContent',
            'article',
            'div.content-detail'
        ],
        'keywords': ['KET', '真题', '解析', '考试', '备考'],
        'column_hint': 'ket_exam',
        'type': 'ket',
        'enabled': True,
    },
    {
        'name': 'BBC Learning English',
        'list_url': 'https://www.bbc.co.uk/learningenglish/features',
        'list_item': 'li.list-item, div.lj-secondary__item, article',
        'title_sel': 'a.lj-link-heading',
        'base': 'https://www.bbc.co.uk',
        'content_sel': [
            'div.share-content',
            'article.article__main',
            'div.article-content-full',
            'div.bodyText'
        ],
        'keywords': ['vocabulary', 'grammar', 'pronunciation', 'English', 'lesson'],
        'column_hint': 'ket',
        'type': 'ket',
        'enabled': True,
    },
    {
        'name': '雅思哥KET词汇',
        'list_url': 'https://www.ieltsgo.com/tag/ket',
        'list_item': 'div.post-item, article, div.post',
        'title_sel': 'h2 a, h3 a, a.post-title',
        'base': 'https://www.ieltsgo.com',
        'content_sel': [
            'div.post-content',
            'div.entry-content',
            'article .content',
            'div.main-content'
        ],
        'keywords': ['KET', '词汇', '单词', '学习', '英语'],
        'column_hint': 'ket_word',
        'type': 'ket',
        'enabled': True,
    },
    {
        'name': '英语学习网KET写作',
        'list_url': 'https://www.yingyu.com/ket/',
        'list_item': 'li.list-li, div.article-li, tr[class*="list"]',
        'title_sel': 'a',
        'base': 'https://www.yingyu.com',
        'content_sel': [
            'div.news-cont',
            'div.article-content',
            'div.content',
            'div#main'
        ],
        'keywords': ['KET', '写作', '短语', '句型', '写'],
        'column_hint': 'ket_write',
        'type': 'ket',
        'enabled': True,
    },

    # ============ PET备考源 ============
    {
        'name': '沪江英语PET',
        'list_url': 'https://www.hjenglish.com/tag/pet/',
        'list_item': 'div.article-item, li.item',
        'title_sel': 'h2 a, h3 a',
        'base': 'https://www.hjenglish.com',
        'content_sel': [
            'div.article-content',
            'div.article__content',
            'article',
        ],
        'keywords': ['PET', '真题', '备考', '考试'],
        'column_hint': 'pet_exam',
        'type': 'pet',
        'enabled': True,
    },

    # ============ 通用英语学习源 ============
    {
        'name': '可可英语精选',
        'list_url': 'http://www.kekenet.com/wangye/n50/',
        'list_item': 'li[class*="list"], div.article-item, tr[class*="item"]',
        'title_sel': 'a',
        'base': 'http://www.kekenet.com',
        'content_sel': [
            'div.article-body',
            'div.content-text',
            'div.newscont',
            'div#articlenr'
        ],
        'keywords': ['英语', '学习', '词汇', '语法', '听力', '口语'],
        'column_hint': 'reading',
        'type': None,
        'enabled': True,
    },
    {
        'name': '爱思英语资讯',
        'list_url': 'https://www.24en.com/news/',
        'list_item': 'li.news-item, div.article, article',
        'title_sel': 'a',
        'base': 'https://www.24en.com',
        'content_sel': [
            'div.article-content',
            'div.newscontent',
            'article.article-content',
            'div.main-container'
        ],
        'keywords': ['英语', '学习', '阅读', '考试'],
        'column_hint': 'reading',
        'type': None,
        'enabled': True,
    },

    # ============ RSS源（稳定） ============
    # {
    #     'name': '21世纪英文报 RSS',
    #     'list_url': 'https://www.i21st.cn/rss.xml',
    #     'is_rss': True,
    #     'keywords': ['考试', '词汇', '英语', '阅读', 'exam', 'vocabulary'],
    #     'column_hint': 'reading',
    #     'type': None,
    #     'enabled': False,  # 暂时禁用
    # },
]


# ========== 工具函数 ==========

def clean_text(text):
    """清理文本空白"""
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_html(html_str):
    """清理HTML中的脚本、样式、广告等"""
    if not html_str:
        return ''

    soup = BeautifulSoup(html_str, 'html.parser')

    # 移除干扰元素
    for tag in soup.select(
        'script, style, noscript, nav, header, footer, '
        '.ad, .advertisement, .sidebar, .widget, '
        '.comment, .comment-list, .relate, .tags, '
        '.share, .social, .breadcrumb, .pagination'
    ):
        tag.decompose()

    # 移除iframe
    for iframe in soup.find_all('iframe'):
        iframe.decompose()

    return str(soup)


def make_desc(content_html, length=200):
    """从HTML提取纯文本摘要"""
    if not content_html:
        return ''

    try:
        soup = BeautifulSoup(content_html, 'html.parser')
        # 获取所有文本，用空格连接
        text = soup.get_text(separator=' ', strip=True)
        text = clean_text(text)

        # 移除重复空白并截断
        if len(text) > length:
            # 在标点符号处截断以保持完整句子
            truncated = text[:length]
            last_period = max(
                truncated.rfind('。'),
                truncated.rfind('！'),
                truncated.rfind('？'),
                truncated.rfind('.'),
                truncated.rfind('!'),
                truncated.rfind('?'),
                truncated.rfind(' ')
            )
            if last_period > length * 0.7:  # 至少保留70%
                truncated = text[:last_period]
            return truncated + '...'
        return text
    except:
        return ''


def guess_column(title, content=''):
    """根据标题和内容判断栏目"""
    t = (title + content).upper()

    # KET相关
    if 'KET' in t:
        if '真题' in t or 'EXAM' in t or 'TEST' in t:
            return COLUMN_MAP['ket_exam']
        elif '词汇' in t or 'VOCABULARY' in t or 'WORD' in t:
            return COLUMN_MAP['ket_word']
        elif '写作' in t or 'WRITING' in t or 'WRITE' in t:
            return COLUMN_MAP['ket_write']
        elif '听力' in t or 'LISTENING' in t or 'LISTEN' in t:
            return COLUMN_MAP['ket_listen']
        else:
            return COLUMN_MAP['ket']

    # PET相关
    if 'PET' in t or 'B1' in t:
        if '真题' in t or 'EXAM' in t:
            return COLUMN_MAP['pet_exam']
        return COLUMN_MAP['pet']

    # 通用阅读
    return COLUMN_MAP['reading']


def already_exists(conn, title):
    """检查文章是否已存在"""
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM ep_news WHERE title=%s LIMIT 1", (title,))
        result = cur.fetchone()
        return result is not None
    except:
        return False


def insert_article(conn, title, content, desc, col_id, source_url='', image_url=''):
    """插入文章到数据库"""
    if not conn:
        return None

    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO ep_news
            (title, content, description, bigclass, inputtime, updatetime,
             lang, isshow, issys, hits, nofollow, out_url, imgurl)
            VALUES (%s,%s,%s,%s,%s,%s,'cn',1,0,0,0,%s,%s)"""
        cur = conn.cursor()
        cur.execute(sql, (title, content, desc, col_id, now, now, source_url, image_url))
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        print('  入库错误: {}'.format(e))
        return None


def fetch_page(url, timeout=15):
    """获取网页内容"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout, verify=False)
        response.encoding = response.apparent_encoding or 'utf-8'
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print('  请求失败: {}'.format(str(e)[:50]))
    return None


def extract_images(soup):
    """从内容中提取第一张图片URL"""
    if not soup:
        return ''

    try:
        img = soup.find('img')
        if img and img.get('src'):
            return img.get('src')
    except:
        pass
    return ''


def extract_content(url, selectors):
    """抓取文章正文HTML"""
    html = fetch_page(url)
    if not html or len(html) < 500:
        return None, ''

    soup = BeautifulSoup(html, 'html.parser')
    cleaned = clean_html(str(soup))
    soup = BeautifulSoup(cleaned, 'html.parser')

    # 尝试用选择器获取内容
    content = None
    for selector in selectors:
        try:
            el = soup.select_one(selector)
            if el:
                text_len = len(el.get_text(strip=True))
                if text_len > 300:  # 至少300字符
                    content = str(el)
                    break
        except:
            continue

    # 如果没找到，用body的主要内容
    if not content:
        body = soup.find('body')
        if body:
            # 移除边栏、菜单等
            for tag in body.select('.sidebar, nav, .menu, aside'):
                tag.decompose()
            content = str(body)

    # 提取图片
    image_url = extract_images(soup)

    return content, image_url


# ========== RSS 解析 ==========

def crawl_rss(source, conn):
    """爬取RSS源"""
    count = 0

    try:
        feed = feedparser.parse(source['list_url'])
        entries = feed.entries[:12]
        print('  RSS条目: {}'.format(len(entries)))

        for entry in entries:
            title = clean_text(entry.get('title', ''))
            link = entry.get('link', '')
            summary = clean_text(entry.get('summary', ''))

            if not title or not link:
                continue

            # 关键词过滤
            if not any(kw in (title + summary).lower() for kw in source['keywords']):
                continue

            print('  [{}]'.format(title[:35]))

            if not DRY_RUN and already_exists(conn, title):
                print('    -> 已存在')
                continue

            # 尝试提取详细内容
            content, image = extract_content(link, [
                'div.article-content', 'div.entry-content',
                'article', 'div.content'
            ])

            if not content:
                # 用RSS摘要替代
                content = '<p>{}</p>'.format(summary) if summary else '<p>{}</p>'.format(title)

            desc = make_desc(content, 250)
            col_id = guess_column(title, desc)

            if DRY_RUN:
                print('    [DRY] 栏目:{} 字数:{}'.format(col_id, len(desc)))
            else:
                nid = insert_article(conn, title, content, desc[:255], col_id, link, image)
                if nid:
                    print('    -> ID={}'.format(nid))
                    count += 1

            time.sleep(random.uniform(1, 3))

    except Exception as e:
        print('  RSS解析错误: {}'.format(e))

    return count


# ========== 列表页爬取 ==========

def crawl_list(source, conn):
    """爬取列表页"""
    count = 0

    html = fetch_page(source['list_url'])
    if not html:
        return 0

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select(source['list_item'])
    print('  找到列表项: {} 条'.format(len(items)))

    for item in items[:15]:  # 最多爬15篇
        try:
            a = item.select_one(source['title_sel'])
            if not a:
                a = item.find('a')
            if not a:
                continue

            title = clean_text(a.get_text())
            if not title or len(title) < 6:
                continue

            # 关键词过滤
            if not any(kw in title for kw in source['keywords']):
                continue

            href = a.get('href', '')
            if not href or href.startswith('#'):
                continue

            # 补全URL
            if not href.startswith('http'):
                if href.startswith('/'):
                    # 解析base URL
                    import urllib.parse
                    base_url = source.get('base', '')
                    if base_url:
                        href = urllib.parse.urljoin(base_url, href)
                    else:
                        continue
                else:
                    href = source.get('base', '') + '/' + href

            print('  [{}]'.format(title[:35]))

            if not DRY_RUN and already_exists(conn, title):
                print('    -> 已存在')
                continue

            # 延迟以避免被禁
            time.sleep(random.uniform(1, 3))

            # 提取正文
            content, image = extract_content(href, source['content_sel'])
            if not content or len(BeautifulSoup(content, 'html.parser').get_text(strip=True)) < 300:
                print('    -> 正文太短，跳过')
                continue

            desc = make_desc(content)
            col_id = guess_column(title, desc)

            if DRY_RUN:
                print('    [DRY] 栏目:{} 字数:{}'.format(col_id, len(desc)))
            else:
                nid = insert_article(conn, title, content, desc[:255], col_id, href, image)
                if nid:
                    print('    -> ID={}'.format(nid))
                    count += 1

        except Exception as e:
            print('  处理错误: {}'.format(str(e)[:40]))
            continue

    return count


# ========== 主流程 ==========

def main():
    print('\n' + '='*60)
    print('[{}] 英语陪跑GO 内容爬虫 v2.0 启动'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('='*60)

    if DRY_RUN:
        print('⚠️  DRY RUN 模式 - 只预览不写入\n')
    if FILTER_TYPE:
        print('📌 类型过滤: {}\n'.format(FILTER_TYPE.upper()))

    # 初始化数据库连接
    conn = None
    if not DRY_RUN:
        try:
            conn = pymysql.connect(**DB)
            print('✓ 数据库连接成功\n')
        except Exception as e:
            print('✗ 数据库连接失败: {}\n'.format(e))
            sys.exit(1)

    total = 0

    # 爬取所有源
    for src in SOURCES:
        # 类型过滤
        if FILTER_TYPE and src.get('type') != FILTER_TYPE:
            continue

        if not src.get('enabled', True):
            print('[跳过] {}'.format(src['name']))
            continue

        print('\n[{}] 抓取中...'.format(src['name']))
        print('-' * 50)

        try:
            if src.get('is_rss'):
                count = crawl_rss(src, conn)
            else:
                count = crawl_list(src, conn)
            total += count
        except Exception as e:
            print('  错误: {}\n'.format(e))
            continue

    # 关闭连接
    if conn:
        conn.close()

    print('\n' + '='*60)
    print('✓ 爬虫任务完成！共入库 {} 篇文章'.format(total))
    print('='*60 + '\n')


if __name__ == '__main__':
    main()
