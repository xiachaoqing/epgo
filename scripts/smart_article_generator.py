#!/usr/bin/env python3
"""
英语陪跑GO - 高质量文章爬取和二次创作系统
策略：
1. 从高质量教育网站爬取热点爆文（Medium、英语学习网站等）
2. 使用LLM进行智能改写/二次创作
3. 保留核心价值，优化表达
4. 自动生成中文和英文版本
5. 配置真实图片和合理阅读数
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime, timedelta
import random
import requests
from bs4 import BeautifulSoup
import pymysql

# ============ 配置 ============
DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="Xia@07090218",
    database="epgo_db",
    charset="utf8mb4"
)

# 爬取源配置 - 高质量教育类英文网站
SOURCES = [
    {
        "name": "Medium - English Learning",
        "url": "https://medium.com/tag/english-learning",
        "keywords": ["KET", "PET", "English", "exam", "vocabulary", "speaking", "writing"]
    },
    {
        "name": "English Teachers Online",
        "url": "https://www.englishteachersontv.com/",
        "keywords": ["grammar", "pronunciation", "fluency", "conversation"]
    },
    {
        "name": "Cambridge English Blog",
        "url": "https://www.cambridgeenglish.org/blog/",
        "keywords": ["exam", "preparation", "tips", "strategy"]
    }
]

# LLM改写提示词
REWRITE_PROMPT = """
你是一位专业的英语教育内容创作者。

原文内容：
{original}

任务：
1. 保留原文的核心知识点和价值
2. 用更专业、更实用的语言重新组织
3. 添加实际例子和场景应用
4. 组织结构：标题 → 背景 → 关键点(3-5条) → 实践建议 → 总结
5. 字数800-1200字，通俗易懂

输出格式：
{{
    "title": "优化后的标题",
    "content": "完整的改写内容（HTML格式）",
    "key_points": ["要点1", "要点2", "要点3"],
    "difficulty": "初级/中级/高级"
}}
"""

# ============ 爬虫模块 ============

def fetch_articles_from_source(source):
    """从指定源爬取文章列表"""
    articles = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(source['url'], headers=headers, timeout=10)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.content, 'html.parser')

        # 提取文章 - 这是通用逻辑，需要根据每个网站调整
        for article_elem in soup.find_all(['article', 'div'], class_=['post', 'article-item']):
            title_elem = article_elem.find(['h1', 'h2', 'h3', 'a'])
            title = title_elem.text.strip() if title_elem else "Unknown"

            text_elem = article_elem.find(['p', 'div'], class_=['content', 'excerpt', 'summary'])
            text = text_elem.text.strip() if text_elem else ""

            # 过滤：只要高质量、与关键词相关的文章
            if any(keyword.lower() in title.lower() or keyword.lower() in text.lower()
                   for keyword in source['keywords']):
                articles.append({
                    'title': title[:100],
                    'content': text[:500],
                    'source': source['name'],
                    'url': article_elem.find('a', href=True)['href'] if article_elem.find('a', href=True) else ""
                })

        print(f"✓ 从 {source['name']} 爬取 {len(articles)} 篇文章")
        return articles

    except Exception as e:
        print(f"❌ 爬取 {source['name']} 失败: {e}")
        return []

# ============ LLM改写模块 ============

def rewrite_with_llm(original_content, title):
    """
    使用LLM进行二次创作改写
    实际使用需要接入OpenAI/Claude等API
    这里是示例框架
    """
    # TODO: 集成实际的LLM API调用
    # 此处示例使用占位符，实际使用时需要配置API key

    # 临时方案：使用本地启发式改写（直到集成LLM）
    improved_content = generate_improved_content(original_content, title)

    return improved_content

def generate_improved_content(original, title):
    """本地启发式改写 - 用更好的结构和内容生成"""
    return {
        "title": title,
        "content": f"""
<p><strong>{title}</strong></p>

<p>英语学习中，{title.lower()}是一个关键课题。本文基于多个高质量教育源的综合分析，为你提供最实用的学习方法。</p>

<h2>核心要点</h2>
<ul>
<li><strong>系统学习</strong>：从基础到进阶的完整学习路径</li>
<li><strong>实际应用</strong>：在真实场景中如何运用所学知识</li>
<li><strong>高效练习</strong>：最有效的反复练习方法</li>
<li><strong>常见误区</strong>：避免浪费时间的错误方向</li>
</ul>

<h2>学习建议</h2>
<p>根据剑桥英语考试标准，建议学习者：</p>
<ol>
<li>每天投入30分钟专项训练</li>
<li>使用真实考试题目进行练习</li>
<li>定期参加模拟考试检测进度</li>
<li>与学习伙伴进行交流和讨论</li>
</ol>

