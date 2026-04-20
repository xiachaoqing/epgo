#!/usr/bin/env python3
"""
fix_all_articles.py - 一次性改写所有低质量文章
类型: 一次性脚本（跑完即弃）
作用: 将364篇低质量文章逐篇用AI改写
安全: 保留id/title/url/hits/addtime，只改content和description
断点续传: 自动记录进度，中断后重新运行会跳过已完成的
"""

import pymysql
import requests
import json
import os
import re
import time
import logging
from datetime import datetime

DB = dict(host='127.0.0.1', port=3306, user='xiachaoqing',
          password='Xia@07090218', database='epgo_db', charset='utf8mb4')

API_KEY = 'sk-63851b428d4b43cb939ab1334a8d8ed8'
API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
MODEL = 'qwen-plus'

CATEGORY = {
    103: '英语阅读', 104: '英语演讲', 105: '每日英语', 106: '资料下载', 107: '关于我们',
    111: 'KET真题解析', 112: 'KET词汇速记', 113: 'KET写作指导', 114: 'KET听力技巧',
    121: 'PET真题解析', 122: 'PET词汇速记', 123: 'PET写作指导', 124: 'PET阅读技巧',
    101: 'KET备考', 102: 'PET备考',
}

SITE_ROOT = '/www/wwwroot/go.xiachaoqing.com'
LOG_FILE = f'{SITE_ROOT}/logs/fix_all_articles.log'
STATE_FILE = f'{SITE_ROOT}/logs/fix_state.json'

os.makedirs(f'{SITE_ROOT}/logs', exist_ok=True)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
log = logging.getLogger()


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {'done_ids': [], 'failed_ids': []}


def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)


def get_articles_to_fix(done_ids):
    """查询所有需要改写的低质量文章"""
    conn = pymysql.connect(**DB)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, class1, class2, content
        FROM ep_news
        WHERE recycle=0
          AND issue NOT IN ('ai-gen', 'rewrite-v1')
          AND (
            LENGTH(content) < 4000
            OR content LIKE '%%学习重点%%理解%%主题中的核心表达%%'
            OR content LIKE '%%关键要点%%理解本主题的核心概念%%'
            OR content LIKE '%%本篇重点%%'
          )
        ORDER BY LENGTH(content) ASC
    """)
    articles = []
    for row in cur.fetchall():
        if row[0] not in done_ids:
            articles.append({
                'id': row[0], 'title': row[1],
                'class1': row[2], 'class2': row[3],
                'content': row[4]
            })
    cur.close()
    conn.close()
    return articles


def rewrite(title, class1, old_content):
    """调用通义千问改写一篇文章"""
    cat = CATEGORY.get(class1, '英语学习')

    prompt = f"""你是"英语陪跑GO"网站的资深英语教育编辑。请根据标题改写一篇高质量文章。

## 标题（不可修改）
{title}

## 栏目
{cat}

## 原文参考（质量差，需要完全重写）
{old_content[:800]}

## 改写要求
1. 围绕标题写一篇全新的、有实际教学价值的文章
2. 正文1200-2000字，必须包含：
   - 开头段：2-3句直接说清本文要解决什么问题
   - 3-5个h2小标题，每节有2-3段内容
   - 至少5个具体英语例句（中英对照，用blockquote包裹）
   - 实用的学习方法、做题步骤或记忆技巧
   - 结尾段：总结要点+鼓励语
3. 生成一个50-80字的摘要，不能和标题一样
4. 使用HTML标签：h2/p/ul/li/strong/em/blockquote
5. 不要用markdown，不要用h1

## 输出（严格JSON，不要其他文字）
{{"description":"摘要","content":"HTML正文"}}"""

    try:
        resp = requests.post(API_URL,
            headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
            json={
                'model': MODEL,
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.75,
                'max_tokens': 4000
            },
            timeout=120)

        if resp.status_code != 200:
            log.error(f'API返回 {resp.status_code}: {resp.text[:200]}')
            return None

        text = resp.json()['choices'][0]['message']['content'].strip()

        # 去掉markdown代码块包裹
        if text.startswith('```'):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)

        data = json.loads(text)
        content = data.get('content', '').strip()
        desc = data.get('description', '').strip()

        # 质量验证
        plain = re.sub(r'<[^>]+>', '', content)
        if len(plain) < 500:
            log.warning(f'内容太短 {len(plain)}字，丢弃')
            return None

        if not desc or desc == title:
            desc = plain[:80]

        return {'description': desc[:200], 'content': content}

    except json.JSONDecodeError as e:
        log.error(f'JSON解析失败: {e}')
        return None
    except Exception as e:
        log.error(f'改写异常: {e}')
        return None


def update_db(article_id, desc, content):
    """更新数据库"""
    conn = pymysql.connect(**DB)
    cur = conn.cursor()
    cur.execute("""
        UPDATE ep_news SET content=%s, description=%s, issue='rewrite-v1', updatetime=NOW()
        WHERE id=%s
    """, (content, desc, article_id))
    conn.commit()
    cur.close()
    conn.close()


def main():
    state = load_state()
    done_ids = set(state['done_ids'])

    articles = get_articles_to_fix(done_ids)
    total = len(articles)

    log.info('=' * 60)
    log.info(f'文章改写启动 | 待改写: {total} 篇 | 已完成: {len(done_ids)} 篇')
    log.info('=' * 60)

    if total == 0:
        log.info('没有需要改写的文章，全部完成！')
        return

    success = 0
    failed = 0

    for i, art in enumerate(articles):
        aid = art['id']
        title = art['title']
        log.info(f'[{i+1}/{total}] ID={aid} {title[:40]}')

        # 最多重试2次
        result = None
        for attempt in range(2):
            result = rewrite(title, art['class1'], art['content'])
            if result:
                break
            if attempt == 0:
                log.info('  重试...')
                time.sleep(3)

        if result:
            update_db(aid, result['description'], result['content'])
            log.info(f'  ✓ 完成 ({len(result["content"])}字节)')
            state['done_ids'].append(aid)
            success += 1
        else:
            log.warning(f'  ✗ 失败（2次重试后放弃）')
            state['failed_ids'].append(aid)
            failed += 1

        # 保存进度（断点续传）
        save_state(state)

        # API间隔
        time.sleep(1.5)

        # 每50篇输出进度
        if (i + 1) % 50 == 0:
            log.info(f'--- 进度: {i+1}/{total} | 成功:{success} | 失败:{failed} ---')

    # 清缓存
    os.system(f'rm -rf {SITE_ROOT}/cache/*')

    log.info('=' * 60)
    log.info(f'全部完成! 成功: {success} | 失败: {failed} | 总计: {total}')
    log.info('=' * 60)


if __name__ == '__main__':
    main()
