#!/usr/bin/env python3
"""
英语陪跑GO - 内容爬虫 + 自动入库
目标：抓取KET/PET英语备考相关内容，写入 ep_news 表

用法：
  python3 crawler.py          # 抓取并入库
  python3 crawler.py --dry    # 只抓取不入库（预览）

每天定时执行（服务器cron）：
  0 6 * * * cd /www/wwwroot/go.xiachaoqing.com/scripts && python3 crawler.py >> /tmp/crawler.log 2>&1
"""

import requests
from bs4 import BeautifulSoup
import pymysql
import hashlib
import time
import random
import sys
import re
from datetime import datetime

# ========== 配置 ==========
DB = dict(host='localhost', user='xiachaoqing', password='07090218',
          db='epgo_db', charset='utf8mb4', port=3306)

# 栏目ID映射（对应MetInfo后台实际栏目ID，确认后填写）
# 格式：关键词 -> ep_column.id
COLUMN_MAP = {
    'ket': 128,   # KET备考栏目ID（需确认）
    'pet': 140,   # PET备考栏目ID（需确认）
    'english': 141,  # 英语学习栏目ID（需确认）
}
DEFAULT_COLUMN = 128  # 默认栏目

# 抓取来源（教育类公开内容站点）
SOURCES = [
    {
        'name': '朗阁教育资讯',
        'url': 'https://www.longre.com/news/',
        'list_selector': '.news-list .item',
        'title_selector': 'h3, h2, .title',
        'link_selector': 'a',
        'base_url': 'https://www.longre.com',
        'keywords': ['KET', 'PET', '剑桥', '备考', '词汇', '写作', '听力'],
    },
    {
        'name': '新东方英语资讯',
        'url': 'https://www.xdf.cn/ket/',
        'list_selector': '.article-list .item, .news-item',
        'title_selector': 'h3, h2, .title',
        'link_selector': 'a',
        'base_url': 'https://www.xdf.cn',
        'keywords': ['KET', 'PET', '备考', '真题', '技巧'],
    },
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

DRY_RUN = '--dry' in sys.argv


# ========== 工具函数 ==========

def clean_text(text):
    """清理文本，去除多余空白"""
    if not text:
        return ''
    return re.sub(r'\s+', ' ', text).strip()


def make_description(content, length=150):
    """从正文提取摘要"""
    text = BeautifulSoup(content, 'html.parser').get_text()
    text = clean_text(text)
    return text[:length] + ('...' if len(text) > length else '')


def guess_column(title, content=''):
    """根据标题关键词猜测栏目ID"""
    text = (title + content).upper()
    if 'KET' in text:
        return COLUMN_MAP['ket']
    if 'PET' in text or 'B1' in text:
        return COLUMN_MAP['pet']
    return COLUMN_MAP['english']


def content_hash(title):
    """用标题生成去重hash"""
    return hashlib.md5(title.encode('utf-8')).hexdigest()[:16]


def already_exists(conn, title):
    """检查标题是否已入库"""
    cur = conn.cursor()
    cur.execute("SELECT id FROM ep_news WHERE title=%s LIMIT 1", (title,))
    return cur.fetchone() is not None


def insert_article(conn, title, content, description, column_id, source_url=''):
    """插入文章到ep_news表"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = """
        INSERT INTO ep_news
        (title, content, description, bigclass, inputtime, updatetime,
         lang, isshow, issys, hits, nofollow, out_url)
        VALUES (%s, %s, %s, %s, %s, %s, 'cn', 1, 0, 0, 0, %s)
    """
    cur = conn.cursor()
    cur.execute(sql, (title, content, description, column_id, now, now, source_url))
    conn.commit()
    return cur.lastrowid


def fetch_article_content(url):
    """抓取文章正文"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')

        # 移除无用标签
        for tag in soup.select('script, style, nav, header, footer, .ad, .ads, .sidebar, .comment'):
            tag.decompose()

        # 尝试常见正文选择器
        for sel in ['.article-content', '.content', '.article-body', '.detail-content',
                    'article', '.post-content', '#content', '.text']:
            el = soup.select_one(sel)
            if el and len(el.get_text(strip=True)) > 200:
                # 清理内联样式保留结构
                content_html = str(el)
                # 移除 script/iframe
                content_html = re.sub(r'<script[^>]*>.*?</script>', '', content_html, flags=re.S)
                content_html = re.sub(r'<iframe[^>]*>.*?</iframe>', '', content_html, flags=re.S)
                return content_html

        return None
    except Exception as e:
        print(f"  抓取正文失败: {e}")
        return None


# ========== 主流程 ==========

def crawl_source(source, conn=None):
    """爬取单个来源"""
    print(f"\n[{source['name']}] 开始抓取...")
    count = 0

    try:
        r = requests.get(source['url'], headers=HEADERS, timeout=10)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')

        items = soup.select(source['list_selector'])
        print(f"  找到 {len(items)} 条列表")

        for item in items[:10]:  # 每次最多抓10条
            # 提取标题
            title_el = item.select_one(source['title_selector'])
            if not title_el:
                continue
            title = clean_text(title_el.get_text())
            if not title or len(title) < 5:
                continue

            # 关键词过滤
            matched = any(kw.upper() in title.upper() for kw in source['keywords'])
            if not matched:
                continue

            # 提取链接
            link_el = item.select_one(source['link_selector'])
            if not link_el:
                continue
            href = link_el.get('href', '')
            if not href.startswith('http'):
                href = source['base_url'] + href

            print(f"  [{title[:30]}...]")

            # 去重检查
            if not DRY_RUN and conn and already_exists(conn, title):
                print(f"    -> 已存在，跳过")
                continue

            # 抓取正文
            content = fetch_article_content(href)
            if not content:
                print(f"    -> 正文为空，跳过")
                continue

            description = make_description(content)
            column_id = guess_column(title, description)

            if DRY_RUN:
                print(f"    [DRY] 标题: {title}")
                print(f"    [DRY] 栏目ID: {column_id}, 描述: {description[:50]}")
            else:
                nid = insert_article(conn, title, content, description, column_id, href)
                print(f"    -> 入库成功 ID={nid}")
                count += 1

            time.sleep(random.uniform(1.5, 3.0))  # 礼貌爬取

    except Exception as e:
        print(f"  来源抓取失败: {e}")

    return count


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 英语陪跑GO 内容爬虫启动")
    if DRY_RUN:
        print("** DRY RUN 模式，不写入数据库 **")

    conn = None
    if not DRY_RUN:
        try:
            conn = pymysql.connect(**DB)
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {e}")
            sys.exit(1)

    total = 0
    for source in SOURCES:
        total += crawl_source(source, conn)

    if conn:
        conn.close()

    print(f"\n完成！共入库 {total} 篇文章")


if __name__ == '__main__':
    main()
