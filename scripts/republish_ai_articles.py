#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重新发布AI方向文章"""
import sys, os, time, warnings
warnings.filterwarnings('ignore')

PUBLISHER_DIR = os.path.expanduser("~/blogger-publisher")
sys.path.insert(0, PUBLISHER_DIR)
os.chdir(PUBLISHER_DIR)

from publish_to_blogger import publish_article

ARTICLES = [
    ("10 Best Free AI Tools in 2026 (Actually Useful)",
     "/tmp/blogger-articles-en/10-best-free-ai-tools-2026.html",
     ["AI Tools", "Productivity", "2026", "Free Tools"]),
    ("How I Use ChatGPT to Code Faster (Real Examples)",
     "/tmp/blogger-articles-en/how-i-use-chatgpt-to-code-faster.html",
     ["ChatGPT", "Coding", "AI", "Productivity"]),
    ("Midjourney vs DALL-E 3 in 2026: Which Is Better?",
     "/tmp/blogger-articles-en/midjourney-vs-dalle3-2026.html",
     ["Midjourney", "DALL-E", "AI Image", "2026"]),
    ("My Productivity Stack in 2026 (Tools I Actually Use)",
     "/tmp/blogger-articles-en/my-productivity-stack-2026.html",
     ["Productivity", "Tools", "2026"]),
    ("Python REST API Tutorial for Beginners (2026)",
     "/tmp/blogger-articles-en/python-rest-api-tutorial.html",
     ["Python", "API", "Tutorial", "2026"]),
    ("Best Remote Work Tools in 2026: My Complete List",
     "/tmp/blogger-articles-en/remote-work-tools-2026.html",
     ["Remote Work", "Tools", "2026"]),
]

success = 0
for i, (title, path, labels) in enumerate(ARTICLES, 1):
    print(f"[{i}/{len(ARTICLES)}] {title}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        post = publish_article(title, content, labels)
        print(f"  OK: {post.get('url','')}")
        success += 1
    except Exception as e:
        print(f"  FAIL: {e}")
    if i < len(ARTICLES):
        time.sleep(12)

print(f"\n完成: {success}/{len(ARTICLES)}")
