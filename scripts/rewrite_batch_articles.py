#!/usr/bin/env python3
"""
rewrite_batch_articles.py - 一次性批量改写低质量文章

用途: 改写所有低质量文章（重复+模板+过短），提升Google AdSense审核通过率
脚本类型: 一次性执行（可多轮运行）
触发方式: 手动执行

运行示例:
  python3 rewrite_batch_articles.py --round=1 --batch-size=20
  python3 rewrite_batch_articles.py --round=2 --parallel=4

修改历史:
  2026-04-16 v1.0 - 初始版本
"""

import pymysql
import requests
import json
import argparse
import logging
import time
import os
import re
import hashlib
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

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
QWEN_MODEL = "qwen-plus"

SITE_ROOT = "/www/wwwroot/go.xiachaoqing.com"
LOG_DIR = f"{SITE_ROOT}/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = f"{LOG_DIR}/rewrite_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ========== 参数 ==========
class Config:
    def __init__(self):
        parser = argparse.ArgumentParser(description='批量改写低质量文章')
        parser.add_argument('--round', type=int, choices=[1, 2, 3], default=1,
                          help='改写轮次: 1=重复 2=模板 3=过短')
        parser.add_argument('--batch-size', type=int, default=20,
                          help='每批处理数量（默认20）')
        parser.add_argument('--parallel', type=int, default=1,
                          help='并行线程数（默认1=串行）')
        parser.add_argument('--quality-threshold', type=int, default=6,
                          help='质量评分阈值(1-10)')
        parser.add_argument('--api-key', type=str, default=QWEN_API_KEY,
                          help='LLM API Key')
        parser.add_argument('--dry-run', action='store_true',
                          help='测试模式，不实际修改DB')
        parser.add_argument('--resume-from-id', type=int, default=None,
                          help='断点续传，从指定ID继续')

        self.args = parser.parse_args()
        self.round = self.args.round
        self.batch_size = self.args.batch_size
        self.parallel = self.args.parallel
        self.quality_threshold = self.args.quality_threshold
        self.api_key = self.args.api_key
        self.dry_run = self.args.dry_run
        self.resume_from_id = self.args.resume_from_id

config = Config()

# ========== 数据库操作 ==========

def get_low_quality_articles(round_num, limit=None):
    """获取需要改写的低质量文章"""
    conn = pymysql.connect(**DB)
    cur = conn.cursor()

    if round_num == 1:
        # 第一轮：重复内容（开头200字相同的）
        sql = """
        SELECT id, title, class1, class2, LEFT(content, 200) as c200
        FROM ep_news
        WHERE recycle=0 AND LENGTH(content)<3000 AND issue NOT IN ('ai-gen','rewrite-v1','rewrite-v2')
        ORDER BY LENGTH(content) ASC
        LIMIT %s
        """ % (limit or 500)

    elif round_num == 2:
        # 第二轮：模板化内容
        sql = """
        SELECT id, title, class1, class2, content
        FROM ep_news
        WHERE recycle=0 AND issue NOT IN ('ai-gen','rewrite-v1','rewrite-v2')
        AND (content LIKE '%学习重点%理解%主题中的核心表达%'
          OR content LIKE '%关键要点%理解本主题的核心概念%'
          OR content LIKE '%本篇重点%')
        ORDER BY id ASC
        LIMIT %s
        """ % (limit or 500)

    else:  # round_num == 3
        # 第三轮：过短内容
        sql = """
        SELECT id, title, class1, class2, content
        FROM ep_news
        WHERE recycle=0 AND LENGTH(content)<2000 AND issue NOT IN ('ai-gen','rewrite-v1','rewrite-v2')
        ORDER BY LENGTH(content) ASC
        LIMIT %s
        """ % (limit or 500)

    cur.execute(sql)
    articles = cur.fetchall()
    cur.close()
    conn.close()

    return [dict(zip(['id','title','class1','class2','content'], a)) for a in articles]

# ========== LLM改写 ==========

def call_qwen(prompt, max_tokens=3000):
    """调用通义千问"""
    try:
        resp = requests.post(
            QWEN_API_URL,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": QWEN_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
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
        log.error(f"调用LLM失败: {e}")
        return None

def rewrite_article(article):
    """改写一篇文章"""
    title = article['title']
    old_content = article['content']
    class1 = article['class1']

    # 栏目名称
    category_map = {
        103: "英语阅读", 104: "英语演讲", 105: "每日英语",
        111: "KET真题解析", 112: "KET词汇速记", 113: "KET写作指导", 114: "KET听力技巧",
        121: "PET真题解析", 122: "PET词汇速记", 123: "PET写作指导", 124: "PET阅读技巧"
    }
    category = category_map.get(class1, "英语学习")

    prompt = f"""你是英语教育内容编辑。需要改写一篇文章，提升内容质量。

## 原文标题
{title}

## 栏目
{category}

## 原文内容（可能很短或质量不佳）
{old_content[:1000]}

## 改写要求
1. **保留标题不变**，直接用原标题
2. **改写正文内容**，使其满足以下标准：
   - 总字数: 1500-2500字节（改写后）
   - 包含3-5个h2小标题
   - 每个小标题下2-3段内容
   - 必须包含具体英语例句（中英对照）
   - 提供实用方法或学习建议
   - 结尾有总结+鼓励语
3. **生成新摘要**：50-80字，概括核心价值，不能和标题相同
4. **使用HTML标签**：h2/h3/p/ul/li/strong/em/blockquote
5. **不要使用Markdown**

## 输出格式（JSON）
{{
  "title": "{title}",
  "description": "50-80字摘要",
  "content": "完整HTML正文"
}}

只输出JSON，不要其他文字。"""

    raw = call_qwen(prompt)
    if not raw:
        return None

    try:
        text = raw.strip()
        if text.startswith('```'):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)

        result = json.loads(text)

        # 验证
        title_check = result.get('title', '').strip() == title
        desc = result.get('description', '').strip()
        content = result.get('content', '').strip()

        if not title_check:
            log.warning(f"标题变更: {result.get('title')} != {title}")
        if not desc or len(desc) < 30:
            log.warning(f"摘要过短: {len(desc)}字")
        if not content or len(content) < 2000:
            log.warning(f"内容过短: {len(content)}字节")

        return result

    except Exception as e:
        log.error(f"JSON解析失败: {e}\n原始: {raw[:200]}")
        return None

