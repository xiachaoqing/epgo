#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补发第6、7篇（速率限制后重试）"""
import sys, os, time

PUBLISHER_DIR = os.path.expanduser("~/blogger-publisher")
sys.path.insert(0, PUBLISHER_DIR)
os.chdir(PUBLISHER_DIR)

from publish_to_blogger import publish_article

REMAINING = [
    ("Midjourney vs DALL-E 3 in 2026: Which Is Better?",
     "/tmp/blogger-articles-en/midjourney-vs-dalle3-2026.html",
     ["Midjourney", "AI", "Image Generation", "2026"]),
    ("My Productivity Stack in 2026 (Tools I Actually Use)",
     "/tmp/blogger-articles-en/my-productivity-stack-2026.html",
     ["Productivity", "Tools", "2026"]),
]

print("等待 60 秒后重试...")
time.sleep(60)

for title, path, labels in REMAINING:
    print(f"发布: {title}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        post = publish_article(title, content, labels)
        print(f"  OK: {post.get('url', '')}")
    except Exception as e:
        print(f"  FAIL: {e}")
    time.sleep(15)
