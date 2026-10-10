#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch the account's published articles from WeChat's official API.

Run this file on the WeChat service host with that service's virtualenv:

    venv/bin/python3 scripts/fetch_wechat_history.py > /tmp/wechat-history.json

The script deliberately emits JSON only.  It does not publish, delete, or
update any WeChat content.
"""
from __future__ import print_function

import json
import os
import sys
import time

# The file is intentionally copied to /tmp on the service host.  Add the
# service working directory so ``app`` can still be imported there.
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from app.api.content import _wx_post


def fetch_all():
    offset = 0
    bundles = []
    total = None
    while total is None or offset < total:
        result = _wx_post(
            "/cgi-bin/freepublish/batchget",
            {"offset": offset, "count": 20, "no_content": 0},
        )
        if result.get("errcode"):
            raise RuntimeError(
                "WeChat API error {}: {}".format(
                    result.get("errcode"), result.get("errmsg", "unknown")
                )
            )
        page = result.get("item", [])
        total = int(result.get("total_count", len(page)))
        if not page:
            break
        bundles.extend(page)
        offset += len(page)

    articles = []
    for bundle in bundles:
        content = bundle.get("content") or {}
        for item in content.get("news_item", []) or []:
            if item.get("is_deleted"):
                continue
            articles.append(
                {
                    "article_id": bundle.get("article_id", ""),
                    "bundle_update_time": bundle.get("update_time")
                    or content.get("update_time")
                    or 0,
                    "title": item.get("title", ""),
                    "author": item.get("author", ""),
                    "digest": item.get("digest", ""),
                    "content": item.get("content", ""),
                    "thumb_url": item.get("thumb_url", ""),
                    "url": item.get("url", ""),
                    "content_source_url": item.get("content_source_url", ""),
                }
            )
    return {
        "source": "wechat_freepublish_batchget",
        "fetched_at": int(time.time()),
        "bundle_count": len(bundles),
        "article_count": len(articles),
        "articles": articles,
    }


if __name__ == "__main__":
    try:
        json.dump(fetch_all(), sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    except Exception as exc:
        print("fetch failed: {}".format(exc), file=sys.stderr)
        sys.exit(1)
