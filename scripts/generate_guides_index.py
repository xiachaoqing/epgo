#!/usr/bin/env python3
"""Generate a public index of the reviewed, substantial learning guides."""
from __future__ import print_function

import argparse
import html
import os
import re
from collections import defaultdict

import pymysql


BASE = "https://xiachaoqing.com"
ISSUES = ("原创专题", "editorial-v2")


def db_value(config, key):
    match = re.search(r'%s\s*=\s*(?:"([^"]*)"|([^\s]+))' % key, config)
    if not match:
        raise RuntimeError("missing database setting: {}".format(key))
    return match.group(1) or match.group(2)


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
    cur.execute("SELECT id,name,foldername FROM ep_column WHERE isshow=1")
    columns = {int(row["id"]): row for row in cur.fetchall()}
    cur.execute(
        "SELECT id,title,description,class1,updatetime,addtime FROM ep_news "
        "WHERE recycle=0 AND lang='cn' AND issue IN (%s,%s) "
        "AND LENGTH(content)>=2000 ORDER BY class1,COALESCE(updatetime,addtime) DESC,id DESC",
        ISSUES,
    )
    rows = cur.fetchall()
    db.close()

    groups = defaultdict(list)
    for row in rows:
        column = columns.get(int(row["class1"] or 0))
        if column:
            # FCE currently shares the public PET/skill routes, but deserves
            # its own heading in the index so readers can find the advanced
            # material without mistaking it for PET content.
            if (row["title"] or "").strip().lower().startswith("fce"):
                column = dict(column)
                column["id"] = -1
                column["name"] = "FCE进阶"
            groups[column["id"]].append((column, row))

    lines = [
        "<!doctype html>",
        '<html lang="zh-CN"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<title>学习指南索引｜英语陪跑GO</title>',
        '<meta name="description" content="英语陪跑GO 的 KET、PET、FCE、阅读、写作、听力和口语原创学习指南索引。">',
        '<meta name="robots" content="index,follow">',
        '<link rel="canonical" href="{}/guides.html">'.format(BASE),
        '<link rel="alternate" type="application/rss+xml" title="英语陪跑GO学习指南" href="{}/feed.xml">'.format(BASE),
        '<style>body{margin:0;background:#f6f8fb;color:#1f2937;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;line-height:1.7}.wrap{max-width:1080px;margin:0 auto;padding:0 20px}.top{background:#1565c0;color:#fff;padding:22px 0}.top a{color:#fff;text-decoration:none;margin-right:18px;font-size:14px}.hero{background:#fff;padding:42px 0 32px;border-bottom:1px solid #e5e7eb}.hero h1{margin:0 0 8px;font-size:32px;color:#111827}.hero p{margin:0;max-width:760px;color:#667085}.count{display:inline-block;margin-top:18px;padding:6px 12px;border-radius:999px;background:#eff6ff;color:#1d4ed8;font-size:13px}.group{background:#fff;margin:22px 0;padding:24px;border-radius:12px;box-shadow:0 2px 8px rgba(15,23,42,.05)}.group h2{margin:0 0 14px;font-size:22px;color:#111827}.group ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 28px;list-style:none;padding:0;margin:0}.group li{border-bottom:1px solid #eef2f7;padding:6px 0}.group a{color:#1d4ed8;text-decoration:none}.group a:hover{text-decoration:underline}.desc{display:block;color:#667085;font-size:13px;line-height:1.5}.foot{padding:30px 0 50px;text-align:center;color:#667085;font-size:13px}.foot a{color:#1d4ed8}@media(max-width:700px){.group ul{grid-template-columns:1fr}.hero h1{font-size:27px}}</style>',
        '</head><body>',
        '<header class="top"><div class="wrap"><a href="/">英语陪跑GO</a><a href="/ket/">KET备考</a><a href="/pet/">PET备考</a><a href="/reading/">英语阅读</a><a href="/speech/">英语演讲</a><a href="/guides.html">学习指南索引</a><a href="/study-log.html">学习记录表</a><a href="/editorial.html">内容编辑说明</a></div></header>',
        '<main><section class="hero"><div class="wrap"><h1>学习指南索引</h1><p>这里集中整理英语陪跑GO 已完成编辑复核的长期学习指南，覆盖 KET、PET、FCE、阅读、写作、听力和口语。文章中的练习和场景以自编内容为主，并在正文中说明适用边界。</p><span class="count">共 {} 篇公开指南</span></div></section>'.format(len(rows)),
    ]
    for column_id in sorted(groups):
        column = groups[column_id][0][0]
        items = [pair[1] for pair in groups[column_id]]
        lines.append('<section class="group"><h2>{}</h2><ul>'.format(html.escape(column["name"] or "学习指南")))
        for row in items:
            href = "{}/{}/{}.html".format(BASE, (column["foldername"] or "").strip("/"), row["id"])
            title = html.escape(row["title"] or "")
            summary = html.escape(re.sub(r"\s+", " ", row["description"] or "").strip()[:110])
            lines.append('<li><a href="{}">{}</a><span class="desc">{}</span></li>'.format(href, title, summary))
        lines.append('</ul></section>')
    lines.extend([
        '</main><footer class="foot"><div class="wrap">',
        '<a href="/privacy.html">隐私政策</a> · <a href="/terms.html">服务条款</a> · <a href="/editorial.html">内容编辑说明</a> · <a href="/study-log.html">学习记录表</a> · <a href="/feedback/">联系我们</a> · <a href="/">返回首页</a>',
        '<br>英语陪跑GO｜文章示例不等同于官方考试题目或成绩承诺</div></footer>',
        '</body></html>',
    ])
    output = "\n".join(lines) + "\n"
    if args.output == "-":
        print(output, end="")
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
    print("generated {} guide links".format(len(rows)), file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
