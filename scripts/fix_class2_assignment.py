#!/usr/bin/env python3
"""
修复文章的 class2（二级栏目）分配
"""
import pymysql
import random

DB = dict(
    host="127.0.0.1", port=3306,
    user="xiachaoqing", password="***REMOVED***",
    database="epgo_db", charset="utf8mb4"
)

# 栏目映射：class1 -> [class2_list]
CATEGORY_MAP = {
    101: [111, 112, 113, 114],      # KET
    102: [121, 122, 123, 124],      # PET
    103: [],                         # 英语阅读（无子栏目）
    104: [],                         # 英语演讲（无子栏目）
    105: [],                         # 每日英语（无子栏目）
    106: [],                         # 资料下载（无子栏目）
    107: [],                         # 关于我们（无子栏目）
}

conn = pymysql.connect(**DB)
cur = conn.cursor()

# 对于有子栏目的主栏目，把 class2=0 的文章分散到各个子栏目
for class1, class2_list in CATEGORY_MAP.items():
    if not class2_list:
        continue

    # 查出这个 class1 中 class2=0 的文章
    cur.execute(f"SELECT id FROM ep_news WHERE recycle=0 AND class1={class1} AND class2=0 ORDER BY id")
    articles = [row[0] for row in cur.fetchall()]

    print(f"\n类别 {class1}: 找到 {len(articles)} 篇无子栏目的文章，将分散到 {class2_list}")

    # 轮流分配到各个子栏目
    for i, article_id in enumerate(articles):
        target_class2 = class2_list[i % len(class2_list)]
        cur.execute(f"UPDATE ep_news SET class2={target_class2} WHERE id={article_id}")
        if (i + 1) % 10 == 0:
            print(f"  已处理 {i+1}/{len(articles)}")

conn.commit()

# 验证结果
print("\n\n=== 修复后的分布 ===")
for class1 in [101, 102]:
    cur.execute(f"""
        SELECT class2, COUNT(*)
        FROM ep_news
        WHERE recycle=0 AND class1={class1}
        GROUP BY class2
        ORDER BY class2
    """)
    results = cur.fetchall()
    for class2, cnt in results:
        class2_name = {
            111: 'KET真题', 112: 'KET词汇', 113: 'KET写作', 114: 'KET听力',
            121: 'PET真题', 122: 'PET词汇', 123: 'PET写作', 124: 'PET阅读'
        }.get(class2, '其他')
        print(f"  class1={class1}, class2={class2} ({class2_name}): {cnt} 篇")

cur.close()
conn.close()

print("\n✓ 二级栏目分配已完成")
