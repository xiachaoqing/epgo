#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语陪跑GO - 内容爬虫 + 自动入库
抓取KET/PET英语备考相关内容，写入 ep_news 表

用法：
  python3 crawler.py          # 正式抓取入库
  python3 crawler.py --dry    # 只抓取不入库（预览）

定时任务（服务器 crontab -e）：
  0 7 * * * cd /www/wwwroot/go.xiachaoqing.com/scripts && python3 crawler.py >> /tmp/epgo_crawler.log 2>&1
"""

from __future__ import print_function
import sys
import re
import time
import random
import hashlib
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import pymysql

# ========== 配置 ==========
DB = dict(
    host='localhost',
    user='xiachaoqing',
    password='07090218',
    db='epgo_db',
    charset='utf8mb4',
    port=3306
)

# 栏目ID（已确认）
COLUMN_MAP = {
    'ket':       128,  # KET备考
    'ket_real':  140,  # KET真题解析
    'ket_word':  141,  # KET词汇速记
    'ket_write': 142,  # KET写作指导
    'pet':       127,  # PET备考
    'english':   126,  # 英语学习
}
DEFAULT_COLUMN = 128

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# 抓取来源配置
SOURCES = [
    # 沪江英语 - KET分类
    {
        'name': '沪江英语KET',
        'list_url': 'https://www.hjenglish.com/new/p1523/',
        'list_item': 'div.article-list li, ul.news-list li, .list-article li',
        'title_sel': 'a',
        'base': 'https://www.hjenglish.com',
        'content_sel': ['div.article-content', '.content-detail', '#article-content'],
        'keywords': ['KET', 'PET', '备考', '词汇', '写作', '真题', '剑桥'],
        'col_hint': 'ket',
    },
    # 可可英语 - 英语学习文章
    {
        'name': '可可英语资讯',
        'list_url': 'http://www.kekenet.com/Article/',
        'list_item': '.article-list .item, ul.list li',
        'title_sel': 'a',
        'base': 'http://www.kekenet.com',
        'content_sel': ['.article-body', '.content', '#article'],
        'keywords': ['KET', 'PET', '词汇', '语法', '写作', '听力', '口语', '考试'],
        'col_hint': 'english',
    },
    # 21世纪英文报 RSS（稳定）
    {
        'name': '21世纪英文报',
        'list_url': 'https://www.i21st.cn/rss.xml',
        'is_rss': True,
        'keywords': ['考试', '词汇', '英语', 'English', 'exam', 'vocabulary'],
        'col_hint': 'english',
    },
]

DRY_RUN = '--dry' in sys.argv


# ========== 工具函数 ==========

def clean_text(text):
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def make_desc(content_html, length=150):
    """从HTML提取纯文本摘要"""
    text = BeautifulSoup(content_html, 'html.parser').get_text(separator=' ')
    text = clean_text(text)
    if len(text) > length:
        return text[:length] + '...'
    return text


def guess_column(title, content=''):
    """根据标题内容判断栏目"""
    t = title + content
    if '真题' in t and 'KET' in t:
        return COLUMN_MAP['ket_real']
    if ('词汇' in t or '单词' in t) and 'KET' in t:
        return COLUMN_MAP['ket_word']
    if '写作' in t and 'KET' in t:
        return COLUMN_MAP['ket_write']
    if 'KET' in t:
        return COLUMN_MAP['ket']
    if 'PET' in t or 'B1' in t:
        return COLUMN_MAP['pet']
    return COLUMN_MAP['english']


def already_exists(conn, title):
    cur = conn.cursor()
    cur.execute("SELECT id FROM ep_news WHERE title=%s LIMIT 1", (title,))
    return cur.fetchone() is not None


def insert_article(conn, title, content, desc, col_id, source_url=''):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = """INSERT INTO ep_news
        (title, content, description, bigclass, inputtime, updatetime,
         lang, isshow, issys, hits, nofollow, out_url)
        VALUES (%s,%s,%s,%s,%s,%s,'cn',1,0,0,0,%s)"""
    cur = conn.cursor()
    cur.execute(sql, (title, content, desc, col_id, now, now, source_url))
    conn.commit()
    return cur.lastrowid


def fetch_page(url, timeout=12):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.encoding = r.apparent_encoding or 'utf-8'
        return r.text
    except Exception as e:
        print('  请求失败: {}'.format(e))
        return None


def extract_content(url, selectors):
    """抓取文章正文HTML"""
    html = fetch_page(url)
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    # 去除干扰
    for tag in soup.select('script,style,nav,header,footer,.ad,.sidebar,.comment,.relate'):
        tag.decompose()
    for sel in selectors:
        el = soup.select_one(sel)
        if el and len(el.get_text(strip=True)) > 100:
            # 清理内联JS
            content = re.sub(r'<script[^>]*>.*?</script>', '', str(el), flags=re.S)
            content = re.sub(r'<iframe[^>]*>.*?</iframe>', '', content, flags=re.S)
            return content
    return None


# ========== RSS 解析 ==========

def crawl_rss(source, conn):
    count = 0
    html = fetch_page(source['list_url'])
    if not html:
        return 0
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('item')
    print('  RSS条目: {}'.format(len(items)))
    for item in items[:8]:
        title_el = item.find('title')
        link_el = item.find('link')
        desc_el = item.find('description')
        if not title_el or not link_el:
            continue
        title = clean_text(title_el.get_text())
        link = clean_text(link_el.get_text())
        desc_text = clean_text(desc_el.get_text()) if desc_el else ''

        # 关键词过滤
        if not any(kw in title + desc_text for kw in source['keywords']):
            continue

        print('  [{}]'.format(title[:30]))
        if not DRY_RUN and conn and already_exists(conn, title):
            print('    -> 已存在')
            continue

        # 尝试抓正文，失败用RSS描述代替
        content = '<p>{}</p>'.format(desc_text) if desc_text else '<p>{}</p>'.format(title)
        col_id = guess_column(title, desc_text)

        if DRY_RUN:
            print('    [DRY] 栏目:{} 描述:{}'.format(col_id, desc_text[:40]))
        else:
            nid = insert_article(conn, title, content, desc_text[:150], col_id, link)
            print('    -> 入库 ID={}'.format(nid))
            count += 1
        time.sleep(random.uniform(1, 2))
    return count


# ========== 普通列表页爬取 ==========

def crawl_list(source, conn):
    count = 0
    html = fetch_page(source['list_url'])
    if not html:
        return 0
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select(source['list_item'])
    print('  找到列表: {} 条'.format(len(items)))

    for item in items[:10]:
        a = item.select_one(source['title_sel'])
        if not a:
            a = item.find('a')
        if not a:
            continue
        title = clean_text(a.get_text())
        if not title or len(title) < 4:
            continue

        # 关键词过滤
        if not any(kw in title for kw in source['keywords']):
            continue

        href = a.get('href', '')
        if not href:
            continue
        if not href.startswith('http'):
            href = source['base'] + href

        print('  [{}]'.format(title[:30]))
        if not DRY_RUN and conn and already_exists(conn, title):
            print('    -> 已存在')
            continue

        content = extract_content(href, source['content_sel'])
        if not content:
            print('    -> 正文为空，跳过')
            continue

        desc = make_desc(content)
        col_id = guess_column(title, desc)

        if DRY_RUN:
            print('    [DRY] 栏目:{} 描述:{}'.format(col_id, desc[:40]))
        else:
            nid = insert_article(conn, title, content, desc, col_id, href)
            print('    -> 入库 ID={}'.format(nid))
            count += 1

        time.sleep(random.uniform(2, 4))

    return count


# ========== 主流程 ==========

def main():
    print('[{}] 英语陪跑GO 内容爬虫启动'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    if DRY_RUN:
        print('** DRY RUN - 不写入数据库 **')

    conn = None
    if not DRY_RUN:
        try:
            conn = pymysql.connect(**DB)
            print('数据库连接成功')
        except Exception as e:
            print('数据库连接失败: {}'.format(e))
            sys.exit(1)

    total = 0
    for src in SOURCES:
        print('\n[{}] 抓取中...'.format(src['name']))
        if src.get('is_rss'):
            total += crawl_rss(src, conn)
        else:
            total += crawl_list(src, conn)

    if conn:
        conn.close()
    print('\n完成！共入库 {} 篇'.format(total))


if __name__ == '__main__':
    main()
