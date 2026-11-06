#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate an RSS feed containing only reviewed, public learning articles."""
from __future__ import print_function

import argparse
import html
import os
import re
from datetime import datetime

import pymysql


BASE = "https://xiachaoqing.com"
EDITORIAL_ISSUES = ("原创专题", "editorial-v2")


def plain_text(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="-")
    parser.add_argument("--db-host", default="localhost")
    parser.add_argument("--db-user", default="xiachaoqing")
    parser.add_argument("--db-password", default=os.environ.get("EPGO_DB_PASSWORD", ""))
    parser.add_argument("--db-name", default="epgo_db")
    args = parser.parse_args()
    if not args.db_password:
        parser.error("--db-password or EPGO_DB_PASSWORD is required")
    db = pymysql.connect(
        host=args.db_host, user=args.db_user, password=args.db_password,
        db=args.db_name, charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
    )
    cur = db.cursor()
    cur.execute("SELECT id, foldername FROM ep_column WHERE isshow=1")
    folders = {int(row["id"]): (row["foldername"] or "").strip("/") for row in cur.fetchall()}
    cur.execute(
        "SELECT id,title,description,content,class1,updatetime,addtime FROM ep_news "
        "WHERE recycle=0 AND lang='cn' AND issue IN (%s,%s) AND LENGTH(content)>=2000 "
        "ORDER BY COALESCE(updatetime,addtime) DESC, id DESC LIMIT 100",
        EDITORIAL_ISSUES,
    )
    articles = cur.fetchall()
    db.close()

    now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0"><channel>',
        '<title>英语陪跑GO｜KET/PET/FCE 学习指南</title>',
        '<link>{}/</link>'.format(BASE),
        '<description>英语陪跑GO 的 KET/PET/FCE 备考、阅读、听力、写作和家庭学习指南。</description>',
        '<language>zh-CN</language>',
        '<lastBuildDate>{}</lastBuildDate>'.format(now),
    ]
    count = 0
    for row in articles:
        folder = folders.get(int(row["class1"] or 0))
        if not folder:
            continue
        modified = row["updatetime"] or row["addtime"]
        stamp = modified.strftime("%a, %d %b %Y %H:%M:%S +0800") if modified else now
        url = "{}/{}/{}.html".format(BASE, folder, row["id"])
        summary = plain_text(row["description"] or row["content"])[:240]
        lines.extend([
            "<item>",
            "<title>{}</title>".format(html.escape(row["title"] or "")),
            "<link>{}</link>".format(html.escape(url)),
            "<guid isPermaLink=\"true\">{}</guid>".format(html.escape(url)),
            "<description>{}</description>".format(html.escape(summary)),
            "<pubDate>{}</pubDate>".format(stamp),
            "</item>",
        ])
        count += 1
    lines.append("</channel></rss>")
    output = "\n".join(lines) + "\n"
    if args.output == "-":
        print(output, end="")
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
    print("generated {} reviewed feed items".format(count), file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
