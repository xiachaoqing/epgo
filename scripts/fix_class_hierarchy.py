#!/usr/bin/env python3
"""
修复栏目分配 - 把 class1=111-124 的文章改成正确的 class1, class2
"""
import pymysql

DB = dict(
    host="127.0.0.1", port=3306,
    user="xiachaoqing", password="Xia@07090218",
    database="epgo_db", charset="utf8mb4"
)

# 子栏目 -> 父栏目的映射
SUBCATEGORY_TO_PARENT = {
    111: 101,  # KET真题解析 -> KET备考
    112: 101,  # KET词汇速记 -> KET备考
    113: 101,  # KET写作指导 -> KET备考
    114: 101,  # KET听力技巧 -> KET备考
    121: 102,  # PET真题解析 -> PET备考
    122: 102,  # PET词汇速记 -> PET备考
    123: 102,  # PET写作指导 -> PET备考
    124: 102,  # PET阅读技巧 -> PET备考
}

conn = pymysql.connect(**DB)
cur = conn.cursor()

total_fixed = 0

# 对每个子栏目，把 class1=XXX 的文章改成 class1=PARENT, class2=XXX
for child_id, parent_id in SUBCATEGORY_TO_PARENT.items():
    cur.execute(f"""
        UPDATE ep_news
        SET class1={parent_id}, class2={child_id}
        WHERE recycle=0 AND class1={child_id} AND class2=0
    """)
    affected = cur.rowcount
    total_fixed += affected
    print(f"  class1={child_id} -> class1={parent_id}, class2={child_id}: {affected} 篇")

conn.commit()

print(f"\n总共修复: {total_fixed} 篇文章")

# 验证结果
print("\n=== 修复后的结构 ===")
for parent_id in [101, 102]:
    parent_names = {101: 'KET备考', 102: 'PET备考'}
    print(f"\n{parent_names[parent_id]} (class1={parent_id}):")

    cur.execute(f"""
        SELECT class2, COUNT(*)
        FROM ep_news
        WHERE recycle=0 AND class1={parent_id}
        GROUP BY class2
        ORDER BY class2
    """)

    for class2, cnt in cur.fetchall():
        if class2 == 0:
            print(f"  class2=0 (无子栏目): {cnt} 篇")
        else:
            sub_names = {
                111: 'KET真题', 112: 'KET词汇', 113: 'KET写作', 114: 'KET听力',
                121: 'PET真题', 122: 'PET词汇', 123: 'PET写作', 124: 'PET阅读'
            }
            print(f"  class2={class2} ({sub_names.get(class2, '?')}): {cnt} 篇")

cur.close()
conn.close()

print("\n✓ 栏目分配修复完成")
