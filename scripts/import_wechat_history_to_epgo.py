#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import owned WeChat articles into the MetInfo ``ep_news`` table.

The current production schema is different from the old importer in this
repository.  This script uses the live schema (``class1``, ``addtime``,
``publisher``) and is dry-run by default.  It never overwrites an existing
article with the same normalized title.

Examples (run on the EPGO server):

    python3 import_wechat_history_to_epgo.py --input /tmp/wechat-history.json
    python3 import_wechat_history_to_epgo.py --input /tmp/wechat-history.json --apply
"""
from __future__ import print_function

import argparse
from collections import Counter
import html
import json
import re
import sys
from datetime import datetime, timedelta, timezone

import pymysql


DEFAULT_DB = {
    "host": "localhost",
    "port": 3306,
    "user": "xiachaoqing",
    "password": "Xia@07090218",
    "db": "epgo_db",
    "charset": "utf8mb4",
    "connect_timeout": 10,
}

# Live EPGO columns.  These IDs are read from ep_column on the production
# server and match the public Chinese navigation.
COLUMNS = {
    "ket": 101,
    "ket_exam": 111,
    "ket_word": 112,
    "ket_write": 113,
    "ket_listen": 114,
    "pet": 102,
    "pet_exam": 121,
    "pet_word": 122,
    "pet_write": 123,
    "pet_read": 124,
    "reading": 103,
    "speech": 104,
    "daily": 105,
}


def normalize_title(value):
    value = html.unescape(value or "")
    return re.sub(r"[\s\u3000]+", "", value).strip().lower()


def strip_dangerous_html(value):
    """Keep article structure while removing WeChat-only and unsafe markup."""
    value = value or ""
    value = re.sub(r"<!--.*?-->", "", value, flags=re.S)
    value = re.sub(r"<\s*(script|iframe|object|embed|form)[^>]*>.*?<\s*/\s*\1\s*>", "", value, flags=re.I | re.S)
    # WeChat stores some images in data-src.  Promote that URL before
    # dropping data-* attributes.
    value = re.sub(
        r"<img([^>]*?)data-src=[\"']([^\"']+)[\"']([^>]*)>",
        r'<img\1src="\2"\3>',
        value,
        flags=re.I,
    )
    value = re.sub(r"\s+on[a-z]+\s*=\s*([\"']).*?\1", "", value, flags=re.I | re.S)
    value = re.sub(r"\s+data-[a-z0-9_-]+\s*=\s*([\"']).*?\1", "", value, flags=re.I | re.S)
    value = re.sub(r"\s+leaf\s*=\s*([\"']).*?\1", "", value, flags=re.I | re.S)
    # Keep a responsive image rule even when the source used a fixed width.
    def responsive_image(match):
        attrs = match.group(1)
        attrs = re.sub(r"\s+style\s*=\s*([\"']).*?\1", "", attrs, flags=re.I | re.S)
        return '<img{} style="max-width:100%;height:auto;border-radius:8px;" />'.format(attrs)

    value = re.sub(r"<img([^>]*)/?>", responsive_image, value, flags=re.I)
    return value.strip()


def plain_text(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def classify(title):
    text = title.lower()
    if "ket" in text:
        if any(k in title for k in ("真题", "题型", "完形")):
            return COLUMNS["ket_exam"]
        if any(k in title for k in ("词汇", "单词", "短语", "易混词", "介词")):
            return COLUMNS["ket_word"]
        if any(k in title for k in ("写作", "作文", "连接词", "句式", "语法")):
            return COLUMNS["ket_write"]
        if "听力" in title:
            return COLUMNS["ket_listen"]
        return COLUMNS["ket"]
    if "pet" in text:
        if any(k in title for k in ("真题", "题型", "完形")):
            return COLUMNS["pet_exam"]
        if any(k in title for k in ("词汇", "单词", "短语", "易混词", "介词")):
            return COLUMNS["pet_word"]
        if any(k in title for k in ("写作", "作文", "连接词", "句式")):
            return COLUMNS["pet_write"]
        if "阅读" in title:
            return COLUMNS["pet_read"]
        return COLUMNS["pet"]
    if any(k in title for k in ("阅读", "绘本", "故事")):
        return COLUMNS["reading"]
    if any(k in title for k in ("演讲", "TED")):
        return COLUMNS["speech"]
    return COLUMNS["daily"]


def keywords(title):
    words = ["英语陪跑GO", "剑桥英语"]
    for word in ("KET", "PET", "FCE", "阅读", "听力", "口语", "写作", "词汇", "语法"):
        if word.lower() in title.lower() and word not in words:
            words.insert(0, word)
    return ",".join(words[:6])


def published_at(item):
    stamp = int(item.get("bundle_update_time") or 0)
    if not stamp:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # WeChat timestamps are UTC seconds.  Convert to China Standard Time.
    dt = datetime.fromtimestamp(stamp, tz=timezone.utc).astimezone(
        timezone(timedelta(hours=8))
    )
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def website_content(item):
    body = strip_dangerous_html(item.get("content", ""))
    title = html.escape(item.get("title", ""), quote=True)
    author = html.escape(item.get("author") or "Cathy", quote=True)
    original = item.get("content_source_url") or item.get("url") or ""
    link = ""
    if original.startswith("http"):
        link = ' <a href="{}" rel="nofollow noopener" target="_blank">查看公众号原文</a>'.format(
            html.escape(original, quote=True)
        )
    note = (
        '<div class="epgo-article-meta" style="margin:0 0 24px;padding:12px 16px;'
        'background:#f6f8fb;border-left:3px solid #2d6cdf;color:#667085;font-size:14px;line-height:1.8;">'
        '<strong>{}</strong> · 英语陪跑GO<br>本文为英语陪跑GO原创内容的网站整理版。{}</div>'
    ).format(author, link)
    related = (
        '<div class="epgo-article-cta" style="margin-top:32px;padding:16px 18px;'
        'background:#eff6ff;border-radius:8px;line-height:1.8;">'
        '<strong>继续学习</strong><br>'
        '<a href="https://go.xiachaoqing.com/epgo/assessment.html">做一次 KET/PET 入学测评</a> · '
        '<a href="https://go.xiachaoqing.com/epgo/">了解英语陪跑GO</a>'
        '</div>'
    )
    return note + body + related


def load_items(path):
    with open(path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    items = payload if isinstance(payload, list) else payload.get("articles", [])
    cleaned = []
    seen = set()
    for item in items:
        title = (item.get("title") or "").strip()
        content = item.get("content") or ""
        key = normalize_title(title)
        if not title or not content or key in seen:
            continue
        seen.add(key)
        cleaned.append(item)
    return cleaned


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--apply", action="store_true", help="write into ep_news; default is dry-run")
    args = parser.parse_args()

    items = load_items(args.input)
    db = pymysql.connect(**DEFAULT_DB, cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()
    cur.execute("SELECT title FROM ep_news WHERE recycle=0")
    existing = {normalize_title(row["title"]) for row in cur.fetchall()}

    candidates = []
    skipped = 0
    for item in items:
        key = normalize_title(item["title"])
        if key in existing:
            skipped += 1
            continue
        html_body = website_content(item)
        candidates.append(
            {
                "title": item["title"].strip(),
                "content": html_body,
                "description": plain_text(item.get("digest") or item.get("content", ""))[:200],
                "class1": classify(item["title"]),
                "keywords": keywords(item["title"]),
                "imgurl": item.get("thumb_url") or "",
                "addtime": published_at(item),
            }
        )
        existing.add(key)

    print("source articles: {}".format(len(items)))
    print("new candidates: {}".format(len(candidates)))
    print("skipped existing/duplicate: {}".format(skipped))
    print("column distribution: {}".format(dict(Counter(row["class1"] for row in candidates))))
    for row in candidates[:20]:
        print("  [{}] {}".format(row["class1"], row["title"]))

    if not args.apply:
        print("dry-run only; pass --apply after reviewing this list")
        db.close()
        return 0

    try:
        for row in candidates:
            cur.execute(
                """INSERT INTO ep_news
                (title, ctitle, keywords, description, content, class1,
                 imgurl, img_ok, wap_ok, displaytype, lang, recycle,
                 publisher, updatetime, addtime)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,1,'cn',0,%s,%s,%s)""",
                (
                    row["title"], row["title"], row["keywords"], row["description"],
                    row["content"], row["class1"], row["imgurl"],
                    1 if row["imgurl"] else 0, "英语陪跑GO", row["addtime"], row["addtime"],
                ),
            )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
    print("inserted: {}".format(len(candidates)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
