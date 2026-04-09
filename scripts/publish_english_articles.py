#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布英语陪跑GO方向的10篇Blogger文章"""
import sys, os, time, warnings
warnings.filterwarnings('ignore')

PUBLISHER_DIR = os.path.expanduser("~/blogger-publisher")
sys.path.insert(0, PUBLISHER_DIR)
os.chdir(PUBLISHER_DIR)

from publish_to_blogger import publish_article

ARTICLES = [
    ("KET阅读技巧：5个方法让你阅读分数提升20分",
     "/tmp/blogger-english/ket-reading-tips.html",
     ["KET", "英语阅读", "剑桥英语", "备考技巧"]),
    ("KET听力真题解析：这3种题型让你不再失分",
     "/tmp/blogger-english/ket-listening-guide.html",
     ["KET", "英语听力", "剑桥英语", "真题解析"]),
    ("KET写作邮件范文：5个万能模板（高分必备）",
     "/tmp/blogger-english/ket-writing-email.html",
     ["KET", "英语写作", "剑桥英语", "写作模板"]),
    ("PET阅读长文攻略：如何在限时内读懂复杂文章",
     "/tmp/blogger-english/pet-reading-long-text.html",
     ["PET", "英语阅读", "剑桥英语", "备考技巧"]),
    ("KET/PET必考语法：时态一网打尽（附练习题）",
     "/tmp/blogger-english/english-grammar-tense.html",
     ["KET", "PET", "英语语法", "时态", "备考"]),
    ("KET高频词汇：日常生活主题100词（分类记忆）",
     "/tmp/blogger-english/ket-vocabulary-daily-life.html",
     ["KET", "词汇", "英语学习", "日常用语"]),
    ("PET口语考试攻略：考官最想听到的表达方式",
     "/tmp/blogger-english/pet-speaking-tips.html",
     ["PET", "英语口语", "剑桥英语", "口语技巧"]),
    ("剑桥英语级别对照：KET/PET/FCE/CAE你在哪一级？",
     "/tmp/blogger-english/cambridge-english-levels.html",
     ["剑桥英语", "KET", "PET", "FCE", "英语水平"]),
    ("30天KET备考计划（详细版）：每天只需1小时",
     "/tmp/blogger-english/english-study-plan-30days.html",
     ["KET", "学习计划", "英语备考", "30天"]),
    ("PET写作文章题（Article）：考官评分标准+范文解析",
     "/tmp/blogger-english/pet-writing-article.html",
     ["PET", "英语写作", "剑桥英语", "写作范文"]),
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
