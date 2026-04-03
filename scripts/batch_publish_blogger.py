#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量发布9篇文章到 xiachaoqing.blogspot.com
在本地Mac运行：
  cd ~/blogger-publisher
  python3 /Users/xiachaoqing/projects/epgo/scripts/batch_publish_blogger.py
"""
import sys, os, time

# 引入发布工具（需要在 ~/blogger-publisher 目录下运行）
PUBLISHER_DIR = os.path.expanduser("~/blogger-publisher")
sys.path.insert(0, PUBLISHER_DIR)
os.chdir(PUBLISHER_DIR)

from publish_to_blogger import publish_article

ARTICLES = [
    # 中文
    ("KET必备：最高频50个动词完整列表（附例句）",
     "/tmp/blogger-articles/ket-top-50-verbs.html",
     ["KET", "英语学习", "词汇", "剑桥英语"]),
    ("PET备考：必备30个形容词+搭配用法",
     "/tmp/blogger-articles/pet-top-30-adjectives.html",
     ["PET", "英语学习", "词汇", "剑桥英语"]),
    ("英语写作万能句：10个高分句型（KET/PET通用）",
     "/tmp/blogger-articles/10-universal-sentences-for-writing.html",
     ["KET", "PET", "英语写作", "备考技巧"]),
    # 英文
    ("10 Best Free AI Tools in 2026 (Actually Useful)",
     "/tmp/blogger-articles-en/10-best-free-ai-tools-2026.html",
     ["AI", "Tools", "Productivity", "2026"]),
    ("How I Use ChatGPT to Code Faster (Real Examples)",
     "/tmp/blogger-articles-en/how-i-use-chatgpt-to-code-faster.html",
     ["ChatGPT", "Programming", "AI", "Productivity"]),
    ("Midjourney vs DALL-E 3 in 2026: Which Is Better?",
     "/tmp/blogger-articles-en/midjourney-vs-dalle3-2026.html",
     ["Midjourney", "AI", "Image Generation", "2026"]),
    ("My Productivity Stack in 2026 (Tools I Actually Use)",
     "/tmp/blogger-articles-en/my-productivity-stack-2026.html",
     ["Productivity", "Tools", "2026"]),
    ("Python REST API Tutorial for Beginners (2026)",
     "/tmp/blogger-articles-en/python-rest-api-tutorial.html",
     ["Python", "API", "Programming", "Tutorial"]),
    ("Best Remote Work Tools in 2026: My Complete List",
     "/tmp/blogger-articles-en/remote-work-tools-2026.html",
     ["Remote Work", "Tools", "Productivity", "2026"]),
]

def main():
    print(f"准备发布 {len(ARTICLES)} 篇文章到 xiachaoqing.blogspot.com\n")
    success = 0
    for i, (title, path, labels) in enumerate(ARTICLES, 1):
        if not os.path.exists(path):
            print(f"[{i}/{len(ARTICLES)}] SKIP (文件不存在): {path}")
            continue
        print(f"[{i}/{len(ARTICLES)}] 发布: {title}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            post = publish_article(title, content, labels)
            print(f"  OK: {post.get('url', '')}")
            success += 1
        except Exception as e:
            print(f"  FAIL: {e}")
        if i < len(ARTICLES):
            time.sleep(3)
    print(f"\n完成: {success}/{len(ARTICLES)} 篇发布成功")

if __name__ == '__main__':
    main()
