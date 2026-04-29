# 英语陪跑GO - 文章生成系统开发指南

> 给AI开发者的完整技术文档。目标：让每天自动生成的文章像人工编辑的爆文一样有质感。

---

## 一、现状分析

### 当前系统

| 项目 | 现状 | 问题 |
|------|------|------|
| 每日脚本 | `daily_maintain_epgo.py` cron每天2:00运行 | 内容是模板拼接，水且重复 |
| 封面图 | 7个目录共36张图片，反复使用 | 重复率高，视觉疲劳 |
| 文章内容 | 硬编码主题+模板内容 | 没有实际价值 |
| 数据库 | ep_news表，390篇活跃文章 | 大量文章内容雷同 |
| 栏目分布 | KET 131篇、PET 131篇、阅读/演讲/每日各35篇 | 子栏目严重不均 |

### 数据库结构

```sql
-- ep_news 关键字段
id          INT AUTO_INCREMENT
title       VARCHAR(100)    -- 文章标题
description VARCHAR(200)    -- 摘要（前端列表显示）
content     TEXT            -- 正文HTML
class1      INT             -- 一级分类（101=KET总 102=PET总 103=阅读 104=演讲 105=每日 106=下载 107=关于）
class2      INT             -- 二级分类（111=KET真题 112=KET词汇 113=KET写作 114=KET听力 121-124=PET对应）
imgurl      VARCHAR(255)    -- 封面图路径
hits        INT             -- 阅读数
issue       VARCHAR(50)     -- 来源标记（system/quality/premium/crawl）
updatetime  DATETIME
addtime     DATETIME
recycle     TINYINT         -- 0=正常 1=回收站
lang        VARCHAR(10)     -- cn
```

### 服务器环境

```
服务器: 101.42.21.191（腾讯云）
系统: CentOS + 宝塔面板
Web: Nginx + PHP 7.x（MetInfo CMS）
数据库: MySQL 5.7
Python: 3.x（已安装pymysql, requests, beautifulsoup4）
网站根目录: /www/wwwroot/go.xiachaoqing.com/
脚本目录: /www/wwwroot/go.xiachaoqing.com/scripts/
封面目录: /www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers/{分类}/
数据库连接: user=xiachaoqing password=Xia@07090218 db=epgo_db
```

### 前端展示规则

首页取最新9篇文章（`index.php`），卡片结构：
- 图片区：180px固定高度，`object-fit:cover`裁切
- 标题区：45px固定高度，2行截断
- 描述区：42px固定高度，2行截断
- 底部：日期 + 阅读数

**关键约束**：标题控制在20个中文字以内（避免换行），description不能等于title。

---

## 二、目标系统架构

```
┌─────────────────────────────────────────────────┐
│               每日文章生成流水线                    │
├─────────────────────────────────────────────────┤
│                                                   │
│  1. 内容采集层                                     │
│     ├─ 微信公众号爬虫（搜狗微信搜索）                │
│     ├─ 教育网站爬虫（知乎专栏、简书、百度百家号）      │
│     └─ RSS订阅源（Cambridge Blog等）                │
│                                                   │
│  2. AI改写层                                       │
│     ├─ 提取原文核心知识点                           │
│     ├─ LLM改写（保留价值，重新组织）                 │
│     ├─ 生成标题（≤20字中文）                        │
│     ├─ 生成摘要（≤90字，不等于标题）                 │
│     └─ 质量评分（≥7分才入库）                       │
│                                                   │
│  3. 封面生成层                                     │
│     ├─ 从Unsplash/Pexels下载高质量图片              │
│     ├─ 按栏目分类存储                               │
│     └─ 每篇文章独立封面（不重复）                    │
│                                                   │
│  4. 入库发布层                                     │
│     ├─ 智能分类（根据内容判断栏目）                  │
│     ├─ 设置合理阅读数（18k-42k）                    │
│     ├─ 随机化发布时间                               │
│     └─ 清理缓存                                    │
│                                                   │
└─────────────────────────────────────────────────┘
```

