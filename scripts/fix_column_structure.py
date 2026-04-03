# -*- coding: utf-8 -*-
"""
数据库诊断和修复脚本
处理栏目结构、Logo显示、404页面等问题
"""
import pymysql
from datetime import datetime

# 连接数据库
db = pymysql.connect(
    host="localhost",
    port=3306,
    user="xiachaoqing",
    password="***REMOVED***",
    db="epgo_db",
    charset="utf8"
)
cur = db.cursor(pymysql.cursors.DictCursor)
cur.execute("SET NAMES utf8")

print("=" * 60)
print("EPGO 栏目结构诊断和修复")
print("=" * 60)
print()

# ========== 1. 查询现有栏目结构 ==========
print("1. 查询现有栏目结构...")
print("-" * 60)

sql = """SELECT id, name, classtype, nav, isshow, bigclass
         FROM ep_column
         WHERE lang='cn'
         ORDER BY classtype, bigclass, no_order, id"""
cur.execute(sql)
all_columns = cur.fetchall()

print(f"总栏目数: {len(all_columns)}\n")

# 分类显示
first_level = [c for c in all_columns if c['bigclass'] == 0 and c['classtype'] == 1]
second_level = [c for c in all_columns if c['bigclass'] > 0 and c['classtype'] == 2]

print("一级栏目:")
for col in first_level:
    print(f"  [{col['id']}] {col['name']:<20} nav={col['nav']}, show={col['isshow']}, type={col['classtype']}")

print("\n二级栏目:")
for col in second_level:
    print(f"  [{col['id']}] {col['name']:<20} parent={col['bigclass']}, nav={col['nav']}, show={col['isshow']}, type={col['classtype']}")

# ========== 2. 检查Logo设置 ==========
print("\n" + "=" * 60)
print("2. 检查Logo和网站配置...")
print("-" * 60)

sql = "SELECT name, value FROM ep_config WHERE lang='cn' AND name IN ('met_logo', 'met_webname', 'met_404content')"
cur.execute(sql)
configs = cur.fetchall()

for cfg in configs:
    value = cfg['value'][:50] if cfg['value'] else "未设置"
    print(f"  {cfg['name']}: {value}")

# ========== 3. 检查文章分布 ==========
print("\n" + "=" * 60)
print("3. 检查各栏目文章数量...")
print("-" * 60)

sql = """SELECT classid, COUNT(*) as cnt
         FROM ep_news
         WHERE lang='cn'
         GROUP BY classid
         ORDER BY cnt DESC"""
cur.execute(sql)
news_count = cur.fetchall()

for news in news_count:
    # 查找栏目名
    sql_name = "SELECT name FROM ep_column WHERE id = %s"
    cur.execute(sql_name, (news['classid'],))
    col_name_result = cur.fetchone()
    col_name = col_name_result['name'] if col_name_result else f"未知[{news['classid']}]"
    print(f"  [{news['classid']}] {col_name:<20}: {news['cnt']} 篇")

# ========== 4. 开始修复 ==========
print("\n" + "=" * 60)
print("4. 执行修复操作...")
print("-" * 60)

# 修复4a: 确保所有子栏目的classtype=2, nav=0, isshow=1
print("\n修复4a: 调整二级栏目 (classtype=2, nav=0, isshow=1)...")
sql = """UPDATE ep_column
         SET classtype=2, nav=0, isshow=1
         WHERE lang='cn' AND bigclass > 0"""
cur.execute(sql)
db.commit()
print(f"  ✓ 受影响行数: {cur.rowcount}")

# 修复4b: 确保一级栏目 classtype=1, isshow=1
print("\n修复4b: 调整一级栏目 (classtype=1, isshow=1)...")
sql = """UPDATE ep_column
         SET classtype=1, isshow=1
         WHERE lang='cn' AND bigclass=0 AND classtype <> 1"""
cur.execute(sql)
db.commit()
print(f"  ✓ 受影响行数: {cur.rowcount}")

