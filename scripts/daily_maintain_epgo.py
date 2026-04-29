#!/usr/bin/env python3
"""
epgo 每日文章生成脚本（V3 - AI增强版）
- 使用阿里百炼（通义千问）生成高质量文章
- 每篇800-1500字，有具体知识点、例句、练习
- 标题≤20字中文，摘要和标题不重复
- 每天12篇，覆盖所有栏目
- 自动分配封面图 + 合理阅读数

crontab: 0 2 * * * cd /www/wwwroot/go.xiachaoqing.com && python3 scripts/daily_maintain_epgo.py >> logs/daily_maintain.log 2>&1
"""

import pymysql
import requests
import json
import random
import os
import subprocess
import logging
import time
import re
from datetime import datetime, timedelta

# ========== 配置 ==========
DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="Xia@07090218",
    database="epgo_db",
    charset="utf8mb4"
)

QWEN_API_KEY = "sk-63851b428d4b43cb939ab1334a8d8ed8"
QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
QWEN_MODEL = "qwen-plus"  # qwen-plus质量更好，成本也很低

SITE_ROOT = "/www/wwwroot/go.xiachaoqing.com"
LOG_FILE = f"{SITE_ROOT}/logs/daily_maintain.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ========== 栏目配置 ==========
# 每天生成的文章计划：栏目 -> (class1, class2, 栏目名称)
# 注意：class1必须用子栏目号（如111而非101），否则首页查询不到
DAILY_COLUMNS = [
    (111, 111, "KET真题解析"),
    (112, 112, "KET词汇速记"),
    (113, 113, "KET写作指导"),
    (114, 114, "KET听力技巧"),
    (121, 121, "PET真题解析"),
    (122, 122, "PET词汇速记"),
    (123, 123, "PET写作指导"),
    (124, 124, "PET阅读技巧"),
    (103, 0,   "英语阅读"),
    (104, 0,   "英语演讲"),
    (105, 0,   "每日英语"),
    (105, 0,   "每日英语"),  # 每日英语出2篇
]

# 每个栏目的主题方向池（AI每次从中随机选一个方向展开，保证内容不重复）
TOPIC_SEEDS = {
    "KET真题解析": [
        "Reading Part 1-5中某个Part的题型拆解与解题步骤",
        "Writing Part 6或Part 7的审题技巧和高分范文",
        "Listening某个Part的听力陷阱与应对方法",
        "Speaking口语考试常见话题与回答模板",
        "历年高频考点归纳与备考优先级",
        "KET考试时间分配策略与临场技巧",
        "KET模拟题逐题精讲与易错点分析",
        "从KET真题看出题规律与趋势变化",
    ],
    "KET词汇速记": [
        "学校生活场景核心词汇与例句",
        "购物与餐饮场景高频表达",
        "家庭与朋友关系描述词汇",
        "旅行与交通场景必备单词",
        "天气与自然环境相关词汇",
        "兴趣爱好与运动休闲表达",
        "身体健康与看病就医词汇",
        "词根词缀记忆法实战应用",
        "容易混淆的近义词辨析",
        "KET高频动词短语与固定搭配",
    ],
    "KET写作指导": [
        "邮件写作的开头结尾万能模板",
        "看图写句子的描述技巧与常用句型",
        "写作中常见语法错误与纠正方法",
        "如何在25字限制内写好短消息",
        "写作连接词使用技巧让文章更流畅",
        "写作审题方法：快速抓住题目要求",
        "高分范文拆解：好文章好在哪里",
        "限时写作训练方法与节奏控制",
    ],
    "KET听力技巧": [
        "图片选择题的预判与关键词捕捉",
        "数字、时间、价格的听辨专项训练",
        "对话理解题中的转折与否定陷阱",
        "笔记填空题的速记与拼写技巧",
        "不同英式美式口音的适应训练",
        "听前读题与信息预测方法",
        "长对话中追踪说话人观点的技巧",
        "听力高频场景词汇速查与记忆",
    ],
    "PET真题解析": [
        "Reading Part 5-6阅读理解的定位技巧",
        "Writing Part 1句子改写的同义转换方法",
        "Writing Part 2邮件或故事写作高分策略",
        "Listening Part 1-4各题型的核心解题思路",
        "Speaking看图描述与讨论的表达框架",
        "PET阅读长文快速定位答案的扫读技巧",
        "PET历年真题高频话题与考点汇总",
        "PET与KET难度差异对比与升级策略",
    ],
    "PET词汇速记": [
        "B1级别校园与学术场景核心词汇",
        "社交与人际关系描述的高级表达",
        "环境与社会话题相关词汇积累",
        "科技与媒体主题的现代英语表达",
        "情感与心理状态的精准描述词",
        "PET考试中的同义替换高频词对",
        "从KET到PET的词汇跨越必备清单",
        "PET写作中加分的高级词汇与短语",
    ],
    "PET写作指导": [
        "邮件回复的标准结构与得分要点",
        "故事续写的情节设计与语言技巧",
        "议论文写作的观点表达与论证方法",
        "PET写作评分标准详解与对标练习",
        "从简单句到复合句的写作升级技巧",
        "写作中过渡词与逻辑连接的运用",
        "PET高分范文赏析与模仿训练",
        "限时写作的时间分配与检查策略",
    ],
    "PET阅读技巧": [
        "同义替换的快速识别与积累方法",
        "主旨题与细节题的审题与答题区别",
        "长文阅读的段落结构分析技巧",
        "上下文推断生词词义的实用方法",
        "阅读速度提升的系统训练方案",
        "PET阅读中的逻辑推理与推断题",
        "不同体裁文章的阅读策略差异",
        "PET真题阅读逐篇精讲与规律总结",
    ],
    "英语阅读": [
        "适合中学生的英文原著推荐与阅读方法",
        "新闻英语阅读：如何读懂BBC/CNN文章",
        "英语阅读中的长难句拆解技巧",
        "如何通过大量阅读自然提升词汇量",
        "英语阅读笔记的高效记录方法",
        "科普类英语文章的阅读策略",
        "英语故事类文章的情节理解技巧",
        "英语阅读习惯养成的21天计划",
    ],
    "英语演讲": [
        "英语演讲开场白的5种经典方式",
        "如何克服英语演讲时的紧张与怯场",
        "英语演讲中的肢体语言与语调技巧",
        "TED演讲结构分析：如何讲好一个故事",
        "英语辩论的论点组织与反驳技巧",
        "校园英语演讲的话题选择与素材积累",
        "英语演讲中的修辞手法与表达力",
        "即兴英语发言的快速组织思路法",
    ],
    "每日英语": [
        "日常问候与社交寒暄的地道表达",
        "描述天气与季节的实用英语句型",
        "点餐与外出就餐的英语对话实练",
        "表达观点与同意反对的礼貌说法",
        "打电话与发消息的常用英语表达",
        "描述日常习惯与作息的英语表达",
        "旅行与出行中的实用英语会话",
        "描述感受与情绪的丰富英语表达",
        "课堂互动与学习讨论的英语句型",
        "购物与网购场景的英语对话练习",
        "描述人物外貌与性格的英语表达",
        "节日与文化相关的趣味英语知识",
    ],
}