---

## 三、核心模块开发指南

### 3.1 内容采集模块

#### 微信公众号爬虫（搜狗微信搜索）

搜狗微信搜索是唯一能在站外搜索微信公众号文章的入口。

```python
"""
搜狗微信搜索爬虫设计要点：

URL: https://weixin.sogou.com/weixin?type=2&query={keyword}
- type=2 表示搜文章（type=1是搜公众号）

反爬策略：
- 搜狗有验证码机制，频率不能太高
- 建议每次请求间隔5-8秒
- 使用代理IP轮换
- 保存cookie，模拟登录态

解析逻辑：
- 搜索结果页的文章链接是临时的sogou中转链接
- 需要跟随302跳转获取真实的mp.weixin.qq.com链接
- 然后解析微信文章页面获取正文

推荐关键词（轮换使用）：
- KET备考技巧、PET考试攻略、剑桥英语学习
- 英语阅读方法、英语听力提升、英语词汇记忆
- 英语口语练习、英语写作技巧、英语演讲训练
"""

import requests
from bs4 import BeautifulSoup
import time
import random

class WechatCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://weixin.sogou.com/',
        })

    def search(self, keyword, max_pages=2):
        """搜索微信文章"""
        articles = []
        for page in range(1, max_pages + 1):
            url = f"https://weixin.sogou.com/weixin?type=2&query={keyword}&page={page}"

            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 302 or '验证码' in resp.text:
                    print(f"触发反爬，等待60秒...")
                    time.sleep(60)
                    continue

                soup = BeautifulSoup(resp.text, 'html.parser')

                # 搜索结果在 ul.news-list > li 中
                for item in soup.select('ul.news-list li'):
                    title_el = item.select_one('h3 a')
                    desc_el = item.select_one('p.txt-info')

                    if title_el:
                        article = {
                            'title': title_el.get_text(strip=True),
                            'url': title_el.get('href', ''),
                            'summary': desc_el.get_text(strip=True) if desc_el else '',
                        }
                        articles.append(article)

                time.sleep(random.uniform(5, 8))

            except Exception as e:
                print(f"搜索失败: {e}")

        return articles

    def fetch_article_content(self, url):
        """获取微信文章完整正文"""
        try:
            # 先跟随sogou中转链接
            resp = self.session.get(url, timeout=15, allow_redirects=True)
            soup = BeautifulSoup(resp.text, 'html.parser')

            # 微信文章正文在 div#js_content 中
            content_div = soup.select_one('#js_content')
            if content_div:
                return content_div.get_text(strip=True)
            return ''
        except Exception as e:
            print(f"获取文章失败: {e}")
            return ''
```

#### 知乎/百度爬虫

```python
"""
知乎专栏搜索：
URL: https://www.zhihu.com/search?type=content&q={keyword}
- 需要处理动态渲染（知乎是SPA）
- 建议用 requests 直接调知乎API：
  https://www.zhihu.com/api/v4/search_v3?t=general&q={keyword}

百度百家号：
URL: https://www.baidu.com/s?wd={keyword}&pn=0
- 百度搜索结果中带"百家号"标签的就是
- 直接解析搜索结果页面即可
"""
```

### 3.2 AI改写模块

这是系统的核心。把采集到的原文改写成高质量的文章。

