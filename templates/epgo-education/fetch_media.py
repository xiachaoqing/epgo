#!/usr/bin/env python3
"""
文章图片/视频本地化脚本
把 ep_news 文章内容中的外部图片下载到服务器本地，并更新数据库中的 URL

用法:
    python3 fetch_media.py              # 处理所有文章
    python3 fetch_media.py --id 123     # 只处理指定文章
    python3 fetch_media.py --dry-run    # 只预览，不写数据库

依赖:
    pip3 install pymysql requests beautifulsoup4
"""

import os
import sys
import re
import time
import hashlib
import argparse
import logging
import urllib.request
from pathlib import Path
from urllib.parse import urlparse, urljoin

try:
    import pymysql
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("缺少依赖，请运行: pip3 install pymysql requests beautifulsoup4")
    sys.exit(1)

# ─── 配置 ───────────────────────────────────────────────
DB = dict(host="127.0.0.1", port=3306,
          user="xiachaoqing", password="07090218",
          database="epgo_db", charset="utf8mb4")

# 本地保存路径（相对于网站根目录）
UPLOAD_DIR = "/www/wwwroot/go.xiachaoqing.com/upload"
# 网站根 URL（用于替换数据库中的路径）
SITE_URL   = "https://go.xiachaoqing.com"

# 只下载这些域的图片（为空则下载所有外部图片）
ALLOWED_DOMAINS = []

# 跳过已经是本站图片的 URL
LOCAL_PREFIXES = ("/upload/", "../upload/", SITE_URL)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EPGOBot/1.0)",
    "Accept": "image/*,video/*,*/*"
}

# ─── 工具函数 ─────────────────────────────────────────────

def is_local(url: str) -> bool:
    """判断 URL 是否已经是本站资源"""
    for prefix in LOCAL_PREFIXES:
        if url.startswith(prefix):
            return True
    return False


def url_to_local_path(url: str, article_id: int) -> tuple[str, str]:
    """
    返回 (本地文件系统路径, 数据库中应存的相对路径)
    按年月分目录，文件名取 URL MD5 + 原扩展名
    """
    parsed = urlparse(url)
    ext = Path(parsed.path).suffix.lower() or ".jpg"
    allowed_ext = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg",
                   ".mp4", ".mov", ".webm", ".pdf"}
    if ext not in allowed_ext:
        ext = ".jpg"

    date_dir = time.strftime("%Y%m")
    fname = hashlib.md5(url.encode()).hexdigest()[:16] + ext
    rel = f"upload/{date_dir}/{fname}"
    full = os.path.join(UPLOAD_DIR, date_dir, fname)
    return full, f"../{rel}"


def download_file(url: str, dest: str) -> bool:
    """下载文件到 dest，返回是否成功"""
    if os.path.exists(dest):
        log.debug("已存在，跳过: %s", dest)
        return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, stream=True)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(65536):
                f.write(chunk)
        log.info("下载完成: %s → %s", url, dest)
        return True
    except Exception as e:
        log.warning("下载失败 %s : %s", url, e)
        return False


def localize_html(html: str, article_id: int, dry_run: bool) -> tuple[str, int]:
    """
    扫描 HTML 中的 <img src> 和 <video src/poster>，
    下载外部资源到本地并替换 URL。
    返回 (新 HTML, 替换数量)
    """
    if not html:
        return html, 0

    soup = BeautifulSoup(html, "html.parser")
    count = 0

    # img 标签
    for tag in soup.find_all("img"):
        src = tag.get("src") or tag.get("data-src") or tag.get("data-original")
        if not src or is_local(src):
            continue
        if ALLOWED_DOMAINS and not any(d in src for d in ALLOWED_DOMAINS):
            continue
        full_path, rel_path = url_to_local_path(src, article_id)
        if dry_run:
            log.info("[DRY] img: %s → %s", src, rel_path)
        else:
            if download_file(src, full_path):
                tag["src"] = rel_path
                if tag.get("data-src"):
                    tag["data-src"] = rel_path
                if tag.get("data-original"):
                    tag["data-original"] = rel_path
                count += 1

    # video / source 标签
    for tag in soup.find_all(["video", "source"]):
        for attr in ["src", "poster"]:
            src = tag.get(attr)
            if not src or is_local(src):
                continue
            full_path, rel_path = url_to_local_path(src, article_id)
            if dry_run:
                log.info("[DRY] video.%s: %s → %s", attr, src, rel_path)
            else:
                if download_file(src, full_path):
                    tag[attr] = rel_path
                    count += 1

    return str(soup), count


def localize_imgurl(imgurl: str, article_id: int, dry_run: bool) -> str:
    """处理文章封面图"""
    if not imgurl or is_local(imgurl):
        return imgurl
    full_path, rel_path = url_to_local_path(imgurl, article_id)
    if dry_run:
        log.info("[DRY] imgurl: %s → %s", imgurl, rel_path)
        return imgurl
    if download_file(imgurl, full_path):
        return rel_path
    return imgurl


# ─── 主流程 ───────────────────────────────────────────────

def process_articles(article_id: int = None, dry_run: bool = False):
    conn = pymysql.connect(**DB)
    cur  = conn.cursor(pymysql.cursors.DictCursor)

    if article_id:
        cur.execute("SELECT id, title, content, imgurl FROM ep_news WHERE id=%s", (article_id,))
    else:
        cur.execute("SELECT id, title, content, imgurl FROM ep_news WHERE recycle=0 ORDER BY id")

    rows = cur.fetchall()
    log.info("共 %d 篇文章待处理", len(rows))

    total_replaced = 0
    for row in rows:
        aid    = row["id"]
        title  = (row["title"] or "")[:40]
        html   = row["content"] or ""
        imgurl = row["imgurl"] or ""

        new_html, n = localize_html(html, aid, dry_run)
        new_imgurl  = localize_imgurl(imgurl, aid, dry_run)

        if n > 0 or new_imgurl != imgurl:
            total_replaced += n
            log.info("文章 %d《%s》替换 %d 个图片/视频", aid, title, n)
            if not dry_run:
                cur.execute(
                    "UPDATE ep_news SET content=%s, imgurl=%s WHERE id=%s",
                    (new_html, new_imgurl, aid)
                )
                conn.commit()

    cur.close()
    conn.close()
    log.info("完成！共替换 %d 个外部资源", total_replaced)


def main():
    parser = argparse.ArgumentParser(description="文章图片/视频本地化")
    parser.add_argument("--id",      type=int, default=None, help="只处理指定文章 ID")
    parser.add_argument("--dry-run", action="store_true",    help="预览模式，不写数据库")
    args = parser.parse_args()

    if args.dry_run:
        log.info("===== DRY RUN 模式，不修改数据库 =====")

    process_articles(article_id=args.id, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
