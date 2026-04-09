#!/usr/bin/env python3
"""
epgo 网站日常维护脚本（统一版）
- 合并原有的两个日常脚本
- 增加数据质量检查
- 随机化时间戳
- 自动清理缓存

运行：crontab 0 2 * * * python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py
"""

import pymysql
import random
import subprocess
import logging
from datetime import datetime, timedelta

# 配置数据库
DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="***REMOVED***",
    database="epgo_db",
    charset="utf8mb4"
)

# 配置日志
LOG_FILE = "/www/wwwroot/go.xiachaoqing.com/logs/daily_maintain.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 每个栏目的文章轮转主题
ARTICLE_TOPICS = {
    103: [  # 英语阅读
        ("英语阅读技巧：校园生活主题短文精读", "围绕校园生活场景训练略读、扫读与细节定位能力"),
        ("英语阅读技巧：科技生活主题短文精读", "聚焦科技生活高频主题，帮助学习者积累阅读策略"),
        ("英语阅读技巧：环保主题文章快速理解", "通过环保主题阅读练习，提升主旨判断与细节提取能力"),
    ],
    104: [  # 英语演讲
        ("英语演讲表达：校园话题开场白训练", "聚焦校园演讲话题，整理开场、过渡和收尾表达"),
        ("英语演讲技巧：如何让表达更有条理", "从结构设计到连接词使用，帮助演讲更清晰自然"),
        ("英语演讲范文：梦想与成长主题", "提供适合学生练习的演讲范文与表达积累"),
    ],
    105: [  # 每日英语
        ("每日英语 | 今日表达：描述计划与安排", "学习日常中最常用的计划类英语表达"),
        ("每日英语 | 今日表达：鼓励与赞美怎么说", "积累在学习和生活中常用的鼓励表达"),
        ("每日英语 | 今日表达：课堂互动常用句", "掌握课堂提问、回答和讨论中的高频句型"),
    ],
    106: [  # 资料下载
        ("KET/PET历年真题集合下载指南", "整理各年份KET和PET官方真题，帮助系统备考"),
        ("英语学习必备参考书推荐与获取方式", "精选高质量参考书籍，支持在线预览和下载"),
    ],
    107: [  # 关于我们
        ("英语陪跑GO平台简介与使用指南", "了解平台功能、栏目设置和学习路径"),
        ("用户常见问题解答与技术支持", "快速解决使用过程中遇到的各类问题"),
    ],
    111: [  # KET真题
        ("KET真题解析：Reading Part 1 题型训练", "拆解KET Reading Part 1常见设问与解题步骤"),
        ("KET真题解析：Writing Part 7 高分思路", "梳理KET写作题的要点覆盖与语言组织方法"),
    ],
    112: [  # KET词汇
        ("KET词汇速记：学校生活高频词", "围绕学校生活场景整理KET高频核心词汇"),
        ("KET词汇速记：日常交流必背表达", "补充考试和日常都高频出现的词组与短语"),
    ],
    113: [  # KET写作
        ("KET写作指导：邮件写作开头与结尾", "整理KET邮件写作中稳定可用的开头和结尾模板"),
        ("KET写作指导：常见失分点专项纠错", "聚焦语法、拼写和逻辑问题，避免低级失分"),
    ],
    114: [  # KET听力
        ("KET听力技巧：图片题关键词捕捉", "训练KET听力图片题中的关键信息定位能力"),
        ("KET听力技巧：数字时间题快速判断", "掌握时间、日期、价格等高频信息的听辨方法"),
    ],
    121: [  # PET真题
        ("PET真题解析：Reading Part 3 长文策略", "拆解PET长文阅读中的定位与排除方法"),
        ("PET真题解析：Listening Part 2 关键信息训练", "围绕PET听力Part 2常考信息进行专项分析"),
    ],
    122: [  # PET词汇
        ("PET词汇速记：B1校园主题高频词", "梳理B1阶段常见校园主题词汇及短语搭配"),
        ("PET词汇速记：生活方式主题核心表达", "补充PET考试中常见生活方式和习惯表达"),
    ],
    123: [  # PET写作
        ("PET写作指导：邮件回复结构模板", "整理PET邮件回复类写作的稳定结构与表达"),
        ("PET写作指导：议论文常用连接词", "帮助写作时更自然地组织观点和论据"),
    ],
    124: [  # PET阅读
        ("PET阅读技巧：同义替换快速识别", "围绕阅读题中的同义替换进行专项训练"),
        ("PET阅读技巧：主旨题与细节题区分方法", "帮助学习者更快识别题目要求和答题路径"),
    ],
}