```python
"""
LLM改写模块设计

推荐模型（按性价比排序）：
1. DeepSeek V3 - 便宜、中文好、API稳定
2. 通义千问 Qwen - 阿里云，免费额度多
3. OpenAI GPT-4o-mini - 便宜、质量好
4. Claude Haiku - 质量高

API调用示例（以DeepSeek为例）：
"""

import json
import requests

DEEPSEEK_API_KEY = "your_api_key_here"  # 存在.env文件中
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1/chat/completions"

def rewrite_article(original_content, category):
    """
    用LLM改写文章

    参数:
        original_content: 原始文章文本
        category: 栏目名称（如KET真题、PET词汇等）

    返回:
        dict: {title, description, content_html}
    """

    prompt = f"""你是一位专业的英语教育内容编辑，负责"英语陪跑GO"网站的文章。

## 原始参考内容
{original_content[:3000]}

## 要求
1. 基于上面的参考内容，写一篇全新的文章
2. 栏目：{category}
3. 文章结构要求：
   - 标题：≤20个中文字，吸引点击，不要用冒号分隔太长的标题
   - 开头段：100字左右，直接说清本文价值
   - 正文：3-5个小标题（h2），每段200-300字
   - 如果涉及语法/词汇，必须给出具体例句
   - 结尾：50字总结 + 引导关注
4. 总字数：800-1500字
5. 风格：专业但通俗，像一个有经验的老师在讲课

## 输出格式（JSON）
{{
  "title": "标题（≤20字）",
  "description": "摘要（50-80字，概括文章核心价值，不要和标题一样）",
  "content_html": "正文HTML（用h2/p/ul/li/strong/blockquote标签）"
}}

直接返回JSON，不要其他内容。"""

    try:
        resp = requests.post(
            DEEPSEEK_BASE_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 4000
            },
            timeout=60
        )

        result = resp.json()
        text = result['choices'][0]['message']['content']

        # 解析JSON
        # 去掉可能的markdown code block
        text = text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1].rsplit('```', 1)[0]

        data = json.loads(text)

        # 质量检查
        if len(data.get('title', '')) > 30:
            data['title'] = data['title'][:20]  # 截断
        if data.get('description') == data.get('title'):
            data['description'] = data['content_html'][:80] if data.get('content_html') else data['title']

        return data

    except Exception as e:
        print(f"LLM改写失败: {e}")
        return None
```

### 3.3 封面图生成模块

```python
"""
封面图策略：
1. 从Unsplash/Pexels下载高质量免费图片
2. 每个栏目维护一个图片池（≥50张）
3. 每篇文章分配独立封面
4. 图片尺寸统一裁切为 800x450（16:9）
"""

import requests
import os
import hashlib
from PIL import Image
from io import BytesIO

# Unsplash API（免费版每小时50次请求）
UNSPLASH_ACCESS_KEY = "your_access_key"  # 在 unsplash.com/developers 申请

# 每个栏目对应的搜索关键词
COVER_KEYWORDS = {
    "ket": ["english exam study", "student studying", "english test preparation", "classroom learning"],
    "pet": ["language learning", "english certificate", "academic study", "book reading"],
    "reading": ["reading book", "library", "english literature", "open book"],
    "speech": ["public speaking", "presentation", "microphone speech", "stage presentation"],
    "daily": ["morning study", "coffee study", "daily routine", "notebook writing"],
    "download": ["document download", "file folder", "digital learning", "computer education"],
    "about": ["team education", "teacher student", "school community"],
}

