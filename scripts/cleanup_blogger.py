#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理blogspot：
1. 删除所有AI/工具方向文章
2. 删除重复文章
只保留英语学习方向文章
在 ~/blogger-publisher 目录下运行
"""
import sys, os, warnings
warnings.filterwarnings('ignore')
os.chdir(os.path.expanduser('~/blogger-publisher'))
sys.path.insert(0, '.')
from publish_to_blogger import get_blogger_service, get_blog_id

service = get_blogger_service()
blog_id = get_blog_id()

# 获取所有文章
posts = service.posts().list(blogId=blog_id, maxResults=50, orderBy='PUBLISHED').execute()
all_posts = posts.get('items', [])

print(f"共 {len(all_posts)} 篇文章\n")

# 要删除的关键词（AI/工具方向）
DELETE_KEYWORDS = [
    'AI Tools', 'ChatGPT', 'Midjourney', 'DALL-E',
    'Productivity Stack', 'Remote Work Tools', 'REST API',
    'Python REST', 'Code Faster', 'Code 10x',
    'Image Generator', 'Developer'
]

# 英语学习方向保留（含关键词则保留）
KEEP_KEYWORDS = ['KET', 'PET', '英语', 'English', 'IELTS', 'FCE', '写作', '词汇', '备考']

to_delete = []
seen_titles = {}

for p in all_posts:
    title = p['title']
    pid = p['id']

    # 检查是否重复
    if title in seen_titles:
        print(f"[重复] {title[:60]}")
        to_delete.append(pid)
        continue
    seen_titles[title] = pid

    # 检查是否AI方向
    is_wrong = any(kw.lower() in title.lower() for kw in DELETE_KEYWORDS)
    is_english = any(kw in title for kw in KEEP_KEYWORDS)

    if is_wrong and not is_english:
        print(f"[删除-AI方向] {title[:60]}")
        to_delete.append(pid)
    else:
        print(f"[保留] {title[:60]}")

print(f"\n准备删除 {len(to_delete)} 篇，保留 {len(all_posts)-len(to_delete)} 篇")
confirm = input("确认删除? (y/n): ")
if confirm.lower() != 'y':
    print("已取消")
    sys.exit(0)

import time
deleted = 0
for pid in to_delete:
    try:
        service.posts().delete(blogId=blog_id, postId=pid).execute()
        deleted += 1
        print(f"  已删除 {pid}")
        time.sleep(2)
    except Exception as e:
        print(f"  删除失败 {pid}: {e}")

print(f"\n完成：删除 {deleted}/{len(to_delete)} 篇")
