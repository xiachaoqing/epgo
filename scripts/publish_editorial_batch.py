#!/usr/bin/env python3
"""Publish a checked editorial batch without importing unreviewed WeChat material.

The command is intentionally dry-run by default.  Every item must already have
an editorial title, description, class, staggered publication date and a
meaningful body.  ``--apply`` is the only mode that writes ``ep_news``.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

import pymysql


def load_db_config(path):
    raw = Path(path).read_text(encoding="utf-8")

    def value(name):
        match = re.search(rf"{name}\s*=\s*\"([^\"]*)\"", raw)
        if not match:
            raise RuntimeError(f"Missing database setting: {name}")
        return match.group(1)

    return {
        "host": value("con_db_host"),
        "user": value("con_db_id"),
        "password": value("con_db_pass"),
        "db": value("con_db_name"),
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
    }


def image_for_class(class1):
    if class1 in {101, 111, 112, 113, 114}:
        return "/upload/epgo-covers/ket.png"
    if class1 in {102, 121, 122, 123, 124}:
        return "/upload/epgo-covers/pet.png"
    if class1 == 104:
        return "/upload/epgo-covers/speech.png"
    return "/upload/epgo-covers/reading.png"


def load_items(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(items, list) or not items:
        raise RuntimeError("Manifest must be a non-empty JSON list")
    if len(items) > 20:
        raise RuntimeError("Refusing batches larger than 20 items")
    now = datetime.now()
    seen = set()
    for item in items:
        required = {"title", "digest", "content", "class1", "addtime"}
        if not required.issubset(item):
            raise RuntimeError(f"Missing fields in item: {sorted(required - set(item))}")
        title = str(item["title"]).strip()
        if not title or title in seen:
            raise RuntimeError(f"Duplicate or empty title: {title!r}")
        seen.add(title)
        if len(str(item["digest"]).strip()) < 30:
            raise RuntimeError(f"Digest too short: {title}")
        if len(str(item["content"]).encode("utf-8")) < 2000:
            raise RuntimeError(f"Content shorter than 2000 UTF-8 bytes: {title}")
        try:
            addtime = datetime.strptime(item["addtime"], "%Y-%m-%d %H:%M:%S")
        except ValueError as exc:
            raise RuntimeError(f"Bad addtime for {title}") from exc
        if addtime > now:
            raise RuntimeError(f"Future addtime for {title}")
        if int(item["class1"]) not in {101, 102, 103, 104, 111, 112, 113, 114, 121, 122, 123, 124}:
            raise RuntimeError(f"Unsupported public class1 for {title}: {item['class1']}")
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--db-config", default=os.environ.get("EPGO_DB_CONFIG", "config/config_db.php"))
    parser.add_argument("--backup-dir", default="/tmp")
    args = parser.parse_args()

    items = load_items(args.manifest)
    conn = pymysql.connect(**load_db_config(args.db_config))
    inserted = []
    try:
        conn.begin()
        with conn.cursor() as cur:
            for item in items:
                cur.execute("SELECT id FROM ep_news WHERE title=%s LIMIT 1", (item["title"],))
                if cur.fetchone():
                    raise RuntimeError(f"Title already exists: {item['title']}")
            print(f"Validated {len(items)} editorial articles; all bodies are >=2000 UTF-8 bytes")
            if not args.apply:
                conn.rollback()
                return
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = ("INSERT INTO ep_news "
                   "(title,description,content,class1,class2,class3,no_order,wap_ok,img_ok,imgurl,"
                   "com_ok,issue,hits,updatetime,addtime,lang,recycle,displaytype,publisher) "
                   "VALUES (%s,%s,%s,%s,0,0,0,1,1,%s,1,%s,0,%s,%s,'cn',0,1,%s)")
            for item in items:
                cur.execute(sql, (
                    item["title"], item["digest"], item["content"], int(item["class1"]),
                    image_for_class(int(item["class1"])), "editorial-v2", now,
                    item["addtime"], "Cathy",
                ))
                inserted.append(cur.lastrowid)
        conn.commit()
        with conn.cursor() as cur:
            placeholders = ",".join(["%s"] * len(inserted))
            cur.execute(
                f"SELECT id,title,description,content,class1,issue,updatetime,addtime,recycle "
                f"FROM ep_news WHERE id IN ({placeholders}) ORDER BY id",
                inserted,
            )
            backup = cur.fetchall()
        backup_dir = Path(args.backup_dir)
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / f"epgo-editorial-batch-{datetime.now():%Y%m%d-%H%M%S}.json"
        backup_path.write_text(json.dumps(backup, ensure_ascii=False, default=str, indent=2), encoding="utf-8")
        os.chmod(backup_path, 0o600)
        print(f"Applied {len(inserted)} articles; ids={inserted}; backup={backup_path}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