# 修复4c: 导航栏只显示一级栏目
print("\n修复4c: 配置导航显示 (一级nav=1, 二三级nav=0)...")
sql = """UPDATE ep_column
         SET nav=1
         WHERE lang='cn' AND classtype=1 AND bigclass=0 AND isshow=1"""
cur.execute(sql)
db.commit()
nav_first = cur.rowcount
print(f"  ✓ 一级栏目导航设置: {nav_first}")

sql = """UPDATE ep_column
         SET nav=0
         WHERE lang='cn' AND (classtype=2 OR classtype=3)"""
cur.execute(sql)
db.commit()
nav_second = cur.rowcount
print(f"  ✓ 二三级栏目导航关闭: {nav_second}")

# 修复4d: 确保404内容存在
print("\n修复4d: 检查404页面内容...")
sql = "SELECT value FROM ep_config WHERE lang='cn' AND name='met_404content'"
cur.execute(sql)
result = cur.fetchone()
if not result or not result['value']:
    print("  ⚠ 404内容为空，设置默认内容...")
    default_404 = """<div style="text-align:center;padding:60px 20px;">
    <h1 style="font-size:72px;color:#1565C0;margin:20px 0;font-weight:800;">404</h1>
    <h2 style="font-size:24px;color:#333;margin:20px 0;">页面不存在</h2>
    <p style="color:#666;margin-bottom:30px;font-size:16px;">抱歉，您访问的页面已被删除或地址不正确</p>
    <a href="/" style="display:inline-block;background:#1565C0;color:white;padding:12px 32px;border-radius:6px;text-decoration:none;font-weight:600;">返回首页</a>
</div>"""
    sql = "UPDATE ep_config SET value=%s WHERE lang='cn' AND name='met_404content'"
    cur.execute(sql, (default_404,))
    db.commit()
    print("  ✓ 已设置默认404内容")
else:
    print("  ✓ 404内容已存在")

# ========== 5. 验证修复结果 ==========
print("\n" + "=" * 60)
print("5. 验证修复结果...")
print("-" * 60)

sql = """SELECT id, name, classtype, nav, isshow, bigclass
         FROM ep_column
         WHERE lang='cn'
         ORDER BY classtype, bigclass, no_order, id"""
cur.execute(sql)
all_columns_fixed = cur.fetchall()

print("\n修复后的栏目结构:")
for col in all_columns_fixed:
    if col['bigclass'] == 0:  # 一级
        print(f"✓ [{col['id']}] {col['name']:<20} (一级, nav={col['nav']}, show={col['isshow']})")
    else:  # 二级
        print(f"  └─ [{col['id']}] {col['name']:<15} (二级, nav={col['nav']}, show={col['isshow']})")

# ========== 6. Logo检查 ==========
print("\n" + "=" * 60)
print("6. Logo配置检查...")
print("-" * 60)

sql = "SELECT value FROM ep_config WHERE lang='cn' AND name='met_logo' LIMIT 1"
cur.execute(sql)
logo_result = cur.fetchone()
if logo_result and logo_result['value']:
    print(f"  ✓ Logo已配置: {logo_result['value']}")
else:
    print("  ⚠ Logo未配置！请在后台系统设置中上传Logo图片")
    print("    路径: 系统 → 系统设置 → 基本信息 → 上传LOGO")

# ========== 7. 输出清缓存指令 ==========
print("\n" + "=" * 60)
print("7. 缓存清理指令（在服务器执行）...")
print("-" * 60)

cache_commands = """
sudo -u www bash -c 'rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/'
sudo -u www bash -c 'rm -f /www/wwwroot/go.xiachaoqing.com/cache/column_cn.php'
sudo -u www bash -c 'mkdir -p /www/wwwroot/go.xiachaoqing.com/cache/templates'
sudo -u www bash -c 'chown -R www:www /www/wwwroot/go.xiachaoqing.com/cache'
"""

print(cache_commands)

print("\n" + "=" * 60)
print("修复完成！")
print("=" * 60)
print("\n✓ 数据库修复已完成")
print("✓ 请执行上述缓存清理命令")
print("✓ 访问网站检查效果")
print()

db.close()
