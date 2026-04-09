#!/usr/bin/env python3
"""
修复首页图片显示问题
原因：数据库中的文件名与服务器上的实际文件名不匹配
解决：扫描真实存在的文件，更新数据库中的路径
"""

import pymysql
import os
import subprocess

DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="***REMOVED***",
    database="epgo_db",
    charset="utf8mb4"
)

# 图片目录映射
CATEGORY_DIRS = {
    101: "ket",
    102: "pet",
    103: "reading",
    104: "speech",
    105: "daily",
    106: "download",
    107: "about",
    111: "ket",
    112: "ket",
    113: "ket",
    114: "ket",
    121: "pet",
    122: "pet",
    123: "pet",
    124: "pet",
}

UPLOAD_BASE = "/www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers"

def get_available_covers():
    """扫描服务器上真实存在的图片文件"""
    covers = {}
    for class_id, dir_name in CATEGORY_DIRS.items():
        dir_path = os.path.join(UPLOAD_BASE, dir_name)
        if os.path.exists(dir_path):
            files = [f for f in os.listdir(dir_path) if f.endswith('.jpg')]
            files.sort()
            covers[class_id] = [f"/upload/epgo-photo-covers/{dir_name}/{f}" for f in files]
    return covers

def fix_article_covers(conn, available_covers):
    """修复数据库中的图片路径"""
    print("=" * 60)
    print("开始修复文章封面")
    print("=" * 60)

    cur = conn.cursor()

    # 查出所有文章
    cur.execute("""
        SELECT id, class1, class2 FROM ep_news
        WHERE recycle=0
        ORDER BY id
    """)
    articles = cur.fetchall()

    updated = 0
    skipped = 0

    for article_id, class1, class2 in articles:
        # 确定分类（二级优先）
        cover_class = class2 if class2 > 0 else class1

        # 如果分类没有配置，使用 class1
        if cover_class not in available_covers:
            cover_class = class1

        if cover_class not in available_covers or not available_covers[cover_class]:
            print(f"⊘ ID {article_id}: 没有找到分类 {cover_class} 的可用封面")
            skipped += 1
            continue

        # 轮转选择封面
        covers = available_covers[cover_class]
        cover_idx = article_id % len(covers)
        new_cover = covers[cover_idx]

        # 更新数据库
        cur.execute(
            "UPDATE ep_news SET imgurl=%s WHERE id=%s",
            (new_cover, article_id)
        )
        updated += 1

        if updated % 50 == 0:
            print(f"已更新 {updated} 篇")

    conn.commit()
    print(f"\n✓ 封面修复完成：共更新 {updated} 篇，跳过 {skipped} 篇")

    cur.close()

def clear_cache():
    """清理缓存"""
    print("\n清理缓存...")
    subprocess.run("rm -rf /www/wwwroot/go.xiachaoqing.com/cache/* 2>/dev/null", shell=True)
    subprocess.run("rm -rf /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/cache/* 2>/dev/null", shell=True)
    subprocess.run("find /www/wwwroot/go.xiachaoqing.com -name '*.html' -delete 2>/dev/null", shell=True)
    print("✓ 缓存已清理")

def main():
    print("\n" + "=" * 60)
    print("epgo 首页图片修复脚本")
    print("=" * 60 + "\n")

    # 扫描可用的图片
    print("扫描服务器上的实际图片文件...")
    available_covers = get_available_covers()

    for class_id in sorted(available_covers.keys()):
        count = len(available_covers[class_id])
        print(f"  class {class_id}: {count} 张图片")

    print("\n")

    # 连接数据库并修复
    conn = pymysql.connect(**DB)

    try:
        fix_article_covers(conn, available_covers)
        clear_cache()

        # 统计
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0")
        total = cur.fetchone()[0]
        cur.close()

        print("\n" + "=" * 60)
        print(f"修复完成！总计 {total} 篇文章")
        print("=" * 60 + "\n")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
