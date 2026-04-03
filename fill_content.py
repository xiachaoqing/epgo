#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EPGO 内容自动化填充脚本 v1.1
自动在MetInfo数据库中填充:
- 关于我们: 8篇文章
- 资料下载: 20个资源
- 随机阅读量

该脚本需要在服务器上运行或需要正确的数据库连接配置。

使用方法:
    1. 在服务器上执行: python3 fill_content.py
    2. 或在本地配置远程数据库连接

配置说明:
    修改DB_CONFIG字典中的主机地址、用户名、密码等信息
"""

import pymysql
import random
import datetime
import json
import sys
from typing import Dict, List, Tuple

# ==================== 配置信息 ====================
# 请根据实际情况修改以下配置

# 方案1: 连接远程服务器 (推荐在服务器上运行)
DB_CONFIG = {
    'host': 'localhost',        # 如果在服务器上运行，改为 'localhost'
    'port': 3306,
    'user': 'xiachaoqing',
    'password': '***REMOVED***',
    'database': 'epgo_db',
    'charset': 'utf8mb4'
}

# 方案2: 如果需要连接远程服务器，可以使用以下配置
# DB_CONFIG = {
#     'host': '101.42.21.191',    # 改为服务器IP
#     'port': 3306,
#     'user': 'xiachaoqing',
#     'password': '***REMOVED***',
#     'database': 'epgo_db',
#     'charset': 'utf8mb4'
# }

print("=" * 80)
print("🚀 EPGO 内容自动化填充脚本 v1.1")
print("=" * 80)
print(f"\n📌 数据库配置:")
print(f"   主机: {DB_CONFIG['host']}")
print(f"   端口: {DB_CONFIG['port']}")
print(f"   用户: {DB_CONFIG['user']}")
print(f"   数据库: {DB_CONFIG['database']}")

# ==================== 数据库连接 ====================
def get_db_connection():
    """获取数据库连接"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("\n✅ 数据库连接成功")
        return conn
    except Exception as e:
        print(f"\n❌ 数据库连接失败: {e}")
        print("\n💡 提示:")
        print("   1. 请确保MySQL服务已启动")
        print("   2. 请检查数据库连接配置是否正确")
        print("   3. 如果在本地运行，请将脚本上传到服务器上执行")
        sys.exit(1)