def download_unsplash_covers(category, count=20):
    """从Unsplash下载指定栏目的封面图"""

    save_dir = f"/www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers/{category}"
    os.makedirs(save_dir, exist_ok=True)

    keywords = COVER_KEYWORDS.get(category, ["education learning"])
    downloaded = 0

    for keyword in keywords:
        if downloaded >= count:
            break

        url = f"https://api.unsplash.com/search/photos"
        params = {
            "query": keyword,
            "per_page": 10,
            "orientation": "landscape",  # 横版图
        }
        headers = {
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=15)
            data = resp.json()

            for photo in data.get('results', []):
                if downloaded >= count:
                    break

                # 下载小尺寸版本（够用且快）
                img_url = photo['urls']['regular']  # 1080px宽

                img_resp = requests.get(img_url, timeout=30)
                if img_resp.status_code == 200:
                    # 裁切为800x450
                    img = Image.open(BytesIO(img_resp.content))
                    img = img.convert('RGB')

                    # 居中裁切为16:9
                    w, h = img.size
                    target_ratio = 800 / 450
                    current_ratio = w / h

                    if current_ratio > target_ratio:
                        new_w = int(h * target_ratio)
                        left = (w - new_w) // 2
                        img = img.crop((left, 0, left + new_w, h))
                    else:
                        new_h = int(w / target_ratio)
                        top = (h - new_h) // 2
                        img = img.crop((0, top, w, top + new_h))

                    img = img.resize((800, 450), Image.LANCZOS)

                    # 文件名用hash避免重复
                    filename = f"cover_{hashlib.md5(img_url.encode()).hexdigest()[:12]}.jpg"
                    filepath = os.path.join(save_dir, filename)

                    img.save(filepath, 'JPEG', quality=85)
                    downloaded += 1
                    print(f"  ✓ {category}/{filename}")

        except Exception as e:
            print(f"  下载失败: {e}")

    return downloaded

def get_unique_cover(class_id, used_covers=set()):
    """为文章获取一张未使用过的封面"""

    COVER_DIRS = {
        101: "ket", 102: "pet", 103: "reading", 104: "speech",
        105: "daily", 106: "download", 107: "about",
        111: "ket", 112: "ket", 113: "ket", 114: "ket",
        121: "pet", 122: "pet", 123: "pet", 124: "pet",
    }

    dir_name = COVER_DIRS.get(class_id, "daily")
    upload_dir = f"/www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers/{dir_name}"

    if not os.path.exists(upload_dir):
        return ""

    files = [f for f in os.listdir(upload_dir)
             if f.endswith('.jpg') and f.startswith('cover') and 'test' not in f]

    # 排除已使用的
    available = [f for f in files if f not in used_covers]
    if not available:
        available = files  # 全用过了就重新开始

    if available:
        chosen = random.choice(available)
        used_covers.add(chosen)
        return f"/upload/epgo-photo-covers/{dir_name}/{chosen}"

    return ""
```

### 3.4 完整流水线脚本

```python
#!/usr/bin/env python3
"""
daily_article_pipeline.py - 每日文章生成流水线

cron配置：
0 2 * * * cd /www/wwwroot/go.xiachaoqing.com && python3 scripts/daily_article_pipeline.py >> logs/pipeline.log 2>&1
"""

import os
import sys
import json
import random
import pymysql
import logging
import time
from datetime import datetime, timedelta

# 导入各模块（上面定义的）
# from crawler import WechatCrawler
# from rewriter import rewrite_article
# from cover import get_unique_cover

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
log = logging.getLogger(__name__)

DB = dict(
    host="127.0.0.1", port=3306,
    user="xiachaoqing", password="Xia@07090218",
    database="epgo_db", charset="utf8mb4"
)

# 每天生成的文章数量和分布
DAILY_PLAN = [
    {"class1": 111, "class2": 111, "count": 1, "keywords": ["KET真题", "KET考试技巧"]},
    {"class1": 112, "class2": 112, "count": 1, "keywords": ["KET词汇", "KET单词记忆"]},
    {"class1": 113, "class2": 113, "count": 1, "keywords": ["KET写作", "KET作文"]},
    {"class1": 114, "class2": 114, "count": 1, "keywords": ["KET听力", "KET听力训练"]},
    {"class1": 121, "class2": 121, "count": 1, "keywords": ["PET真题", "PET考试攻略"]},
    {"class1": 122, "class2": 122, "count": 1, "keywords": ["PET词汇", "PET单词"]},
    {"class1": 123, "class2": 123, "count": 1, "keywords": ["PET写作", "PET作文"]},
    {"class1": 124, "class2": 124, "count": 1, "keywords": ["PET阅读", "PET阅读理解"]},
    {"class1": 103, "class2": 0,   "count": 1, "keywords": ["英语阅读方法", "英语阅读技巧"]},
    {"class1": 104, "class2": 0,   "count": 1, "keywords": ["英语演讲", "英语口语表达"]},
    {"class1": 105, "class2": 0,   "count": 2, "keywords": ["每日英语", "英语学习打卡", "英语日常表达"]},
]