# 栏目与类别映射
CATEGORY_MAP = {
    101: (101, 0),   # KET备考 (无子栏目)
    102: (102, 0),   # PET备考 (无子栏目)
    103: (103, 0),   # 英语阅读
    104: (104, 0),   # 英语演讲
    105: (105, 0),   # 每日英语
    106: (106, 0),   # 资料下载
    107: (107, 0),   # 关于我们
    111: (101, 111), # KET真题 (属于101)
    112: (101, 112), # KET词汇 (属于101)
    113: (101, 113), # KET写作 (属于101)
    114: (101, 114), # KET听力 (属于101)
    121: (102, 121), # PET真题 (属于102)
    122: (102, 122), # PET词汇 (属于102)
    123: (102, 123), # PET写作 (属于102)
    124: (102, 124), # PET阅读 (属于102)
}

def get_random_timestamp():
    """生成过去7-30天内的随机时间"""
    days_back = random.randint(7, 30)
    hours_back = random.randint(0, 23)
    minutes_back = random.randint(0, 59)
    dt = datetime.now() - timedelta(days=days_back, hours=hours_back, minutes=minutes_back)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def generate_article_content(title, description):
    """生成标准的文章内容"""
    content = f"""<p>{description}</p>
<h3>学习重点</h3>
<ul>
  <li>明确本篇主题中的高频表达和关键词</li>
  <li>结合题型或场景理解表达的实际使用方式</li>
  <li>完成一轮复盘，整理自己的错题和笔记</li>
</ul>
<h3>练习建议</h3>
<p>建议把本文内容和既有学习资料配套使用，先阅读理解，再做关键词提取，最后尝试复述或写出自己的总结。</p>
<p>每天坚持一篇小专题，长期积累后会明显提升阅读、写作或考试表现。</p>"""
    return content

def check_duplicate(conn, class1, class2, title):
    """检查是否已存在相同文章"""
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM ep_news WHERE recycle=0 AND class1=%s AND class2=%s AND title=%s LIMIT 1",
        (class1, class2, title)
    )
    result = cur.fetchone()
    cur.close()
    return result is not None

def insert_article(conn, class1, class2, title, description):
    """插入新文章"""
    content = generate_article_content(title, description)
    timestamp = get_random_timestamp()
    hits = random.randint(10000, 50000)

    cur = conn.cursor()
    try:
        sql = """
            INSERT INTO ep_news
            (title, description, content, class1, class2, class3, imgurl, hits, issue, updatetime, addtime, lang, recycle)
            VALUES (%s, %s, %s, %s, %s, 0, '', %s, 'system', %s, %s, 'cn', 0)
        """
        cur.execute(sql, (title, description, content, class1, class2, hits, timestamp, timestamp))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        logger.error(f"插入失败 [{class1}/{class2}] {title}: {e}")
        cur.close()
        return False

def clean_cache():
    """清理 MetInfo 缓存"""
    try:
        cache_dirs = [
            "/www/wwwroot/go.xiachaoqing.com/cache",
            "/www/wwwroot/go.xiachaoqing.com/templates/epgo-education/cache"
        ]
        for cache_dir in cache_dirs:
            subprocess.run(f"rm -rf {cache_dir}/*", shell=True, check=False)
        logger.info("缓存已清理")
    except Exception as e:
        logger.error(f"缓存清理失败: {e}")

def get_stats(conn):
    """获取统计信息"""
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0")
    total = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND DATE(addtime)=CURDATE()")
    today = cur.fetchone()[0]
    cur.close()
    return total, today

def main():
    logger.info("=" * 60)
    logger.info("开始 epgo 日常维护")
    logger.info("=" * 60)

    conn = pymysql.connect(**DB)
    added = 0
    skipped = 0

    # 为每个栏目插入一篇新文章
    for class2, (class1, class2_val) in CATEGORY_MAP.items():
        if class2 not in ARTICLE_TOPICS:
            continue

        # 根据今天的日期选择一个话题（轮转）
        day = datetime.now().day
        topics = ARTICLE_TOPICS[class2]
        topic_idx = day % len(topics)
        title, description = topics[topic_idx]

        # 检查是否已存在
        if check_duplicate(conn, class1, class2_val, title):
            logger.info(f"⊘ 跳过 [{class2}] {title[:40]}（已存在）")
            skipped += 1
            continue

        # 插入新文章
        if insert_article(conn, class1, class2_val, title, description):
            logger.info(f"✓ 插入 [{class2}] {title[:40]}")
            added += 1
        else:
            skipped += 1

    # 清理缓存
    clean_cache()

    # 统计
    total, today_count = get_stats(conn)
    conn.close()

    logger.info("=" * 60)
    logger.info(f"新增: {added} 篇 | 跳过: {skipped} 篇 | 总计: {total} 篇 | 今日: {today_count} 篇")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