# ==================== 获取栏目ID ====================
def get_column_id(conn, column_name: str) -> int:
    """根据栏目名称获取栏目ID"""
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id FROM ep_column WHERE name = %s LIMIT 1"
            cursor.execute(sql, (column_name,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                print(f"⚠️  栏目 '{column_name}' 不存在")
                # 尝试显示所有栏目
                cursor.execute("SELECT id, name FROM ep_column LIMIT 20")
                columns = cursor.fetchall()
                if columns:
                    print("\n   现有栏目:")
                    for col_id, col_name in columns:
                        print(f"     - ID:{col_id}, 名称: {col_name}")
                return None
    except Exception as e:
        print(f"❌ 获取栏目ID失败: {e}")
        return None

# ==================== 关于我们 - 8篇文章数据 ====================
ABOUT_US_ARTICLES = [
    {
        'title': '关于EPGO - 我们的故事',
        'hits': 1200,
        'content': '''<h2>我们是谁</h2>
<p>英语陪跑GO（EPGO）是一个致力于帮助中学生高效备考剑桥英语的在线教育平台。我们由多名英语教育专家组成，拥有15年以上的一线教学经验和考试研究积累。</p>
<p>自2025年成立以来，我们已经帮助超过10,000名学生在剑桥英语KET/PET考试中取得优异成绩，其中98%的学生在首次参加考试时就成功通过，获得了学生和家长的一致好评。</p>
<h2>我们的使命</h2>
<p><strong>使命</strong>: 让英语学习变得简单、有趣、高效</p>
<p>我们坚信，每个学生都有成功的潜力。学好英语不是为了应付考试，而是为了打开一扇通往世界的大门。</p>''',
        'summary': '英语陪跑GO是一个致力于帮助中学生高效备考剑桥英语的在线教育平台。',
        'keywords': 'EPGO,在线英语,剑桥英语'
    },
    {
        'title': '我们的教学理念 - 用爱教学',
        'hits': 890,
        'content': '<h2>四个核心理念</h2><p>EPGO的教学理念可以概括为四个字：<strong>专业、趣味、高效、个性</strong>。</p>',
        'summary': 'EPGO的教学理念强调专业、趣味、高效、个性。',
        'keywords': '教学理念,学习方法'
    },
    {
        'title': '师资力量 - 我们的教学团队',
        'hits': 1540,
        'content': '<h2>核心成员介绍</h2><p>EPGO拥有一支由英语教育专家、资深讲师和考试研究员组成的强大师资队伍。</p>',
        'summary': 'EPGO的师资队伍由英语教育硕士、考试研究员和资深讲师组成。',
        'keywords': '师资力量,教学团队'
    },
    {
        'title': '成功案例 - 他们在EPGO获得成功',
        'hits': 2350,
        'content': '<h2>案例分享</h2><p>4位同学通过EPGO的学习，从零基础到高分通过考试。</p>',
        'summary': '4位同学通过EPGO的学习，从零基础到高分通过。',
        'keywords': '成功案例,学员故事'
    },
    {
        'title': '为什么选择EPGO - 10个理由',
        'hits': 1680,
        'content': '<h2>选择理由</h2><p>选择EPGO的10个理由：专业师资、完整课程、高通过率、灵活学习、亲民价格等。</p>',
        'summary': '选择EPGO的10个理由。',
        'keywords': '选择EPGO,优势'
    },
    {
        'title': '教学方法论 - 如何科学地学习英语',
        'hits': 1420,
        'content': '<h2>四步学习法</h2><p>EPGO独创的四步学习法：输入、吸收、应用、输出。</p>',
        'summary': '科学的四步学习法让英语学习更有效。',
        'keywords': '学习方法,四步学习法'
    },
    {
        'title': '平台的发展里程碑',
        'hits': 950,
        'content': '<h2>发展历程</h2><p>EPGO从2025年成立至今，已经帮助10000+学生成功。</p>',
        'summary': 'EPGO发展成为行业领先的在线英语教育平台。',
        'keywords': '发展历程,平台成就'
    },
    {
        'title': '联系与合作',
        'hits': 680,
        'content': '<h2>联系我们</h2><p>电话: 176-1072-1765 工作日9:00-18:00</p>',
        'summary': '联系EPGO获得专业咨询，欢迎合作。',
        'keywords': '联系我们,合作'
    }
]

# ==================== 资料下载 - 20个资源数据 ====================
DOWNLOAD_RESOURCES = [
    # 考试指南类
    {'title': 'KET备考完全指南', 'hits': 1240, 'summary': '系统介绍KET考试内容、题型分析、高分策略'},
    {'title': 'PET备考完全指南', 'hits': 980, 'summary': '完整的PET考试备考指南'},
    {'title': '剑桥英语等级认证解读', 'hits': 650, 'summary': '剑桥英语各等级认证的详细介绍'},
    {'title': '2026年考试时间安排表', 'hits': 2150, 'summary': '2026年全年KET/PET考试日期安排'},

    # 词汇资源类
    {'title': 'KET核心词汇表 (1500词)', 'hits': 3280, 'summary': '完整词汇表包含音标和例句'},
    {'title': 'PET核心词汇表 (3000词)', 'hits': 2540, 'summary': 'PET考试必备的3000个核心词汇'},
    {'title': '常用短语搭配宝典', 'hits': 1890, 'summary': '500+组常用短语搭配详解'},
    {'title': '易混词汇对比 (100组)', 'hits': 1650, 'summary': '学生容易混淆的词汇对比分析'},

    # 语法资料类
    {'title': '英语时态完全解析', 'hits': 2470, 'summary': '12种英语时态详细讲解和用法'},
    {'title': '语态转换详解', 'hits': 1340, 'summary': '主动和被动语态转换详细指导'},
    {'title': '从句系统讲解', 'hits': 1620, 'summary': '名词/形容词/状语从句系统讲解'},
    {'title': '常见语法错误100例', 'hits': 2340, 'summary': '学生常见的100个语法错误分析'},

    # 技能提升类
    {'title': '听力技巧秘籍', 'hits': 2890, 'summary': '听力考试技巧详解，包含30个音频示范'},
    {'title': '口语表达模板库', 'hits': 2100, 'summary': '50+个日常和考试口语表达模板'},
    {'title': '阅读加速技巧', 'hits': 1780, 'summary': '阅读快速定位和理解技巧训练'},
    {'title': '写作范文精选 (50篇)', 'hits': 2560, 'summary': '各题材范文50篇，含详细分析'},

    # 学习工具类
    {'title': 'KET模拟试卷 (5套)', 'hits': 3450, 'summary': '5套完整KET模拟卷，附详细答案解析'},
    {'title': 'PET模拟试卷 (5套)', 'hits': 2680, 'summary': '5套完整PET模拟卷，附详细答案解析'},
    {'title': '学习进度追踪表', 'hits': 1920, 'summary': 'Excel格式的学习进度管理工具'},
    {'title': '每日学习计划模板', 'hits': 1650, 'summary': 'Excel格式的每日学习计划制定工具'}
]

# ==================== 插入文章函数 ====================
def insert_articles(conn, column_id: int, articles: List[Dict]) -> Tuple[int, int]:
    """批量插入文章"""
    success_count = 0
    fail_count = 0

    with conn.cursor() as cursor:
        for idx, article in enumerate(articles, 1):
            try:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                sql = """
                INSERT INTO ep_news (cid, title, content, summary, keywords, addtime, hits, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                """

                cursor.execute(sql, (
                    column_id,
                    article['title'],
                    article['content'],
                    article['summary'],
                    article['keywords'],
                    now,
                    article['hits']
                ))

                print(f"  ✅ [{idx}/8] {article['title']} - 阅读量: {article['hits']}")
                success_count += 1

            except Exception as e:
                print(f"  ❌ [{idx}/8] {article['title']} 插入失败: {e}")
                fail_count += 1

    conn.commit()
    return success_count, fail_count

# ==================== 插入资源函数 ====================
def insert_resources(conn, column_id: int, resources: List[Dict]) -> Tuple[int, int]:
    """批量插入资源"""
    success_count = 0
    fail_count = 0

    with conn.cursor() as cursor:
        for idx, resource in enumerate(resources, 1):
            try:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                sql = """
                INSERT INTO ep_news (cid, title, content, summary, keywords, addtime, hits, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                """

                cursor.execute(sql, (
                    column_id,
                    resource['title'],
                    resource['summary'],
                    resource['summary'],
                    '资源下载',
                    now,
                    resource['hits']
                ))

                print(f"  ✅ [{idx}/20] {resource['title']} - 下载量: {resource['hits']}")
                success_count += 1

            except Exception as e:
                print(f"  ❌ [{idx}/20] {resource['title']} 插入失败: {e}")
                fail_count += 1

    conn.commit()
    return success_count, fail_count

# ==================== 主程序 ====================
def main():
    conn = get_db_connection()

    try:
        print("\n" + "="*80)
        print("📝 第1步: 获取栏目ID")
        print("="*80)

        # 获取栏目ID
        about_us_id = get_column_id(conn, '关于我们')
        if not about_us_id:
            about_us_id = get_column_id(conn, 'About Us')
        if not about_us_id:
            about_us_id = 6  # 默认假设ID为6

        download_id = get_column_id(conn, '资料下载')
        if not download_id:
            download_id = get_column_id(conn, 'Download')
        if not download_id:
            download_id = 7  # 默认假设ID为7

        print(f"✅ 关于我们 (ID: {about_us_id})")
        print(f"✅ 资料下载 (ID: {download_id})")

        # 填充关于我们
        print("\n" + "="*80)
        print("📝 第2步: 填充'关于我们'栏目 (8篇文章)")
        print("="*80)

        about_success, about_fail = insert_articles(conn, about_us_id, ABOUT_US_ARTICLES)
        print(f"\n📊 关于我们统计: ✅ 成功 {about_success} 篇, ❌ 失败 {about_fail} 篇")

        # 填充资料下载
        print("\n" + "="*80)
        print("📥 第3步: 填充'资料下载'栏目 (20个资源)")
        print("="*80)

        download_success, download_fail = insert_resources(conn, download_id, DOWNLOAD_RESOURCES)
        print(f"\n📊 资料下载统计: ✅ 成功 {download_success} 个, ❌ 失败 {download_fail} 个")

        # 最终总结
        print("\n" + "="*80)
        print("🎉 内容填充完成总结")
        print("="*80)

        total_success = about_success + download_success
        total_fail = about_fail + download_fail

        print(f"\n总计:")
        print(f"  ✅ 成功: {total_success} 项")
        print(f"  ❌ 失败: {total_fail} 项")
        print(f"  📊 总计: {total_success + total_fail} 项")

        if total_fail == 0:
            print("\n🎊 所有内容填充成功！")
            print("\n📌 后续步骤:")
            print("  1. 访问后台清除缓存: 系统设置 → 缓存管理")
            print("  2. 在首页验证新内容是否显示")
            print("  3. 检查阅读量是否正确显示")
            print("  4. 测试移动端显示效果")
            return True
        else:
            print(f"\n⚠️  有 {total_fail} 项填充失败")
            return False

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        return False

    finally:
        conn.close()
        print("\n✅ 数据库连接已关闭")

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 致命错误: {e}")
        sys.exit(1)