# ========== 数据库更新 ==========

def update_article(article_id, content, description):
    """更新文章到数据库"""
    if config.dry_run:
        log.info(f"[DRY-RUN] 将更新文章 {article_id}: {len(content)}字节内容")
        return True

    conn = pymysql.connect(**DB)
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE ep_news
            SET content=%s, description=%s, issue='rewrite-v1', updatetime=NOW()
            WHERE id=%s
        """, (content, description[:200], article_id))

        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        log.error(f"数据库更新失败 [{article_id}]: {e}")
        conn.rollback()
        cur.close()
        conn.close()
        return False

# ========== 质量检查 ==========

def validate_content(content):
    """验证改写后的内容"""
    issues = []

    # 检查长度
    if len(content) < 2000:
        issues.append(f"内容太短: {len(content)}字节")

    # 检查h2标题数量
    h2_count = len(re.findall(r'<h2>', content))
    if h2_count < 3:
        issues.append(f"h2标题过少: {h2_count}个")

    # 检查是否有HTML标签
    if not re.search(r'<(h2|h3|p|ul|li|strong|blockquote)', content):
        issues.append("缺少HTML标签")

    # 检查是否有markdown残留
    if re.search(r'^(#{1,6} |[\*\-] |\d+\. )', content, re.MULTILINE):
        issues.append("发现Markdown残留")

    return issues if issues else None

# ========== 主流程 ==========

def main():
    log.info("="*60)
    log.info(f"批量改写脚本启动 - 第{config.round}轮")
    log.info(f"参数: batch_size={config.batch_size}, parallel={config.parallel}, dry_run={config.dry_run}")
    log.info("="*60)

    # 获取待改写文章
    articles = get_low_quality_articles(config.round)

    if not articles:
        log.info("没有符合条件的文章需要改写")
        return

    log.info(f"找到 {len(articles)} 篇待改写文章")

    # 断点续传
    if config.resume_from_id:
        articles = [a for a in articles if a['id'] >= config.resume_from_id]
        log.info(f"从ID {config.resume_from_id} 继续，剩余 {len(articles)} 篇")

    # 逐批处理
    success = 0
    failed = 0
    skipped = 0

    for batch_idx, batch_start in enumerate(range(0, len(articles), config.batch_size)):
        batch = articles[batch_start:batch_start+config.batch_size]
        batch_num = batch_idx + 1

        log.info(f"\n--- 第 {batch_num} 批 ({len(batch)} 篇) ---")

        # 并行处理批次内文章
        if config.parallel > 1:
            with ThreadPoolExecutor(max_workers=config.parallel) as executor:
                futures = {}
                for article in batch:
                    future = executor.submit(process_article, article)
                    futures[future] = article

                for future in as_completed(futures):
                    article = futures[future]
                    ok = future.result()
                    if ok == 1:
                        success += 1
                    elif ok == 0:
                        failed += 1
                    else:
                        skipped += 1
        else:
            # 串行处理
            for article in batch:
                ok = process_article(article)
                if ok == 1:
                    success += 1
                elif ok == 0:
                    failed += 1
                else:
                    skipped += 1

        # 批次间隔
        if batch_idx < (len(articles) // config.batch_size):
            log.info(f"等待30秒后继续下一批...")
            time.sleep(30)

    # 统计
    log.info("\n" + "="*60)
    log.info(f"完成！成功: {success} 篇 | 失败: {failed} 篇 | 跳过: {skipped} 篇")
    log.info(f"日志: {LOG_FILE}")
    log.info("="*60)

def process_article(article):
    """处理单篇文章，返回 1=成功 0=失败 -1=跳过"""
    article_id = article['id']
    title = article['title']

    try:
        # 调用LLM改写
        log.info(f"改写 ID={article_id} 标题='{title[:30]}'...")
        result = rewrite_article(article)

        if not result:
            log.error(f"  ✗ LLM返回None")
            return 0

        content = result.get('content', '').strip()
        desc = result.get('description', '').strip()

        # 验证
        issues = validate_content(content)
        if issues:
            log.warning(f"  ⚠ 验证失败: {', '.join(issues)}")
            return -1

        # 入库
        ok = update_article(article_id, content, desc)
        if ok:
            log.info(f"  ✓ 成功: {len(content)}字节, 摘要{len(desc)}字")
            return 1
        else:
            log.error(f"  ✗ 数据库更新失败")
            return 0

    except Exception as e:
        log.error(f"  ✗ 异常: {e}")
        return 0

if __name__ == "__main__":
    main()
