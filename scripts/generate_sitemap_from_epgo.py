#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate xiachaoqing.com/sitemap.xml from the live EPGO article table.

The previous sitemap was hand-maintained. This generator keeps fixed learning
pages and derives every public article URL from ``ep_news`` + ``ep_column``.
It writes to stdout by default so the output can be reviewed first.
"""
from __future__ import print_function

import argparse
import html
import os
import sys
from datetime import datetime

import pymysql


BASE = "https://xiachaoqing.com"
STATIC = [
    ("/", "monthly"), ("/ket/", "monthly"), ("/pet/", "monthly"),
    ("/reading/", "monthly"), ("/speech/", "monthly"), ("/daily/", "monthly"),
    ("/about/", "monthly"), ("/about1/", "monthly"),
    ("/ket-exam/list-111.html", "monthly"), ("/ket-word/list-112.html", "monthly"),
    ("/ket-write/list-113.html", "monthly"), ("/ket-listen/list-114.html", "monthly"),
    ("/pet-exam/list-121.html", "monthly"), ("/pet-word/list-122.html", "monthly"),
    ("/pet-write/list-123.html", "monthly"), ("/pet-read/list-124.html", "monthly"),
    ("/epgo/assessment.html", "monthly"), ("/epgo/tools.html", "monthly"),
    ("/privacy.html", "yearly"), ("/terms.html", "yearly"),
]


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
    cur.execute("SELECT id, class1, addtime FROM ep_news WHERE recycle=0 AND lang='cn' ORDER BY id")
    articles = cur.fetchall()
    db.close()

    today = datetime.now().strftime("%Y-%m-%d")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq in STATIC:
        lines.extend([
            "  <url>", "    <loc>{}</loc>".format(BASE + path),
            "    <lastmod>{}</lastmod>".format(today),
            "    <changefreq>{}</changefreq>".format(freq), "  </url>",
        ])
    article_urls = 0
    for row in articles:
        folder = folders.get(int(row["class1"] or 0))
        if not folder:
            continue
        lastmod = row["addtime"].strftime("%Y-%m-%d") if row["addtime"] else today
        lines.extend([
            "  <url>",
            "    <loc>{}</loc>".format(html.escape("{}/{}/{}.html".format(BASE, folder, row["id"]))),
            "    <lastmod>{}</lastmod>".format(lastmod),
            "    <changefreq>monthly</changefreq>", "  </url>",
        ])
        article_urls += 1
    lines.append("</urlset>")
    output = "\n".join(lines) + "\n"
    if args.output == "-":
        sys.stdout.write(output)
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
    print("generated {} static + {} article URLs".format(len(STATIC), article_urls), file=sys.stderr)


if __name__ == "__main__":
    main()
