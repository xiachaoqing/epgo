#!/usr/bin/env python3
import pymysql

DB = dict(host="127.0.0.1", port=3306, user="xiachaoqing", password="***REMOVED***", database="epgo_db", charset="utf8mb4")

conn = pymysql.connect(**DB)
cur = conn.cursor()

print("=== 各种查询方式的结果 ===")

# 方式1：class2=121
cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND class2=121")
print(f"class2=121: {cur.fetchone()[0]} 篇")

# 方式2：class1=121 AND class2=0
cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND class1=121 AND class2=0")
print(f"class1=121 AND class2=0: {cur.fetchone()[0]} 篇")

# 方式3：class1=102 AND class2=121
cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND class1=102 AND class2=121")
print(f"class1=102 AND class2=121: {cur.fetchone()[0]} 篇")

cur.close()
conn.close()