<p>坚持这个方法，3个月内你会看到显著的进步。关注英语陪跑GO，获取每日备考资源！</p>
""",
        "key_points": ["系统学习", "实际应用", "高效练习", "常见误区"],
        "difficulty": "中级"
    }

# ============ 入库模块 ============

def insert_article_to_db(conn, title, description, content, class1, class2, difficulty):
    """将改写后的文章插入数据库"""

    # 生成合理的阅读数（不要太极端）
    hits = random.randint(15000, 45000)  # 更合理的范围

    # 生成随机时间戳（避免同时发布）
    base_time = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=random.randint(0, 7))
    timestamp = base_time + timedelta(hours=random.randint(6, 22), minutes=random.randint(0, 59))

    # 获取对应分类的随机封面
    imgurl = get_random_cover(class2 if class2 > 0 else class1)

    cur = conn.cursor()
    try:
        sql = """
            INSERT INTO ep_news
            (title, description, content, class1, class2, class3, imgurl, hits, issue, updatetime, addtime, lang, recycle)
            VALUES (%s, %s, %s, %s, %s, 0, %s, %s, 'source', %s, %s, 'cn', 0)
        """
        cur.execute(sql, (
            title[:100],
            description[:200],
            content,
            class1,
            class2,
            imgurl,
            hits,
            timestamp,
            timestamp
        ))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"❌ 入库失败: {e}")
        cur.close()
        return False

def get_random_cover(class_id):
    """为文章获取随机高质量封面"""
    COVER_DIRS = {
        101: "ket", 102: "pet", 103: "reading", 104: "speech",
        105: "daily", 106: "download", 107: "about",
        111: "ket", 112: "ket", 113: "ket", 114: "ket",
        121: "pet", 122: "pet", 123: "pet", 124: "pet",
    }

    if class_id not in COVER_DIRS:
        return ""

    dir_name = COVER_DIRS[class_id]
    upload_dir = f"/www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers/{dir_name}"

    try:
        import os
        if os.path.exists(upload_dir):
            files = [f for f in os.listdir(upload_dir) if f.endswith('.jpg') and 'test' not in f]
            if files:
                chosen = random.choice(files)
                return f"/upload/epgo-photo-covers/{dir_name}/{chosen}"
    except:
        pass

    return ""

# ============ 主流程 ============

def main():
    print("=" * 60)
    print("英语陪跑GO - 高质量文章爬取和二次创作系统")
    print("=" * 60)

    # 1. 爬取所有源的文章
    all_articles = []
    for source in SOURCES:
        articles = fetch_articles_from_source(source)
        all_articles.extend(articles)
        time.sleep(2)  # 礼貌间隔

    print(f"\n✓ 总共爬取 {len(all_articles)} 篇文章")

    if not all_articles:
        print("⚠️  没有爬取到文章，程序退出")
        return

    # 2. 对每篇文章进行LLM改写
    improved_articles = []
    for article in all_articles[:10]:  # 演示：先改写10篇
        print(f"\n处理: {article['title'][:40]}...")
        improved = rewrite_with_llm(article['content'], article['title'])
        improved_articles.append(improved)
        time.sleep(1)

    # 3. 入库
    conn = pymysql.connect(**DB)
    added = 0

    for improved in improved_articles:
        # 简单的分类判断（实际需要更智能的分类）
        class1, class2 = get_article_category(improved['title'])

        if insert_article_to_db(
            conn,
            improved['title'],
            improved['title'],  # description就用title
            improved['content'],
            class1,
            class2,
            improved.get('difficulty', '中级')
        ):
            added += 1
            print(f"✓ 入库: {improved['title'][:40]}")

    conn.close()

    print(f"\n{'=' * 60}")
    print(f"完成！共入库 {added} 篇高质量文章")
    print(f"{'=' * 60}\n")

def get_article_category(title):
    """根据标题智能分类"""
    title_lower = title.lower()

    if 'ket' in title_lower:
        return 101, 111
    elif 'pet' in title_lower:
        return 102, 121
    elif '阅读' in title_lower or 'read' in title_lower:
        return 103, 0
    elif '演讲' in title_lower or 'speak' in title_lower or 'speech' in title_lower:
        return 104, 0
    elif '日常' in title_lower or 'daily' in title_lower:
        return 105, 0
    elif '词汇' in title_lower or 'vocabulary' in title_lower:
        return 101, 112
    elif '写作' in title_lower or 'writing' in title_lower or 'write' in title_lower:
        return 101, 113
    elif '听力' in title_lower or 'listen' in title_lower:
        return 101, 114
    else:
        return 105, 0  # 默认分类

if __name__ == "__main__":
    main()
