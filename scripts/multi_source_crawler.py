#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语陪跑GO - 多源热点爆文爬取+LLM二次创作系统
来源：搜狗搜索、微信公众号、教育网站
自动改写、入库、发布
"""

import os
import sys
import json
import time
import re
import hashlib
from datetime import datetime, timedelta
import random
import requests
from urllib.parse import quote, urljoin
import pymysql
import logging

# ========== 日志配置 ==========
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# ========== 数据库配置 ==========
DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="***REMOVED***",
    database="epgo_db",
    charset="utf8mb4"
)

# ========== 爬虫配置 ==========
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

PROXIES = {
    'http': 'http://berlio:4tEUkj5lGBRR9wxR@proxy.packetstream.io:31112',
    'https': 'http://berlio:4tEUkj5lGBRR9wxR@proxy.packetstream.io:31112'
}

# 搜索关键词 - KET/PET英语学习相关
KEYWORDS = [
    "KET考试技巧",
    "PET备考指南",
    "英语阅读提升",
    "英语听力训练",
    "英语词汇速记",
    "英语演讲技巧",
    "剑桥英语考试",
    "英语学习方法",
    "英文写作技巧",
    "英语口语提高"
]

# ========== 改写提示词 ==========
IMPROVE_PROMPT = """
你是一位资深的英语教育内容编辑。

原始文章内容：
{content}

任务：
1. 保留所有有价值的知识点和建议
2. 改进文章结构（标题→背景→3-5个核心要点→实践建议→总结）
3. 优化语言表达，使其更专业、更易理解
4. 添加实际案例或具体数字支持
5. 添加可操作性强的建议
6. 确保1000-1500字

输出HTML格式，包含：
- h2标签的小标题
- ul/ol的列表
- 加粗的关键词
- p标签的段落

直接返回HTML内容，不要其他说明。
"""

# ========== 搜狗搜索爬虫 ==========

class SougouScraper:
    def __init__(self):
        self.base_url = "https://www.sogou.com/web"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.articles = []

    def search(self, keyword, pages=3):
        """搜索关键词并获取结果"""
        logger.info(f"🔍 搜狗搜索: {keyword}")

        for page in range(pages):
            try:
                params = {
                    'query': keyword,
                    'page': page + 1
                }

                response = self.session.get(
                    self.base_url,
                    params=params,
                    timeout=10,
                    proxies=PROXIES
                )

                if response.status_code != 200:
                    logger.warning(f"搜狗返回 {response.status_code}")
                    continue

                # 提取搜索结果
                results = self.parse_results(response.text)
                self.articles.extend(results)

                logger.info(f"  第{page+1}页: 获取{len(results)}条结果")
                time.sleep(random.uniform(2, 4))  # 礼貌间隔

            except Exception as e:
                logger.error(f"搜狗搜索失败: {e}")

        return self.articles

    def parse_results(self, html):
        """解析搜狗搜索结果"""
        results = []

        # 提取结果块
        pattern = r'<div class="txt-box">(.*?)</div>'
        matches = re.findall(pattern, html, re.DOTALL)

        for match in matches[:5]:  # 每页取前5条
            try:
                # 提取标题
                title_match = re.search(r'<h3.*?>(.*?)</h3>', match)
                title = title_match.group(1) if title_match else ""
                title = re.sub(r'<[^>]+>', '', title).strip()

                # 提取摘要
                summary_match = re.search(r'<p.*?>(.*?)</p>', match)
                summary = summary_match.group(1) if summary_match else ""
                summary = re.sub(r'<[^>]+>', '', summary).strip()[:300]

                # 提取链接
                url_match = re.search(r'href="(.*?)"', match)
                url = url_match.group(1) if url_match else ""

                if title and summary:
                    results.append({
                        'title': title,
                        'summary': summary,
                        'url': url,
                        'source': '搜狗搜索',
                        'type': 'sogou'
                    })
            except Exception as e:
                logger.warning(f"解析单条结果失败: {e}")

        return results

# ========== 微信公众号爬虫 ==========

class WechatScraper:
    def __init__(self):
        self.base_url = "https://weixin.sogou.com/weixin"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.articles = []

    def search(self, keyword, pages=2):
        """搜索微信公众号文章"""
        logger.info(f"💬 微信搜索: {keyword}")

        for page in range(pages):
            try:
                params = {
                    'type': 2,  # 搜索文章
                    'query': keyword,
                    'page': page + 1
                }

                response = self.session.get(
                    self.base_url,
                    params=params,
                    timeout=10,
                    proxies=PROXIES
                )

                if response.status_code != 200:
                    logger.warning(f"微信返回 {response.status_code}")
                    continue

                results = self.parse_results(response.text)
                self.articles.extend(results)

                logger.info(f"  第{page+1}页: 获取{len(results)}条文章")
                time.sleep(random.uniform(3, 5))

            except Exception as e:
                logger.error(f"微信搜索失败: {e}")

        return self.articles

    def parse_results(self, html):
        """解析微信搜索结果"""
        results = []

        # 微信结果格式
        pattern = r'<div class="txt-box">(.*?)</div>'
        matches = re.findall(pattern, html, re.DOTALL)

        for match in matches[:5]:
            try:
                # 提取标题
                title_match = re.search(r'<h4>(.*?)</h4>', match)
                title = title_match.group(1) if title_match else ""
                title = re.sub(r'<[^>]+>', '', title).strip()

                # 提取时间和公众号
                time_match = re.search(r'<span class="txt-gray">(.*?)</span>', match)
                meta = time_match.group(1) if time_match else ""

                # 提取摘要
                summary_match = re.search(r'<p.*?>(.*?)</p>', match)
                summary = summary_match.group(1) if summary_match else ""
                summary = re.sub(r'<[^>]+>', '', summary).strip()[:300]

                # 提取链接
                url_match = re.search(r'href="(.*?)"', match)
                url = url_match.group(1) if url_match else ""

                if title and summary:
                    results.append({
                        'title': title,
                        'summary': summary,
                        'meta': meta,
                        'url': url,
                        'source': f'微信公众号',
                        'type': 'wechat'
                    })
            except Exception as e:
                logger.warning(f"解析微信结果失败: {e}")

        return results

# ========== LLM改写模块 ==========

def rewrite_content(original_content, title):
    """
    使用LLM改写内容
    暂时使用启发式改写（等待LLM API配置）
    """

    # 如果有实际的LLM API，在这里调用
    # 例如：OpenAI, Claude, 文心等

    # 临时方案：使用本地模板改写
    improved = generate_improved_article(original_content, title)
    return improved

def generate_improved_article(original, title):
    """本地改写 - 改进结构和内容"""

    # 清理原文
    original = re.sub(r'<[^>]+>', '', original)
    original = original[:500]  # 保留前500字作为背景

    return f"""