# 封面图目录映射
COVER_DIRS = {
    101: "ket", 102: "pet", 103: "reading", 104: "speech",
    105: "daily", 106: "download", 107: "about",
    111: "ket", 112: "ket", 113: "ket", 114: "ket",
    121: "pet", 122: "pet", 123: "pet", 124: "pet",
}


# ========== AI文章生成 ==========
def call_qwen(prompt, max_tokens=3000):
    """调用通义千问API"""
    try:
        resp = requests.post(
            QWEN_API_URL,
            headers={
                "Authorization": f"Bearer {QWEN_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": QWEN_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": max_tokens,
            },
            timeout=90
        )

        if resp.status_code != 200:
            log.error(f"API返回 {resp.status_code}: {resp.text[:200]}")
            return None

        data = resp.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        log.error(f"调用通义千问失败: {e}")
        return None


def generate_article(column_name, topic_seed):
    """用AI生成一篇高质量文章"""

    prompt = f"""你是"英语陪跑GO"网站的资深英语教育编辑。请围绕以下方向，写一篇高质量的英语学习文章。

## 栏目
{column_name}

## 本期方向
{topic_seed}

## 严格要求
1. **标题**：≤18个中文字符，简洁有力，能吸引家长和学生点击。不要用冒号把标题分成两半。
2. **摘要**：50-80字，概括文章核心价值，绝对不能和标题一样。
3. **正文**：800-1500字，必须包含：
   - 开头段（2-3句话，直接说清本文解决什么问题）
   - 3-5个小节，每节有小标题
   - 每个小节要有**具体的英语例句**（中英对照）
   - 实用的学习方法或做题步骤
   - 结尾段（总结要点 + 鼓励语）
4. **风格**：像一个耐心的好老师在讲课，专业但不枯燥，有干货有温度
5. **正文用HTML格式**：用 h2/h3/p/ul/li/strong/blockquote 标签，不要用markdown

## 输出格式
请严格按以下JSON格式输出，不要输出其他任何内容：
{{"title":"标题","description":"摘要","content":"正文HTML"}}"""

    raw = call_qwen(prompt)
    if not raw:
        return None

    # 解析JSON
    try:
        # 去掉可能的markdown代码块包裹
        text = raw.strip()
        if text.startswith("```"):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)

        article = json.loads(text)

        # 质量校验
        title = article.get("title", "").strip()
        desc = article.get("description", "").strip()
        content = article.get("content", "").strip()

        if not title or not content:
            log.warning("AI返回内容缺失title或content")
            return None

        # 标题截断保护
        if len(title) > 30:
            title = title[:18]

        # 描述不能等于标题
        if desc == title or not desc:
            # 从content提取前80字作为描述
            plain = re.sub(r'<[^>]+>', '', content)
            desc = plain[:80].strip()

        # 内容太短则拒绝
        plain_content = re.sub(r'<[^>]+>', '', content)
        if len(plain_content) < 300:
            log.warning(f"AI生成内容太短({len(plain_content)}字)，丢弃")
            return None

        return {
            "title": title,
            "description": desc,
            "content": content
        }

    except json.JSONDecodeError as e:
        log.error(f"JSON解析失败: {e}\n原始内容前200字: {raw[:200]}")
        return None


