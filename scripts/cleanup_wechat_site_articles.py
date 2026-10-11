#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clean an already-imported WeChat batch in ``ep_news``.

This is intentionally range-scoped.  It removes inline WeChat images and
公众号尾注, replaces remote covers with local site covers, and refreshes the
CTA so it can point readers to the official account.
"""
from __future__ import print_function

import argparse
import glob
import hashlib
import re

import pymysql


DB = {
    "host": "localhost",
    "port": 3306,
    "user": "xiachaoqing",
    "password": "Xia@07090218",
    "db": "epgo_db",
    "charset": "utf8mb4",
    "connect_timeout": 10,
}

CTA = (
    '<div class="epgo-article-cta" style="margin-top:32px;padding:16px 18px;'
    'background:#eff6ff;border-radius:8px;line-height:1.8;">'
    '<strong>继续学习</strong><br>'
    '<a href="https://go.xiachaoqing.com/epgo/assessment.html">做一次 KET/PET 入学测评</a> · '
    '<a href="https://go.xiachaoqing.com/epgo/">了解英语陪跑GO</a> · '
    '<a href="https://go.xiachaoqing.com/epgo/#follow">关注公众号「英语陪跑GO」</a>'
    '</div>'
)


def clean_content(value):
    value = value or ""
    value = re.sub(r"<img\b[^>]*?/?>", "", value, flags=re.I | re.S)
    value = re.sub(r"<svg\b[^>]*>.*?</svg\s*>", "", value, flags=re.I | re.S)
    value = re.sub(r"\s+powered-by\s*=\s*([\"']).*?\1", "", value, flags=re.I | re.S)

    def section(match):
        block = match.group(0)
        text = re.sub(r"<[^>]+>", " ", block)
        if any(x in text for x in ("觉得有用", "THE END", "禁止转载")):
            return ""
        return block

    value = re.sub(r"<section\b[^>]*>.*?</section\s*>", section, value, flags=re.I | re.S)
    value = re.sub(r"<p\b[^>]*>.*?(觉得有用.*?(转发|分享)|THE\s*END|原创内容\s*[·•]\s*禁止转载).*?</p\s*>", "", value, flags=re.I | re.S)
    value = re.sub(r"<p\b[^>]*>\s*<mp-style-type>.*?</p\s*>", "", value, flags=re.I | re.S)
    value = re.sub(r"<div class=[\"']epgo-article-cta[\"'][^>]*>.*?</div\s*>", "", value, flags=re.I | re.S)
    return value.strip() + CTA


def cover_for(class_id, title):
    paths = glob.glob("/www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers/*/*")
    paths = [p for p in paths if p.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    groups = {"ket": {101, 111, 112, 113, 114}, "pet": {102, 121, 122, 123, 124}, "reading": {103}, "speech": {104}, "daily": {105}}
    group = next((name for name, ids in groups.items() if class_id in ids), "daily")
    selected = sorted(p for p in paths if "/{}/".format(group) in p) or sorted(paths)
    if not selected:
        return ""
    idx = int(hashlib.sha1(title.encode("utf-8")).hexdigest()[:12], 16) % len(selected)
    return selected[idx].split("/www/wwwroot/go.xiachaoqing.com", 1)[-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-id", type=int, required=True)
    parser.add_argument("--max-id", type=int, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    db = pymysql.connect(**DB, cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()
    cur.execute("SELECT id,title,class1,content FROM ep_news WHERE id >= %s AND id < %s AND recycle=0", (args.min_id, args.max_id))
    rows = cur.fetchall()
    print("matched", len(rows))
    for row in rows[:10]:
        print(row["id"], row["title"])
    if not args.apply:
        print("dry-run only; pass --apply to write")
        db.close()
        return
    for row in rows:
        cover = cover_for(int(row["class1"] or 0), row["title"])
        cur.execute(
            "UPDATE ep_news SET content=%s, imgurl=%s, img_ok=%s WHERE id=%s",
            (clean_content(row["content"]), cover, 1 if cover else 0, row["id"]),
        )
    db.commit()
    db.close()
    print("updated", len(rows))


if __name__ == "__main__":
    main()
