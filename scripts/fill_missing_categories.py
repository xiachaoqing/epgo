#!/usr/bin/env python3
"""
为空栏目补充文章数据
"""
import pymysql
from datetime import datetime

DB = dict(
    host="127.0.0.1", port=3306,
    user="xiachaoqing", password="***REMOVED***",
    database="epgo_db", charset="utf8mb4"
)

# 106 下载、107 关于 的文章数据
ARTICLES = [
    # 106 资料下载
    {
        "class1": 106,
        "title": "KET官方真题集合（2023-2024年）",
        "content": """<h3>资料介绍</h3>
<p>本资料包含剑桥官方发布的 KET 真题集合，覆盖 2023 年至 2024 年的全部考试题型。每套真题包括：</p>
<ul>
  <li><strong>Reading and Writing Part 1-7</strong>：1400 字以内的阅读理解和短文写作</li>
  <li><strong>Listening Part 1-5</strong>：日常生活和学习场景的听力训练</li>
  <li><strong>Speaking Part 1-4</strong>：话题卡和交互式口语对话</li>
</ul>

<h3>适用人群</h3>
<ul>
  <li>计划参加 KET 考试的学生</li>
  <li>需要系统备考的英语学习者</li>
  <li>教师进行课堂教学和模拟考试</li>
</ul>

<h3>使用建议</h3>
<p>建议按照考试时间分配，每周完成一套真题模拟，并对答案进行详细复盘。重点关注错题原因分析。</p>

<h3>下载方式</h3>
<p>点击下方链接即可下载全部资料（PDF 格式，共 2.3MB）</p>
<p><strong>下载：</strong> KET_2023-2024_Real_Papers.pdf</p>
""",
        "imgurl": "/upload/epgo-photo-covers/download/cover_v1_1775645515.jpg",
    },
    {
        "class1": 106,
        "title": "PET高分词汇速记表（B1 核心 1500 词）",
        "content": """<h3>词汇分类</h3>
<p>本表按主题分类 PET 考试的核心高频词汇，共 1500 个单词，涵盖：</p>
<ul>
  <li><strong>学校与教育</strong> (80+ 词)</li>
  <li><strong>工作与职业</strong> (120+ 词)</li>
  <li><strong>日常生活与家庭</strong> (150+ 词)</li>
  <li><strong>运动与娱乐</strong> (100+ 词)</li>
  <li><strong>旅游与文化</strong> (130+ 词)</li>
  <li><strong>健康与医疗</strong> (90+ 词)</li>
  <li><strong>环境与科技</strong> (110+ 词)</li>
</ul>

<h3>使用指南</h3>
<p>每个单词配有：英文定义、中文翻译、常用搭配、例句、近义词对比。</p>

<h3>记忆技巧</h3>
<ul>
  <li>按主题分组学习，建立语境联系</li>
  <li>每天记忆 30-50 个单词，坚持复习</li>
  <li>使用单词卡或 App 进行反复训练</li>
  <li>在真题中查找单词用法，加深印象</li>
</ul>

<p><strong>下载：</strong> PET_Core_Vocabulary_1500.xlsx</p>
""",
        "imgurl": "/upload/epgo-photo-covers/download/cover_v2_1775645365.jpg",
    },
    {
        "class1": 106,
        "title": "英语演讲范文库（20篇常见话题）",
        "content": """<h3>包含话题</h3>
<ul>
  <li>我的理想职业</li>
  <li>一个有影响力的人</li>
  <li>我最难忘的经历</li>
  <li>如何保护环境</li>
  <li>学习英语的益处</li>
  <li>我喜欢的运动</li>
  <li>旅游见闻分享</li>
  <li>团队合作的重要性</li>
  <li>数字时代的生活</li>
  <li>艺术与文化欣赏</li>
</ul>

<h3>范文特点</h3>
<ul>
  <li><strong>结构清晰</strong>：开场、展开、收尾各部分完整</li>
  <li><strong>表达地道</strong>：避免中文思维直译，使用自然英文</li>
  <li><strong>难度分级</strong>：初级、中级、高级三个层次</li>
  <li><strong>高分表达</strong>：精选每篇中最实用的短语和句型</li>
</ul>

<h3>学习方式</h3>
<ol>
  <li>阅读范文，理解整体结构</li>
  <li>标记关键短语和高分表达</li>
  <li>背诵 3-5 个核心段落</li>
  <li>练习改写和创新，形成自己的表达</li>
</ol>

<p><strong>下载：</strong> Speech_Topics_20_Sample_Essays.pdf</p>
""",
        "imgurl": "/upload/epgo-photo-covers/download/cover_v3_1775645369.jpg",
    },
    # 107 关于我们
    {
        "class1": 107,
        "title": "关于我们",
        "content": """<h3>平台简介</h3>
<p>英语陪跑GO（epgo）是专注于青少年英语学习的综合平台，致力于为学习者提供系统、实用、有趣的英语学习资源和指导。</p>

<h3>我们的使命</h3>
<ul>
  <li>帮助学生掌握实用英语，适应国际化社会</li>
  <li>打破应试教育与实际应用的壁垒</li>
  <li>让英语学习变成一场愉快的旅程，而非沉重的负担</li>
  <li>提供贴近考试又超越教材的优质内容</li>
</ul>

<h3>平台特色</h3>
<ul>
  <li><strong>栏目齐全</strong>：从 KET、PET 等级考到阅读、演讲、每日表达</li>
  <li><strong>内容系统</strong>：从基础词汇到高分技巧，逐级递进</li>
  <li><strong>实战导向</strong>：真题解析、模板借鉴、高分表达速记</li>
  <li><strong>更新频繁</strong>：每周新增优质文章和学习资源</li>
</ul>

<h3>联系我们</h3>
<p>如有建议或反馈，欢迎通过以下方式联系：</p>
<ul>
  <li>微信公众号：英语陪跑GO</li>
  <li>邮箱：contact@xiachaoqing.com</li>
  <li>反馈表单：[点击这里]提交意见</li>
</ul>

<h3>致谢</h3>
<p>感谢所有在使用过程中提出建议和鼓励的用户。你们的反馈是我们不断改进和优化的动力。</p>
""",
        "imgurl": "/upload/epgo-photo-covers/about/cover_v1_1775645499.jpg",
    },
]

conn = pymysql.connect(**DB)
cur = conn.cursor()

for article in ARTICLES:
    cur.execute("""
        INSERT INTO ep_news
        (class1, title, content, imgurl, hits, updatetime, issue, recycle)
        VALUES (%s, %s, %s, %s, %s, NOW(), %s, 0)
    """, (
        article["class1"],
        article["title"],
        article["content"],
        article["imgurl"],
        15000 + __import__("random").randint(0, 35000),
        "admin"
    ))

conn.commit()
cur.close()
conn.close()

print(f"✓ 已插入 {len(ARTICLES)} 篇文章到 106/107 栏目")
