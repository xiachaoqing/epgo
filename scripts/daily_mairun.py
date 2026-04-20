#!/usr/bin/env python3
"""
mairunkeji.com 每日文章生成脚本
- 迈润科技官网，主营电机保护器/智能监控设备
- 每天生成3篇高质量行业文章
- 使用阿里百炼（通义千问）AI生成

crontab: 0 3 * * * cd /www/wwwroot/mairun && python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_mairun.py >> /www/wwwroot/mairun/logs/daily_mairun.log 2>&1

类型: 长期定时脚本
"""

import pymysql
import requests
import json
import random
import os
import re
import time
import logging
from datetime import datetime, timedelta

# ========== 配置 ==========
DB = dict(
    host="127.0.0.1", port=3306,
    user="hanhong", password="07090218",
    database="hanhong", charset="utf8mb4"
)

API_KEY = "sk-63851b428d4b43cb939ab1334a8d8ed8"
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
MODEL = "qwen-plus"

SITE_ROOT = "/www/wwwroot/mairun"
LOG_DIR = f"{SITE_ROOT}/logs"
LOG_FILE = f"{LOG_DIR}/daily_mairun.log"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
log = logging.getLogger()

# ========== 栏目配置 ==========
# mairunkeji 栏目: 10=产品中心, 128=新闻动态, 152=news(英文)
DAILY_COLUMNS = [
    (128, 0, "新闻动态", "zh"),
    (128, 0, "新闻动态", "zh"),
    (128, 0, "新闻动态", "zh"),
]

# 主题方向池 - 电机保护/工业自动化
TOPIC_SEEDS = {
    "新闻动态": [
        "电机保护器的选型指南：不同场景该怎么选",
        "变频器对电机寿命的影响与保护措施",
        "三相电机缺相保护的原理与重要性",
        "电机过载保护器的工作原理详解",
        "工业电机常见故障排查与预防方法",
        "智能电机监控系统如何降低停机成本",
        "电机轴承温度监测技术与预警方案",
        "防爆电机保护的特殊要求与解决方案",
        "电机绝缘检测技术的最新进展",
        "水泵电机保护器的应用与选型要点",
        "电机启动器类型对比：软启动vs变频启动",
        "工厂电机维护保养的最佳实践",
        "电机振动分析在预测性维护中的应用",
        "高压电机保护方案的设计要点",
        "电机节能改造方案与投资回报分析",
        "物联网在电机远程监控中的应用",
        "电机保护器安装调试的注意事项",
        "压缩机电机保护的特殊需求与方案",
        "电机过热原因分析与解决对策",
        "风机电机保护器的选型与应用案例",
        "工业4.0时代的智能电机管理系统",
        "电机功率因数优化与无功补偿方案",
        "矿用电机保护器的安全要求与标准",
        "电机堵转保护的几种实现方式",
    ],
}

# ========== AI生成 ==========
def generate_article(column_name, topic_seed, lang="zh"):
    if lang == "zh":
        prompt = f"""你是一位资深的工业自动化和电机保护领域的技术编辑。请围绕以下方向，写一篇专业、有深度的技术文章。

## 栏目
{column_name}

## 方向
{topic_seed}

## 要求
1. 标题：≤25个中文字，专业准确，吸引工程师和采购人员
2. 摘要：60-100字，概括核心价值
3. 正文：1500-2500字，必须包含：
   - 开头：明确问题场景，为什么这个话题重要
   - 3-5个小标题(h2)，每节有实质内容
   - 具体的技术参数、数据或案例
   - 实际应用场景和解决方案
   - 结尾：总结+推荐行动
4. 风格：专业严谨，面向工程技术人员和企业采购
5. 使用HTML标签：h2/p/ul/li/strong/em/blockquote/table
6. 不用markdown，不用h1

## 输出（严格JSON）
{{"title":"标题","description":"摘要","content":"HTML正文"}}"""
    else:
        return None

    try:
        resp = requests.post(API_URL,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.75, "max_tokens": 4000},
            timeout=120)
        if resp.status_code != 200:
            log.error(f"API {resp.status_code}")
            return None
        text = resp.json()["choices"][0]["message"]["content"].strip()
        if text.startswith("```"):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
        data = json.loads(text)
        content = data.get("content", "").strip()
        desc = data.get("description", "").strip()
        title = data.get("title", "").strip()
        plain = re.sub(r'<[^>]+>', '', content)
        if len(plain) < 500 or not title:
            return None
        if not desc or desc == title:
            desc = plain[:80]
        return {"title": title[:50], "description": desc[:200], "content": content}
    except Exception as e:
        log.error(f"生成失败: {e}")
        return None

# ========== 数据库操作 ==========
def title_exists(conn, title):
    cur = conn.cursor()
    cur.execute("SELECT id FROM hh_news WHERE title=%s AND recycle=0 LIMIT 1", (title,))
    r = cur.fetchone()
    cur.close()
    return r is not None

def insert_article(conn, class1, class2, article):
    hits = random.randint(5000, 25000)
    today = datetime.now().date()
    pub_time = datetime.combine(today, datetime.min.time()) + timedelta(
        hours=random.randint(8, 18), minutes=random.randint(0, 59))
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO hh_news
            (title, description, content, class1, class2, class3, imgurl, hits, issue, updatetime, addtime, lang, recycle)
            VALUES (%s, %s, %s, %s, %s, 0, '', %s, 'ai-gen', %s, %s, 'cn', 0)
        """, (article["title"], article["description"][:200], article["content"],
              class1, class2, hits, pub_time, pub_time))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        log.error(f"入库失败: {e}")
        conn.rollback()
        cur.close()
        return False

# ========== 主流程 ==========
def main():
    log.info("=" * 50)
    log.info(f"迈润科技每日文章生成 | 计划: {len(DAILY_COLUMNS)}篇")
    log.info("=" * 50)

    conn = pymysql.connect(**DB)
    added = 0

    for idx, (c1, c2, col, lang) in enumerate(DAILY_COLUMNS):
        log.info(f"[{idx+1}/{len(DAILY_COLUMNS)}] {col}")
        seeds = TOPIC_SEEDS.get(col, ["电机保护技术"])
        seed = random.choice(seeds)
        log.info(f"  方向: {seed[:40]}")

        article = None
        for _ in range(2):
            article = generate_article(col, seed, lang)
            if article and not title_exists(conn, article["title"]):
                break
            seed = random.choice(seeds)
            article = None

        if article and insert_article(conn, c1, c2, article):
            log.info(f"  ✓ {article['title']}")
            added += 1
        else:
            log.warning(f"  ✗ 失败")
        time.sleep(2)

    # 清缓存
    os.system(f"rm -rf {SITE_ROOT}/cache/* 2>/dev/null")

    conn.close()
    log.info(f"完成！新增 {added} 篇")

if __name__ == "__main__":
    main()
