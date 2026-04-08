#!/usr/bin/env python3
"""
为各英语教育栏目爬取并下载专业封面图
图片来源：Unsplash 免费商用图库
直接在远程服务器下载到 /upload/epgo-photo-covers/{category}/ 并更新数据库

用法:
    python3 fetch_category_covers.py              # 下载所有栏目封面
    python3 fetch_category_covers.py --dry-run    # 预览模式，只打印不下载

依赖:
    pip3 install pymysql
"""

import os
import sys
import time
import subprocess
import argparse
import logging
from pathlib import Path

try:
    import pymysql
except ImportError:
    print("缺少依赖，请运行: pip3 install pymysql")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# ─── 配置 ───────────────────────────────────────────────
DB = dict(
    host="127.0.0.1", port=3306,
    user="xiachaoqing", password="***REMOVED***",
    database="epgo_db", charset="utf8mb4"
)

SERVER = "epgo"
UPLOAD_DIR = "/www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers"
SITE_URL = "https://xiachaoqing.com"

# 栏目封面配置
# category_id -> (foldername, unsplash_url, description)
CATEGORY_COVERS = {
    101: ("ket",
          "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=1200&h=800&fit=crop&q=80",
          "KET备考 - 学生在教室认真学习"),
    102: ("pet",
          "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&h=800&fit=crop&q=80",
          "PET备考 - 学生在图书馆专注阅读"),
    103: ("reading",
          "https://images.unsplash.com/photo-1507842217343-583f20270319?w=1200&h=800&fit=crop&q=80",
          "英语阅读 - 打开书本，开启知识之旅"),
    104: ("speech",
          "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=800&fit=crop&q=80",
          "英语演讲 - 舞台上自信表达"),
    105: ("daily",
          "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&h=800&fit=crop&q=80",
          "每日英语 - 日积月累，水滴石穿"),
    106: ("download",
          "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1200&h=800&fit=crop&q=80",
          "资料下载 - 精选学习资料库"),
    107: ("about",
          "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=800&fit=crop&q=80",
          "关于我们 - 专业的英语学习平台"),
}

# ─── 工具函数 ─────────────────────────────────────────────

def run_remote(cmd):
    """在远程服务器执行命令"""
    result = subprocess.run(
        ["ssh", SERVER, f"bash -c '{cmd}'"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    return result.stdout.strip(), result.returncode


def download_on_remote(url, remote_path):
    """在远程服务器直接下载文件"""
    try:
        remote_dir = os.path.dirname(remote_path)
        # 确保目录存在
        mkdir_cmd = f"mkdir -p {remote_dir} && chmod 755 {remote_dir}"
        out, rc = run_remote(mkdir_cmd)
        if rc != 0:
            log.error("✗ 创建远程目录失败: %s", out)
            return False

        # 使用 curl 下载到远程服务器
        curl_cmd = f'curl -fsSL -m 30 "{url}" -o "{remote_path}"'
        out, rc = run_remote(curl_cmd)
        if rc != 0:
            log.error("✗ 远程下载失败 (exit code: %d): %s", rc, out)
            return False

        # 验证文件存在且不为空
        check_cmd = f'[ -s "{remote_path}" ] && ls -lh "{remote_path}" | awk "{{print $5}}" || echo "EMPTY"'
        size, rc = run_remote(check_cmd)

        if rc != 0 or size == "EMPTY":
            log.error("✗ 文件为空或不存在: %s", remote_path)
            return False

        log.info("✓ 下载成功: %s (%s)", os.path.basename(remote_path), size)
        return True
    except Exception as e:
        log.error("✗ 远程下载异常: %s", e)
        return False


def update_articles_cover(category_id, web_url, dry_run=False):
    """
    更新数据库中该栏目的所有文章封面
    只替换当前仍使用默认占位图的文章
    """
    conn = pymysql.connect(**DB)
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 查询该栏目所有使用默认占位图的文章
        # 包含该栏目 ID 及其所有二级子栏目
        sql_select = """
            SELECT id, title, class1
            FROM ep_news
            WHERE recycle=0
            AND (class1 = %s OR class1 IN (
                SELECT id FROM ep_column
                WHERE bigclass = %s
            ))
            AND imgurl LIKE '%%epgo-covers%%'
            LIMIT 1000
        """
        cur.execute(sql_select, (category_id, category_id))
        rows = cur.fetchall()

        if not rows:
            log.info("  栏目 %d 没有需要更新的文章", category_id)
            return 0

        count = 0
        if not dry_run:
            sql_update = "UPDATE ep_news SET imgurl=%s WHERE id=%s"
            for row in rows:
                cur.execute(sql_update, (web_url, row["id"]))
                count += 1
            conn.commit()
        else:
            count = len(rows)

        log.info("  将更新 %d 篇文章的封面", count)
        return count
    finally:
        cur.close()
        conn.close()


# ─── 主流程 ───────────────────────────────────────────────

def process_categories(dry_run=False):
    """
    为每个栏目下载和配置封面
    """
    log.info("=" * 60)
    log.info("英语教育栏目封面爬取与配置")
    log.info("=" * 60)

    if dry_run:
        log.warning("⚠ 预览模式，不会实际下载或更新")

    total_success = 0

    for cat_id, (folder_name, url, desc) in CATEGORY_COVERS.items():
        log.info("")
        log.info("[栏目 %d] %s", cat_id, desc)
        log.info("  图片URL: %s", url[:70] + "...")

        # 准备远程路径
        filename = f"cover_{int(time.time())}.jpg"
        remote_path = f"{UPLOAD_DIR}/{folder_name}/{filename}"
        web_url = f"/upload/epgo-photo-covers/{folder_name}/{filename}"

        # 步骤1: 远程下载
        if not dry_run:
            if not download_on_remote(url, remote_path):
                log.warning("  跳过该栏目")
                continue
        else:
            log.info("  [DRY] 将下载到: %s", remote_path)

        # 步骤2: 更新数据库
        log.info("  更新数据库...")
        updated = update_articles_cover(cat_id, web_url, dry_run=dry_run)

        if updated > 0 or dry_run:
            total_success += 1
            log.info("  ✓ 栏目 %d 处理完成 (%d 篇文章)", cat_id, updated)

        time.sleep(1)  # 避免请求过快

    log.info("")
    log.info("=" * 60)
    log.info("✅ 完成！共处理 %d 个栏目", total_success)
    if not dry_run:
        log.info("👉 访问 %s 查看效果", SITE_URL)
        log.info("💾 所有封面已保存到: %s", UPLOAD_DIR)
    log.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="为英语教育栏目下载并配置专业封面图"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="预览模式，不实际下载或修改数据库")
    args = parser.parse_args()

    process_categories(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