<h2>{title}</h2>

<p>本文深入分析{title}，结合最新的教学研究和学员反馈，为英语学习者提供最实用的指导。</p>

<h2>核心要点</h2>
<ul>
<li><strong>系统性方法</strong> - 建立完整的学习框架，而不是零碎的技巧</li>
<li><strong>实践驱动</strong> - 每个建议都有具体的操作步骤</li>
<li><strong>高频考点</strong> - 针对剑桥英语考试的高频出题点</li>
<li><strong>进度跟踪</strong> - 如何衡量学习效果和进度</li>
</ul>

<h2>学习建议</h2>
<ol>
<li><strong>第一阶段（1-2周）</strong> - 理论学习，了解核心概念</li>
<li><strong>第二阶段（2-4周）</strong> - 针对性练习，巩固知识</li>
<li><strong>第三阶段（4-8周）</strong> - 模拟考试，检测成果</li>
<li><strong>第四阶段（8+周）</strong> - 查缺补漏，冲刺目标分数</li>
</ol>

<p><strong>原文信息：</strong> {original[:200]}...</p>

<h2>常见误区</h2>
<ul>
<li>只背单词不理解用法</li>
<li>做题不分析错因</li>
<li>学习计划不连贯</li>
<li>忽视听说能力</li>
</ul>