# ========== 封面图 ==========
def get_cover(class1, class2):
    """获取封面图路径"""
    cover_key = class2 if class2 > 0 else class1
    dir_name = COVER_DIRS.get(cover_key, "daily")
    upload_dir = f"{SITE_ROOT}/upload/epgo-photo-covers/{dir_name}"

    try:
        if os.path.exists(upload_dir):
            files = [f for f in os.listdir(upload_dir)
                     if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if files:
                chosen = random.choice(files)
                return f"/upload/epgo-photo-covers/{dir_name}/{chosen}"
    except Exception as e:
        log.warning(f"获取封面失败: {e}")

    return ""


# ========== 去重检查 ==========
def title_exists(conn, title):
    """检查标题是否已存在"""
    cur = conn.cursor()
    cur.execute("SELECT id FROM ep_news WHERE title=%s AND recycle=0 LIMIT 1", (title,))
    result = cur.fetchone()
    cur.close()
    return result is not None


# ========== 获取今天已用过的主题方向 ==========
def get_today_topics(conn):
    """获取今天已生成的文章标题，避免方向重复"""
    cur = conn.cursor()
    cur.execute(
        "SELECT title FROM ep_news WHERE recycle=0 AND DATE(addtime)=CURDATE()"
    )
    titles = [row[0] for row in cur.fetchall()]
    cur.close()
    return titles


# ========== 入库 ==========
def insert_article(conn, class1, class2, article):
    """插入文章到数据库"""
    cover = get_cover(class1, class2)
    hits = random.randint(18000, 42000)

    # 随机时间（当天6:00-22:00）
    today = datetime.now().date()
    pub_time = datetime.combine(today, datetime.min.time()) + timedelta(
        hours=random.randint(6, 22),
        minutes=random.randint(0, 59)
    )

    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO ep_news
            (title, description, content, class1, class2, class3, imgurl, hits, issue, updatetime, addtime, lang, recycle)
            VALUES (%s, %s, %s, %s, %s, 0, %s, %s, 'ai-gen', %s, %s, 'cn', 0)
        """, (
            article["title"],
            article["description"][:200],
            article["content"],
            class1,
            class2,
            cover,
            hits,
            pub_time,
            pub_time
        ))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        log.error(f"入库失败: {e}")
        conn.rollback()
        cur.close()
        return False


# ========== 清缓存 ==========
def clean_cache():
    """清理MetInfo缓存"""
    for d in ["cache", "templates/epgo-education/cache"]:
        path = f"{SITE_ROOT}/{d}"
        if os.path.exists(path):
            subprocess.run(f"rm -rf {path}/*", shell=True, check=False)
    log.info("缓存已清理")


# ========== 主流程 ==========
def main():
    log.info("=" * 60)
    log.info("每日文章生成 V3（AI增强版）启动")
    log.info(f"模型: {QWEN_MODEL} | 计划生成: {len(DAILY_COLUMNS)} 篇")
    log.info("=" * 60)

    conn = pymysql.connect(**DB)
    today_titles = get_today_topics(conn)

    if len(today_titles) >= len(DAILY_COLUMNS):
        log.info(f"今天已生成 {len(today_titles)} 篇，无需重复执行")
        conn.close()
        return

    added = 0
    failed = 0

    for idx, (class1, class2, column_name) in enumerate(DAILY_COLUMNS):
        log.info(f"\n--- [{idx+1}/{len(DAILY_COLUMNS)}] {column_name} ---")

        # 从主题池随机选一个方向
        seeds = TOPIC_SEEDS.get(column_name, ["英语学习方法与技巧分享"])
        topic_seed = random.choice(seeds)
        log.info(f"方向: {topic_seed[:40]}")

        # 调用AI生成
        retries = 0
        article = None
        while retries < 2:
            article = generate_article(column_name, topic_seed)
            if article and not title_exists(conn, article["title"]):
                break
            if article:
                log.info("标题重复，换个方向重试")
                topic_seed = random.choice(seeds)
            retries += 1
            article = None

        if not article:
            log.warning(f"✗ {column_name} 生成失败")
            failed += 1
            continue

        # 入库
        if insert_article(conn, class1, class2, article):
            log.info(f"✓ 入库成功: {article['title']}")
            added += 1
        else:
            failed += 1

        # 请求间隔，避免API限流
        time.sleep(2)

    # 清缓存
    clean_cache()

    # 统计
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()

    log.info("=" * 60)
    log.info(f"完成！成功: {added} 篇 | 失败: {failed} 篇 | 文章总计: {total} 篇")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
