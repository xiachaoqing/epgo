#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语陪跑GO - 每日文章自动生成脚本
每天运行，为各栏目生成10篇左右高质量文章
用法: python3 daily_articles_epgo.py
Crontab: 0 7 * * * /usr/bin/python3 /root/scripts/daily_articles_epgo.py >> /root/logs/epgo_articles.log 2>&1
"""

import pymysql
import random
import time
from datetime import datetime

# 数据库配置
DB = dict(
    host='127.0.0.1',
    user='xiachaoqing',
    password='07090218',
    db='epgo_db',
    charset='utf8mb4',
    port=3306
)

# 栏目ID（bigclass=0为一级，子栏目填父ID）
COLUMNS = {
    'ket':        101,   # KET备考（父栏目）
    'ket_exam':   111,   # KET真题解析
    'ket_word':   112,   # KET词汇速记
    'ket_write':  113,   # KET写作指导
    'ket_listen': 114,   # KET听力技巧
    'pet':        102,   # PET备考（父栏目）
    'pet_exam':   121,   # PET真题解析
    'pet_word':   122,   # PET词汇速记
    'pet_write':  123,   # PET写作指导
    'pet_read':   124,   # PET阅读技巧
    'reading':    103,   # 英语阅读
    'speech':     104,   # 英语演讲
    'daily':      105,   # 每日英语
}

# ============================================================
# 文章模板库（每次随机选取，组合生成10篇）
# ============================================================

TEMPLATES = [

    # --- KET真题解析 ---
    {
        'col': 'ket_exam',
        'titles': [
            'KET阅读Part {n}真题解析：{year}年{month}月考试',
            'KET {year}年{month}月真题：Writing Part {n}评分标准详解',
            'KET听力Part {n}答题技巧：{year}年真题精析',
        ],
        'content_fn': lambda title: f'''<p>{title}是KET考试中的重要板块。本文结合最新真题，详细拆解解题思路与答题策略。</p>

<h3>题型特点</h3>
<p>该部分主要考察考生在真实语境中理解英语的能力，包括对短文、对话、邮件等体裁的理解。</p>
<ul>
  <li><strong>题量：</strong>5-8题，每题1-2分</li>
  <li><strong>时间建议：</strong>每题不超过2分钟</li>
  <li><strong>难度：</strong>A2-B1级别</li>
</ul>

<h3>真题示例与解析</h3>
<p>以下是近期考试中的典型题目结构：</p>
<blockquote>
<p><em>Text: "The library will be closed on Saturday for maintenance. It will reopen on Monday at 9 a.m."</em></p>
<p><strong>Q: When will the library be open again?</strong></p>
<p>A) Saturday morning &nbsp; B) Sunday afternoon &nbsp; C) Monday morning</p>
</blockquote>
<p><strong>答案：C</strong> — 关键词"reopen on Monday at 9 a.m."直接对应答案，注意"9 a.m."即上午，对应"morning"。</p>

<h3>高分策略</h3>
<ol>
  <li><strong>先读题后读文</strong>：带着问题去文中定位，节省时间</li>
  <li><strong>关注时间、地点、人物</strong>：这三类信息最常考</li>
  <li><strong>注意同义替换</strong>：答案通常不原文复制，要理解语义</li>
  <li><strong>排除法</strong>：先排除明显错误选项，再在剩余中判断</li>
</ol>

<h3>备考练习建议</h3>
<p>建议每天练习1-2套真题，重点关注错题分析。可使用官方Cambridge English网站的免费练习题资源。</p>
<p>掌握{title}的解题规律后，在正式考试中可以节省大量时间，将精力分配到更难的题目上。</p>''',
    },

    # --- KET词汇速记 ---
    {
        'col': 'ket_word',
        'titles': [
            'KET核心词汇Day{n}：{topic}类高频词{num}个',
            'KET考试必背：{topic}场景词汇完整版',
            '用思维导图记KET词汇：{topic}主题词群一网打尽',
        ],
        'content_fn': lambda title: f'''<p>词汇是KET考试的基础。本文精选高频{title.split("：")[-1] if "：" in title else "核心"}词汇，配合例句帮助记忆。</p>

<h3>核心词汇列表</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;">
<tr style="background:#EFF6FF;"><th>单词</th><th>词性</th><th>中文</th><th>例句</th></tr>
<tr><td>appointment</td><td>n.</td><td>预约；约会</td><td>I have a doctor's <em>appointment</em> at 3 p.m.</td></tr>
<tr><td>available</td><td>adj.</td><td>可获得的；有空的</td><td>Are you <em>available</em> this weekend?</td></tr>
<tr><td>convenient</td><td>adj.</td><td>方便的；便利的</td><td>Is it <em>convenient</em> to call you now?</td></tr>
<tr><td>recommend</td><td>v.</td><td>推荐；建议</td><td>I would <em>recommend</em> visiting the museum.</td></tr>
<tr><td>surprised</td><td>adj.</td><td>惊讶的</td><td>She was <em>surprised</em> by the gift.</td></tr>
<tr><td>direction</td><td>n.</td><td>方向；指示</td><td>Can you give me <em>directions</em> to the station?</td></tr>
<tr><td>journey</td><td>n.</td><td>旅程；旅行</td><td>The <em>journey</em> took about two hours.</td></tr>
<tr><td>immediately</td><td>adv.</td><td>立刻；马上</td><td>Please reply <em>immediately</em>.</td></tr>
</table>

<h3>记忆技巧</h3>
<p><strong>方法1：场景联想</strong> — 将单词放入真实场景中记忆，比如把 appointment/available/convenient 组合成"预约场景三件套"。</p>
<p><strong>方法2：词根词缀</strong> — recommend (re-再 + commend 推荐) = 反复推荐；immediately (immediate 立即的 + -ly 副词后缀)。</p>
<p><strong>方法3：例句造句</strong> — 用每个单词自己造一个与日常生活相关的句子。</p>

<h3>练习题</h3>
<p>用上面的词汇填空：</p>
<ol>
  <li>I made an ______ with my dentist for Tuesday. (appointment)</li>
  <li>Is 2 o'clock ______ for you? (convenient)</li>
  <li>The teacher ______ reading English novels every day. (recommended)</li>
</ol>

<p>建议每天学习15-20个新词，配合复习之前的词汇，坚持30天词汇量可提升500+。</p>''',
    },

    # --- KET写作指导 ---
    {
        'col': 'ket_write',
        'titles': [
            'KET写作高分模板：{topic}类邮件万能框架',
            'KET Writing Part 2：{topic}场景邮件范文+解析',
            'KET写作常见失分点：{num}个错误你一定要避免',
        ],
        'content_fn': lambda title: f'''<p>KET写作部分要求在25分钟内完成约100字的邮件，本文提供{title.split("：")[-1] if "：" in title else "高分"}写作框架与范文。</p>

<h3>写作结构模板</h3>
<pre style="background:#F8FAFC;padding:16px;border-radius:8px;line-height:1.8;">
Dear [Name / Sir / Madam],

[开头句] Thank you for your email. / I am writing to...

[要点1] First, I would like to tell you that...
[要点2] Also, ...
[要点3] Finally, ...

[结尾句] I hope to hear from you soon. / Looking forward to your reply.

Best wishes,
[Your name]
</pre>

<h3>高分范文示例</h3>
<blockquote style="background:#EFF6FF;padding:16px;border-left:4px solid #2563EB;border-radius:4px;">
<p><strong>题目：</strong>你的外国朋友想了解你的学校。请写一封邮件，介绍：① 学校位置 ② 最喜欢的课程 ③ 课后活动</p>
<p><strong>范文：</strong></p>
<p>Dear Tom,</p>
<p>Thanks for your email! I'm happy to tell you about my school.</p>
<p>My school is in the centre of the city, near the main park. It's easy to get there by bus.</p>
<p>My favourite subject is English because our teacher makes it very interesting. We also have maths, science and art.</p>
<p>After school, I usually join the basketball club on Tuesdays and Thursdays. We also have a music group that meets on Fridays.</p>
<p>Hope you can visit one day!</p>
<p>Best wishes,<br>Li Ming</p>
</blockquote>

<h3>评分要点</h3>
<ul>
  <li>✅ 覆盖全部3个要点（各占分）</li>
  <li>✅ 字数在90-110字之间</li>
  <li>✅ 使用连接词 (first, also, finally, because)</li>
  <li>✅ 语法正确，拼写无误</li>
  <li>✅ 格式正确（称呼、结尾语）</li>
</ul>

<h3>常见扣分项</h3>
<p>❌ 漏掉某个要点 — 每漏一点扣2-3分</p>
<p>❌ 字数不足80字或超过120字</p>
<p>❌ 拼写错误超过3个</p>
<p>❌ 使用中文或拼音</p>''',
    },

    # --- PET词汇 ---
    {
        'col': 'pet_word',
        'titles': [
            'PET B1词汇精讲：{topic}主题高频词{num}个',
            'PET考试同义替换大全：{topic}类词汇对照表',
            'PET阅读提速：{num}组必背同义词让你秒懂文章',
        ],
        'content_fn': lambda title: f'''<p>PET考试(B1级别)对词汇量要求约2500-3000个，本文聚焦{title.split("：")[-1] if "：" in title else "核心"}词汇的深度掌握。</p>

<h3>核心词汇精讲</h3>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;">
<tr style="background:#F0FDF4;"><th>单词</th><th>释义</th><th>近义词</th><th>考试用法</th></tr>
<tr><td>achieve</td><td>v. 实现；达到</td><td>accomplish, attain</td><td>achieve goals / achieve success</td></tr>
<tr><td>attempt</td><td>v/n. 尝试；努力</td><td>try, endeavour</td><td>attempt to do / make an attempt</td></tr>
<tr><td>benefit</td><td>n/v. 好处；受益</td><td>advantage, profit</td><td>benefit from / health benefits</td></tr>
<tr><td>challenge</td><td>n. 挑战；困难</td><td>difficulty, obstacle</td><td>face challenges / challenging task</td></tr>
<tr><td>consider</td><td>v. 考虑；认为</td><td>think about, regard</td><td>consider doing / consider sb. as</td></tr>
<tr><td>describe</td><td>v. 描述；形容</td><td>explain, depict</td><td>describe how/what / description</td></tr>
<tr><td>effective</td><td>adj. 有效的</td><td>efficient, successful</td><td>effective method / be effective in</td></tr>
<tr><td>experience</td><td>n/v. 经历；体验</td><td>encounter, undergo</td><td>gain experience / personal experience</td></tr>
</table>

<h3>同义替换练习</h3>
<p>PET阅读中经常用同义词替换原文表达，练习识别：</p>
<ul>
  <li>The project was <strong>completed</strong> → <em>finished / accomplished</em></li>
  <li>She was <strong>happy</strong> about the news → <em>pleased / delighted / thrilled</em></li>
  <li>It was a <strong>difficult</strong> task → <em>challenging / demanding / tough</em></li>
  <li>He <strong>decided</strong> to leave → <em>chose to / made up his mind to</em></li>
</ul>

<h3>搭配记忆法</h3>
<p>词汇+固定搭配一起记，在写作中更自然：</p>
<pre style="background:#F8FAFC;padding:12px;border-radius:6px;">
achieve + success/goals/results/dreams
make + progress/effort/decision/mistake
take + part/advantage/care/notice
give + advice/information/help/permission
</pre>''',
    },

    # --- 英语阅读 ---
    {
        'col': 'reading',
        'titles': [
            '英语阅读技巧：{topic}类文章的5个快速理解方法',
            '每日英语阅读：{topic}主题短文精读+词汇讲解',
            '英语阅读提速：从{n}分钟读完一篇文章开始',
        ],
        'content_fn': lambda title: f'''<p>提升英语阅读能力是学好英语的关键。本文介绍{title.split("：")[-1] if "：" in title else "实用的"}阅读技巧，帮助你读得更快、理解更准。</p>

<h3>阅读前：建立预期</h3>
<p>在正式阅读前，先花30秒扫描：</p>
<ul>
  <li>标题和副标题 — 了解主题</li>
  <li>每段首句 — 把握文章结构</li>
  <li>图表/数字 — 重要信息往往在此</li>
</ul>

<h3>今日精读文章</h3>
<blockquote style="background:#F0F9FF;padding:16px;border-left:4px solid #0EA5E9;border-radius:4px;font-style:normal;">
<p><strong>The Benefits of Reading in English</strong></p>
<p>Reading is one of the most effective ways to improve your English. When you read regularly, you naturally absorb new vocabulary, grammar patterns, and expressions without even realising it.</p>
<p>Research shows that students who read for just 20 minutes a day in their target language improve their vocabulary by an average of 1,000 new words per year. That's the power of <strong>extensive reading</strong>.</p>
<p>The key is to choose materials at the right level — not too easy (boring) and not too difficult (frustrating). Start with graded readers, news websites designed for learners, or topics you are already interested in.</p>
</blockquote>

<h3>词汇讲解</h3>
<ul>
  <li><strong>absorb</strong> (v.) — 吸收；不知不觉学到 → "absorb new vocabulary"</li>
  <li><strong>naturally</strong> (adv.) — 自然地；不刻意地</li>
  <li><strong>extensive reading</strong> — 泛读（大量阅读，不求精）vs intensive reading（精读）</li>
  <li><strong>graded readers</strong> — 分级读物（按词汇量级别分类的英语读本）</li>
  <li><strong>frustrating</strong> (adj.) — 令人沮丧的；令人沮丧的</li>
</ul>

<h3>阅读后：巩固记忆</h3>
<ol>
  <li>用自己的话复述文章大意（1-2句）</li>
  <li>记下3-5个新词，用造句法巩固</li>
  <li>思考：文章的主要观点是什么？你同意吗？</li>
</ol>

<p>推荐每天坚持阅读15-20分钟，1个月后你会明显感受到阅读速度和理解力的提升。</p>''',
    },

    # --- 每日英语 ---
    {
        'col': 'daily',
        'titles': [
            '每日英语 | {month}月{day}日：{topic}的地道表达',
            '每日一句 | 今日金句：{quote_topic}',
            '每日英语 | 实用口语：{topic}怎么用英文说',
        ],
        'content_fn': lambda title: f'''<p>坚持每天学一点，英语进步看得见。今天的主题：{title.split("：")[-1] if "：" in title else "实用英语表达"}。</p>

<h3>今日核心表达</h3>
<table border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse;width:100%;">
<tr style="background:#FFF7ED;"><th>中文</th><th>英文表达</th><th>使用场景</th></tr>
<tr><td>我昨天睡过头了</td><td>I overslept yesterday.</td><td>解释迟到原因</td></tr>
<tr><td>没关系，不用担心</td><td>No worries / Don't worry about it.</td><td>安慰别人</td></tr>
<tr><td>我完全同意</td><td>I couldn't agree more.</td><td>表达强烈赞同</td></tr>
<tr><td>稍等一下</td><td>Hold on a second. / Give me a moment.</td><td>请人稍候</td></tr>
<tr><td>就是这个意思</td><td>Exactly. / That's exactly what I mean.</td><td>确认理解</td></tr>
</table>

<h3>今日金句</h3>
<blockquote style="background:#FFFBEB;padding:16px;border-left:4px solid #F59E0B;border-radius:4px;">
<p style="font-size:18px;font-style:italic;">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
<p>— Dr. Seuss</p>
<p><strong>译文：</strong>读的书越多，知道的事情就越多；学到的东西越多，你能去的地方就越远。</p>
</blockquote>

<h3>5分钟口语练习</h3>
<p>大声朗读以下对话，注意语调和节奏：</p>
<pre style="background:#F8FAFC;padding:14px;border-radius:8px;line-height:2;">
A: Hey, are you free this weekend?
B: I think so. What did you have in mind?
A: I was thinking we could check out that new café near the library.
B: That sounds great! What time were you thinking?
A: How about Saturday around 2?
B: Perfect. I'll see you then!
</pre>

<h3>今日作业</h3>
<p>用今天学到的3个表达，各造一个关于自己日常生活的句子，写在评论区或笔记本上。坚持21天，这些表达就会变成你的语言习惯！</p>''',
    },

    # --- 英语演讲 ---
    {
        'col': 'speech',
        'titles': [
            '英语演讲技巧：{topic}的{num}个实用方法',
            '演讲稿模板：{topic}主题开场白万能句型',
            '学生英语演讲范文：{topic}（附中英对照）',
        ],
        'content_fn': lambda title: f'''<p>英语演讲不只是语言能力的体现，更是思维和表达的综合展示。本文围绕{title.split("：")[-1] if "：" in title else "演讲技巧"}展开详细讲解。</p>

<h3>结构框架</h3>
<p>一篇好的英语演讲通常遵循以下结构：</p>
<ol>
  <li><strong>Hook（钩子）</strong>：引人入胜的开场（问题/故事/数据）</li>
  <li><strong>Thesis（论点）</strong>：明确说明演讲核心观点</li>
  <li><strong>Body（主体）</strong>：2-3个支撑论点，配例证</li>
  <li><strong>Conclusion（结尾）</strong>：总结+行动号召</li>
</ol>

<h3>经典开场句型</h3>
<pre style="background:#F8FAFC;padding:14px;border-radius:8px;line-height:2.2;">
1. "Have you ever wondered why...?"   （你有没有想过为什么...？）
2. "Imagine a world where..."         （想象一个...的世界）
3. "According to a recent study..."   （根据最新研究...）
4. "I'd like to start with a story..." （我想以一个故事开始）
5. "Today, I'm going to talk about..."（今天，我将讲述...）
</pre>

<h3>范文片段赏析</h3>
<blockquote style="background:#F0F9FF;padding:16px;border-left:4px solid #2563EB;border-radius:4px;">
<p><strong>主题：The Importance of Learning English</strong></p>
<p>"Good morning, everyone. Have you ever missed an opportunity simply because you couldn't express yourself in English? I have — and that moment changed my life.</p>
<p>Today, I want to share three reasons why learning English is not just useful, but essential in the 21st century..."</p>
</blockquote>

<h3>克服紧张的5个技巧</h3>
<ul>
  <li>✅ <strong>充分准备</strong>：熟悉内容，减少临场记忆压力</li>
  <li>✅ <strong>深呼吸</strong>：上台前做3次深呼吸，降低心率</li>
  <li>✅ <strong>眼神接触</strong>：与听众建立连接，不要只盯着稿子</li>
  <li>✅ <strong>语速放慢</strong>：紧张时容易语速加快，有意识减速</li>
  <li>✅ <strong>接受不完美</strong>：说错一个词没关系，继续往前说</li>
</ul>''',
    },
]

# 随机化内容的填充变量
TOPICS = ['日常交流', '学校生活', '旅行出行', '购物消费', '健康饮食', '科技数码', '文化艺术', '体育运动', '环境保护', '职业规划']
MONTHS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
YEARS  = ['2024', '2025', '2026']
NUMS   = ['5', '6', '7', '8', '10', '12', '15', '20', '30', '50', '100']


def fill_title(title_tpl):
    now = datetime.now()
    return (title_tpl
        .replace('{topic}', random.choice(TOPICS))
        .replace('{month}', now.strftime('%m').lstrip('0'))
        .replace('{day}', now.strftime('%d').lstrip('0'))
        .replace('{year}', str(now.year))
        .replace('{n}', str(random.randint(1, 5)))
        .replace('{num}', random.choice(NUMS))
        .replace('{quote_topic}', random.choice(['坚持学习', '勇于尝试', '享受过程', '保持好奇']))
    )


def get_desc(content: str, max_len=120) -> str:
    """从 content 提取纯文本描述"""
    import re
    text = re.sub(r'<[^>]+>', '', content)
    text = ' '.join(text.split())
    return text[:max_len]


def article_exists(cur, title: str) -> bool:
    cur.execute('SELECT id FROM ep_news WHERE title=%s LIMIT 1', (title,))
    return cur.fetchone() is not None


def insert_article(cur, title, content, desc, col_id):
    now_ts = int(time.time())
    # 随机分散到当天不同时间（避免同一秒）
    now_ts -= random.randint(0, 3600)
    cur.execute('''
        INSERT INTO ep_news
          (title, content, description, keywords, class1, lang, wap_ok, hits, addtime, updatetime)
        VALUES
          (%s, %s, %s, %s, %s, 1, 1, 0, %s, %s)
    ''', (title, content, desc, title[:80], col_id, now_ts, now_ts))


def main():
    conn = pymysql.connect(**DB)
    cur = conn.cursor()

    today = datetime.now().strftime('%Y-%m-%d')
    print(f'[{today}] 开始生成每日文章...')

    generated = 0
    target = 10

    # 随机打乱模板顺序
    random.shuffle(TEMPLATES)

    for tpl in TEMPLATES:
        if generated >= target:
            break
        col_id = COLUMNS.get(tpl['col'])
        if col_id is None:
            continue

        # 每个模板随机选一个标题
        title_tpl = random.choice(tpl['titles'])
        title = fill_title(title_tpl)

        # 防重
        if article_exists(cur, title):
            # 换个变量再试一次
            title = fill_title(title_tpl)
            if article_exists(cur, title):
                continue

        content = tpl['content_fn'](title)
        desc = get_desc(content)

        try:
            insert_article(cur, title, content, desc, col_id)
            conn.commit()
            print(f'  ✓ [{tpl["col"]}] {title}')
            generated += 1
        except Exception as e:
            print(f'  ✗ 插入失败: {e}')
            conn.rollback()

        time.sleep(0.1)

    cur.close()
    conn.close()
    print(f'[{today}] 完成，共生成 {generated} 篇文章')


if __name__ == '__main__':
    main()