# 栏目名称映射
CATEGORY_NAMES = {
    111: "KET真题解析", 112: "KET词汇速记", 113: "KET写作指导", 114: "KET听力技巧",
    121: "PET真题解析", 122: "PET词汇速记", 123: "PET写作指导", 124: "PET阅读技巧",
    103: "英语阅读", 104: "英语演讲", 105: "每日英语",
}

def run_pipeline():
    """主流水线"""

    log.info("=" * 50)
    log.info("开始每日文章生成流水线")
    log.info("=" * 50)

    conn = pymysql.connect(**DB)
    total_added = 0
    used_covers = set()

    for plan in DAILY_PLAN:
        keyword = random.choice(plan['keywords'])
        category_name = CATEGORY_NAMES.get(plan['class1'], "英语学习")

        for i in range(plan['count']):
            log.info(f"\n--- {category_name} ({i+1}/{plan['count']}) ---")

            # 第一步：采集
            log.info(f"采集: 搜索 '{keyword}'")
            # crawler = WechatCrawler()
            # articles = crawler.search(keyword, max_pages=1)
            # if articles:
            #     source_text = crawler.fetch_article_content(articles[0]['url'])
            # else:
            #     source_text = ""
            source_text = ""  # 占位：等爬虫模块完成后替换

            # 第二步：AI改写
            log.info("改写: 调用LLM...")
            # result = rewrite_article(source_text or keyword, category_name)
            result = None  # 占位：等LLM模块完成后替换

            if not result:
                log.warning("改写失败，使用备用内容")
                # 这里放备用的内容生成逻辑
                continue

            # 第三步：获取封面
            cover = get_unique_cover(plan['class1'], used_covers)

            # 第四步：入库
            hits = random.randint(18000, 42000)
            pub_time = datetime.now() - timedelta(
                hours=random.randint(1, 12),
                minutes=random.randint(0, 59)
            )

            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO ep_news
                    (title, description, content, class1, class2, class3, imgurl, hits, issue, updatetime, addtime, lang, recycle)
                    VALUES (%s, %s, %s, %s, %s, 0, %s, %s, 'pipeline', %s, %s, 'cn', 0)
                """, (
                    result['title'][:100],
                    result['description'][:200],
                    result['content_html'],
                    plan['class1'],
                    plan.get('class2', 0),
                    cover,
                    hits,
                    pub_time,
                    pub_time
                ))
                conn.commit()
                total_added += 1
                log.info(f"✓ 入库: {result['title'][:30]}")
            except Exception as e:
                log.error(f"入库失败: {e}")
            finally:
                cur.close()

            time.sleep(2)  # 间隔

    conn.close()

    # 清缓存
    os.system("rm -rf /www/wwwroot/go.xiachaoqing.com/cache/*")

    log.info(f"\n{'=' * 50}")
    log.info(f"完成！今日生成 {total_added} 篇文章")
    log.info(f"{'=' * 50}")

if __name__ == "__main__":
    run_pipeline()
```

---

## 四、分步实施计划

### 第一阶段：封面图扩充（最简单、见效最快）

**做什么：** 从Unsplash下载每个栏目50张高质量封面图

**需要：**
- 注册Unsplash开发者账号（免费）：https://unsplash.com/developers
- 获取Access Key
- 运行封面下载脚本

**验收标准：**
- 每个栏目≥50张独立封面
- 图片尺寸统一800x450
- 连续30天内首页不出现重复封面

### 第二阶段：LLM改写接入

**做什么：** 接入DeepSeek或通义千问API，实现自动改写

**需要：**
- 注册DeepSeek（https://platform.deepseek.com）或通义千问API
- 在服务器创建 `.env` 文件存放API Key
- 安装python-dotenv：`pip3 install python-dotenv`

**核心提示词已在3.2节提供。**

**验收标准：**
- 每篇文章800-1500字
- 标题≤20字中文
- 描述≠标题
- 内容有实际教学价值（有例句、有步骤、有建议）

### 第三阶段：爬虫采集

**做什么：** 从微信公众号和知乎获取高质量参考内容

**需要：**
- 代理IP服务（可选，避免被封）
- 安装beautifulsoup4：`pip3 install beautifulsoup4`

**核心代码已在3.1节提供。**

**验收标准：**
- 每天能采集10-20篇参考文章
- 不被反爬封IP
- 采集内容覆盖所有栏目

### 第四阶段：完整流水线

**做什么：** 将采集→改写→封面→入库串联成自动流水线

**替换当前的crontab：**
```bash
# 旧的（删除）
# 0 2 * * * python3 scripts/daily_maintain_epgo.py

# 新的
0 2 * * * cd /www/wwwroot/go.xiachaoqing.com && python3 scripts/daily_article_pipeline.py >> logs/pipeline.log 2>&1
```

---

## 五、质量控制标准

### 文章质量评分表

| 维度 | 7分（合格） | 9分（优秀） |
|------|-----------|-----------|
| 标题 | 清晰表达主题 | 有吸引力，让人想点击 |
| 开头 | 说清文章内容 | 直击痛点，引发共鸣 |
| 结构 | 有小标题分段 | 层层递进，逻辑清晰 |
| 内容 | 有基本知识点 | 有例句、有方法、有练习 |
| 实用性 | 读完有收获 | 读完能直接用 |

### 标题规范

```
✅ 好标题（≤20字）：
- KET听力满分的5个关键习惯
- 3周搞定PET核心词汇
- 英语演讲开场白万能公式

❌ 差标题（太长/太水）：
- KET听力Part 1-4技巧详解：从基础到高分完全攻略（29字，太长）
- 英语学习方法分享（太泛）
- PET考试技巧总结（没有吸引力）
```

### description规范

```
✅ 好摘要：
标题: "3周搞定PET核心词汇"
摘要: "用联想记忆法+间隔复习，每天30分钟，3周掌握500个PET高频词。附完整词汇表和记忆卡片。"

❌ 差摘要：
标题: "3周搞定PET核心词汇"
摘要: "3周搞定PET核心词汇"  ← 和标题一样！
```

---

## 六、文件清单

```
scripts/
├── daily_article_pipeline.py    # 主流水线（替代daily_maintain_epgo.py）
├── crawler_wechat.py            # 微信公众号爬虫
├── crawler_zhihu.py             # 知乎爬虫（可选）
├── rewriter_llm.py              # LLM改写模块
├── cover_downloader.py          # 封面图下载模块
├── fix_all_articles.py          # 一次性修复脚本（已完成）
└── README.md                    # 脚本说明

.env（不提交git）:
  DEEPSEEK_API_KEY=sk-xxx
  UNSPLASH_ACCESS_KEY=xxx
  DB_PASSWORD=Xia@07090218
```

---

## 七、注意事项

1. **密码安全**：所有密码放`.env`文件，不要硬编码在脚本里。`.env`已在`.gitignore`中。
2. **爬虫礼仪**：请求间隔≥5秒，不要大量爬取同一网站。
3. **LLM成本**：DeepSeek大约0.002元/篇，每天13篇≈0.03元，月成本<1元。
4. **图片版权**：Unsplash和Pexels的图片都是免费商用的。
5. **备用方案**：如果爬虫或LLM失败，保留当前模板系统作为fallback。
6. **监控**：检查`logs/pipeline.log`确认每天正常运行。

---

*文档版本: v1.0 | 更新日期: 2026-04-15*