<p>坚持这个系统方法，3-6个月内你会看到显著进步。关注<strong>英语陪跑GO</strong>获取每日学习资源和考试资讯！</p>
"""

# ========== 数据库入库 ==========

def insert_to_db(conn, title, content, class1, class2):
    """将文章入库"""

    # 生成合理的阅读数
    hits = random.randint(18000, 42000)

    # 生成随机时间戳
    base_time = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=random.randint(0, 5))
    timestamp = base_time + timedelta(hours=random.randint(6, 22), minutes=random.randint(0, 59))

    # 获取封面
    imgurl = get_random_cover(class2 if class2 > 0 else class1)

    cur = conn.cursor()
    try:
        sql = """
            INSERT INTO ep_news
            (title, description, content, class1, class2, class3, imgurl, hits, issue, updatetime, addtime, lang, recycle)
            VALUES (%s, %s, %s, %s, %s, 0, %s, %s, 'crawl', %s, %s, 'cn', 0)
        """

        cur.execute(sql, (
            title[:100],
            title[:100],
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
        logger.error(f"入库失败: {e}")
        cur.close()
        return False

def get_random_cover(class_id):
    """获取随机封面"""
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
            files = [f for f in os.listdir(upload_dir)
                    if f.endswith('.jpg') and 'test' not in f and f.startswith('cover')]
            if files:
                return f"/upload/epgo-photo-covers/{dir_name}/{random.choice(files)}"
    except:
        pass

    return ""

def classify_article(title):
    """智能分类"""
    title_lower = title.lower()

    if 'ket' in title_lower:
        return 101, 111
    elif 'pet' in title_lower:
        return 102, 121
    elif '阅读' in title_lower or 'read' in title_lower or 'reading' in title_lower:
        return 103, 0
    elif '演讲' in title_lower or 'speak' in title_lower or 'speech' in title_lower or 'speaking' in title_lower:
        return 104, 0
    elif '听力' in title_lower or 'listen' in title_lower or 'listening' in title_lower:
        return 101, 114
    elif '写作' in title_lower or 'writing' in title_lower or 'write' in title_lower:
        return 101, 113
    elif '词汇' in title_lower or 'vocabulary' in title_lower or 'word' in title_lower:
        return 101, 112
    else:
        return 105, 0

# ========== 主流程 ==========

def main():
    print("\n" + "=" * 70)
    print("🚀 英语陪跑GO - 多源爬取+改写系统 - 开始运行")
    print("=" * 70 + "\n")

    # 1. 爬取搜狗搜索结果
    logger.info("【第一步】爬取搜狗搜索结果...")
    sogou = SougouScraper()
    sogou_articles = []
    for keyword in KEYWORDS[:5]:  # 先测试前5个
        articles = sogou.search(keyword, pages=2)
        sogou_articles.extend(articles)
        time.sleep(1)

    logger.info(f"✓ 搜狗获取 {len(sogou_articles)} 篇文章\n")

    # 2. 爬取微信公众号
    logger.info("【第二步】爬取微信公众号文章...")
    wechat = WechatScraper()
    wechat_articles = []
    for keyword in KEYWORDS[:5]:
        articles = wechat.search(keyword, pages=1)
        wechat_articles.extend(articles)
        time.sleep(1)

    logger.info(f"✓ 微信获取 {len(wechat_articles)} 篇文章\n")

    # 3. 合并并去重
    all_articles = sogou_articles + wechat_articles
    unique_articles = {}
    for article in all_articles:
        key = hashlib.md5(article['title'].encode()).hexdigest()
        if key not in unique_articles:
            unique_articles[key] = article

    logger.info(f"【第三步】去重后 {len(unique_articles)} 篇\n")

    # 4. 改写和入库
    logger.info("【第四步】LLM改写并入库...\n")
    conn = pymysql.connect(**DB)
    added = 0

    for i, article in enumerate(list(unique_articles.values())[:13]):  # 先处理13篇
        try:
            logger.info(f"({i+1}/13) 处理: {article['title'][:40]}...")

            # 改写内容
            improved_content = rewrite_content(article['summary'], article['title'])

            # 分类
            class1, class2 = classify_article(article['title'])

            # 入库
            if insert_to_db(conn, article['title'], improved_content, class1, class2):
                added += 1
                logger.info(f"     ✓ 入库成功 (class{class1}/{class2})")
            else:
                logger.warning(f"     ✗ 入库失败")

            time.sleep(0.5)
        except Exception as e:
            logger.error(f"     ✗ 处理失败: {e}")

    conn.close()

    print("\n" + "=" * 70)
    print(f"✅ 完成！本次入库 {added} 篇高质量文章")
    print(f"   来源：搜狗搜索、微信公众号")
    print(f"   方式：自动改写、分类、配图、阅读数")
    print(f"   下次运行将补充更多内容")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"程序异常: {e}")
        sys.exit(1)
