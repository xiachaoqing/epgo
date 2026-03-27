#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量补充所有栏目文章，重点填充PET子栏目和空栏目
直接在服务器上运行：python3 /tmp/fill_all_columns.py
"""
import sys, time
from datetime import datetime

try:
    import pymysql
except ImportError:
    import subprocess
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'pymysql', '-q'])
    import pymysql

DB = dict(host='127.0.0.1', user='xiachaoqing',
          password='07090218', db='epgo_db', charset='utf8mb4')

# 栏目ID
COL = {
    'ket_exam':   111, 'ket_word':  112, 'ket_write': 113, 'ket_listen': 114,
    'pet_exam':   121, 'pet_word':  122, 'pet_write': 123, 'pet_read':   124,
    'reading':    103, 'daily':     105, 'speech':    104,
}

NOW = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

ARTICLES = [
    # ── PET真题解析 ─────────────────────────────────────────
    {'col': 'pet_exam', 'title': 'PET 2024年阅读真题解析：Part 3长文阅读技巧',
     'desc': 'PET阅读Part3考察长文理解，本文逐题拆解2024年真题，讲清解题思路。',
     'content': '''<h2>PET 2024年阅读真题解析：Part 3长文阅读技巧</h2>
<p>PET（Cambridge B1 Preliminary）Reading Part 3是阅读中难度最高的部分，共5题，文章约450字，考查深层理解能力。</p>
<h2>一、题型特点</h2>
<ul><li>文章体裁：新闻报道、人物介绍、科普文章</li>
<li>题量：5道四选一</li>
<li>时间建议：12分钟</li></ul>
<h2>二、真题示例分析</h2>
<blockquote>Question: Why did Maria decide to change her career?<br>
A. She earned too little money.<br>
B. She wanted more free time.<br>
C. She felt unfulfilled in her job.<br>
D. Her boss suggested a change.</blockquote>
<p><strong>解析：</strong>原文关键句：<em>"Although the salary was good, she never felt truly happy at work."</em>
答案选C——"unfulfilled"对应"never felt truly happy"，这是同义替换，PET最常考的考点。</p>
<h2>三、同义替换是核心</h2>
<p>PET选项几乎不会原文照搬，而是用不同词表达相同意思：</p>
<ul>
<li>原文 <em>earn a living</em> → 选项 <em>make money</em></li>
<li>原文 <em>children</em> → 选项 <em>young people</em></li>
<li>原文 <em>refused</em> → 选项 <em>said no</em></li>
</ul>
<h2>四、备考方法</h2>
<ol>
<li>先读问题，带问题读文章</li>
<li>找关键句段，不用全文精读</li>
<li>警惕"正确信息、错误答案"的陷阱</li>
<li>每天练1篇真题阅读，积累词汇</li>
</ol>
<hr>
<p>关注<strong>英语陪跑Go</strong>，每天PET备考干货持续更新。</p>'''},

    {'col': 'pet_exam', 'title': 'PET听力考试全解析：5个Part各有什么坑',
     'desc': 'PET听力共5部分，难度层层递进。本文逐一拆解题型，给出防坑策略。',
     'content': '''<h2>PET听力考试全解析：5个Part各有什么坑</h2>
<p>PET听力时长约35分钟，共5个部分25道题。很多考生丢分不是因为听不懂，而是掉入了设计好的陷阱。</p>
<h2>Part 1 – 图片选择（7题）</h2>
<p>听短对话，从3张图片中选正确的一张。</p>
<p><strong>坑：</strong>干扰项会先提到，正确答案在对话结尾才确认。要听到最后再选！</p>
<h2>Part 2 – 填空（6题）</h2>
<p>听一段讲话，填写缺失的信息（数字、名字、时间）。</p>
<p><strong>坑：</strong>说话者会更正信息，如"It starts at 7… sorry, 7:30"，要写7:30。</p>
<h2>Part 3 – 选择（6题）</h2>
<p>较长对话，选择正确答案。</p>
<p><strong>坑：</strong>选项中会有真实提到的词，但组合错误。要理解句意，不能只抓词。</p>
<h2>Part 4 – 判断（6题）</h2>
<p>听访谈，判断每句说法是对（A）还是错（B）。</p>
<p><strong>坑：</strong>说话者的语气很重要——如"I suppose it's okay"其实表示不满意。</p>
<h2>通用策略</h2>
<ul>
<li>听之前用10秒预读选项</li>
<li>第一遍尽量选出答案，第二遍验证</li>
<li>记住：每段听两遍，不要第一遍就慌</li>
</ul>
<hr><p>关注<strong>英语陪跑Go</strong>，每天备考不焦虑。</p>'''},

    {'col': 'pet_exam', 'title': 'PET口语考试备考指南：Partner Task怎么做',
     'desc': 'PET口语有两考生搭档完成任务，很多人不知道怎么配合。本文详解备考重点。',
     'content': '''<h2>PET口语考试备考指南：Partner Task怎么做</h2>
<p>PET口语考试共4部分，约12-17分钟，两名考生同时参加。其中Part 3和Part 4需要考生互动，是最具特色的部分。</p>
<h2>四个部分简介</h2>
<ol>
<li><strong>Part 1（2分钟）</strong>：考官提问，回答个人信息，如家庭、爱好、学习等。</li>
<li><strong>Part 2（2-3分钟/人）</strong>：每人描述一张图片1分钟，然后回答关于另一张图的问题。</li>
<li><strong>Part 3（3分钟）</strong>：两考生共同讨论一个任务（如做计划、讨论选项）。</li>
<li><strong>Part 4（3分钟）</strong>：考官就Part 3话题继续提问，两考生共同回答。</li>
</ol>
<h2>Partner Task关键技巧</h2>
<ul>
<li><strong>主动开启话题：</strong><em>"What do you think about...?"</em></li>
<li><strong>表达同意：</strong><em>"That's a good point."</em> / <em>"I agree with you."</em></li>
<li><strong>表达不同意见：</strong><em>"I see your point, but..."</em></li>
<li><strong>邀请对方发言：</strong><em>"What about you?"</em> / <em>"Do you think so?"</em></li>
<li><strong>做出决定：</strong><em>"So, shall we go with...?"</em></li>
</ul>
<h2>常见错误</h2>
<ul>
<li>一人说太多，不给搭档说话机会</li>
<li>直接说"Yes/No"不解释原因</li>
<li>沉默超过5秒</li>
</ul>
<hr><p>关注<strong>英语陪跑Go</strong>，备考不焦虑。</p>'''},

    # ── PET词汇速记 ─────────────────────────────────────────
    {'col': 'pet_word', 'title': 'PET必考词汇500：B1级别高频词分类精讲',
     'desc': 'PET词汇量要求约3500词，本文精选500个必考高频词，分类讲解记忆方法。',
     'content': '''<h2>PET必考词汇500：B1级别高频词分类精讲</h2>
<p>PET对应CEFR的B1级别，词汇量约3500词。考试中高频出现的词汇相对集中，掌握这些词可以事半功倍。</p>
<h2>一、社会与生活类</h2>
<ul>
<li><strong>advantage</strong> n. 优势 <em>The main advantage is the low cost.</em></li>
<li><strong>behaviour</strong> n. 行为 <em>Good behaviour is expected in school.</em></li>
<li><strong>community</strong> n. 社区 <em>She works for the local community.</em></li>
<li><strong>environment</strong> n. 环境 <em>We must protect the environment.</em></li>
<li><strong>generation</strong> n. 一代人 <em>The younger generation uses smartphones a lot.</em></li>
</ul>
<h2>二、情感与态度类</h2>
<ul>
<li><strong>anxious</strong> adj. 焦虑的 <em>She felt anxious before the exam.</em></li>
<li><strong>confident</strong> adj. 自信的 <em>He was confident about his answers.</em></li>
<li><strong>disappointed</strong> adj. 失望的 <em>I was disappointed with my results.</em></li>
<li><strong>enthusiastic</strong> adj. 热情的 <em>The students were enthusiastic about the project.</em></li>
<li><strong>frustrated</strong> adj. 沮丧的 <em>She got frustrated when she couldn't find the answer.</em></li>
</ul>
<h2>三、学习与工作类</h2>
<ul>
<li><strong>career</strong> n. 职业 <em>She wants a career in medicine.</em></li>
<li><strong>colleague</strong> n. 同事 <em>My colleagues are very helpful.</em></li>
<li><strong>deadline</strong> n. 截止日期 <em>We must meet the deadline.</em></li>
<li><strong>experience</strong> n. 经历/经验 <em>Work experience is very valuable.</em></li>
<li><strong>qualification</strong> n. 资格/证书 <em>PET is a useful qualification.</em></li>
</ul>
<h2>记忆技巧</h2>
<ol>
<li><strong>词根法：</strong>gen（产生）→ generation, generate, genetic</li>
<li><strong>搭配法：</strong>make an effort, take responsibility, have an advantage</li>
<li><strong>语境法：</strong>阅读真实英文材料，在句子中记词</li>
</ol>
<hr><p>关注<strong>英语陪跑Go</strong>，每天备考干货。</p>'''},

    {'col': 'pet_word', 'title': 'PET高频短语动词50个：用法+例句完整版',
     'desc': 'PET考试中短语动词频繁出现，本文整理50个必考短语动词，每个配例句。',
     'content': '''<h2>PET高频短语动词50个：用法+例句完整版</h2>
<p>短语动词（Phrasal Verbs）是英语中常见但令人头疼的结构。PET阅读和听力中经常出现，写作和口语中用好了能大大加分。</p>
<h2>重点短语动词（按字母排序）</h2>
<ul>
<li><strong>break down</strong> 停止运转；情绪崩溃<br><em>The car broke down on the motorway.</em></li>
<li><strong>bring up</strong> 抚养；提起（话题）<br><em>She was brought up by her grandparents.</em></li>
<li><strong>call off</strong> 取消<br><em>They called off the match because of rain.</em></li>
<li><strong>carry on</strong> 继续<br><em>Please carry on with your work.</em></li>
<li><strong>come across</strong> 偶然遇到；给人留下印象<br><em>I came across this book at a second-hand shop.</em></li>
<li><strong>cut down on</strong> 减少<br><em>You should cut down on sugar.</em></li>
<li><strong>deal with</strong> 处理；应对<br><em>How do you deal with stress?</em></li>
<li><strong>drop out</strong> 退出；辍学<br><em>He dropped out of university after one year.</em></li>
<li><strong>end up</strong> 最终成为/到达<br><em>We got lost and ended up in the wrong town.</em></li>
<li><strong>fall out with</strong> 与…闹翻<br><em>She fell out with her best friend over money.</em></li>
<li><strong>figure out</strong> 弄清楚；想明白<br><em>I can't figure out how to use this app.</em></li>
<li><strong>get along with</strong> 与…相处融洽<br><em>I get along well with my classmates.</em></li>
<li><strong>give up</strong> 放弃<br><em>Don't give up — keep trying!</em></li>
<li><strong>go ahead</strong> 开始；继续<br><em>"Can I use your phone?" "Go ahead."</em></li>
<li><strong>grow up</strong> 成长；长大<br><em>Where did you grow up?</em></li>
<li><strong>keep up with</strong> 跟上；保持同步<br><em>It's hard to keep up with all the new technology.</em></li>
<li><strong>look forward to</strong> 期待<br><em>I'm looking forward to the holidays.</em></li>
<li><strong>make up</strong> 和好；编造<br><em>They argued but made up the next day.</em></li>
<li><strong>put off</strong> 推迟<br><em>Don't put off what you can do today.</em></li>
<li><strong>run out of</strong> 用完<br><em>We've run out of milk.</em></li>
<li><strong>set up</strong> 建立；安排<br><em>She set up her own business at 25.</em></li>
<li><strong>show off</strong> 炫耀<br><em>He's always showing off his new car.</em></li>
<li><strong>take up</strong> 开始（兴趣/习惯）<br><em>She took up yoga last year.</em></li>
<li><strong>turn down</strong> 拒绝；调低（音量）<br><em>He turned down the job offer.</em></li>
<li><strong>work out</strong> 锻炼；弄清楚<br><em>I work out at the gym three times a week.</em></li>
</ul>
<hr><p>关注<strong>英语陪跑Go</strong>，每天进步一点点。</p>'''},

    {'col': 'pet_word', 'title': 'PET备考词汇记忆法：5种方法让单词不再忘',
     'desc': '死背单词效果差？本文分享5种科学的PET词汇记忆法，让你事半功倍。',
     'content': '''<h2>PET备考词汇记忆法：5种方法让单词不再忘</h2>
<p>PET备考中，词汇是基础。很多同学用传统死记硬背的方法，效率低、容易忘。本文分享5种更科学的方法。</p>
<h2>方法一：词根词缀法</h2>
<p>英语单词由词根+词缀构成，掌握常见词根能快速推测词义。</p>
<ul>
<li><strong>un-</strong>（否定）：unhappy, unfair, uncertain</li>
<li><strong>re-</strong>（再次）：return, review, rebuild</li>
<li><strong>-tion/-sion</strong>（名词后缀）：information, decision, pollution</li>
<li><strong>-ful</strong>（形容词）：helpful, careful, successful</li>
</ul>
<h2>方法二：语境记忆法</h2>
<p>看到一个新词，不要孤立地背它，而是在句子或段落中记忆。</p>
<blockquote>不好的方式：<em>frustrated = 沮丧的</em><br>
好的方式：<em>She felt frustrated when she couldn't understand the question. 当她听不懂问题时感到很沮丧。</em></blockquote>
<h2>方法三：词汇网络法</h2>
<p>以一个核心词为中心，建立词汇联系网：</p>
<ul>
<li>核心词：<strong>travel</strong></li>
<li>同义词：journey, trip, voyage</li>
<li>相关词：passport, luggage, destination, flight</li>
<li>搭配：travel by plane, go on a trip, pack your bags</li>
</ul>
<h2>方法四：间隔重复法</h2>
<p>利用遗忘曲线，在快要忘记时复习效果最好。推荐使用Anki等软件。</p>
<ul>
<li>新词：当天、第2天、第7天、第30天分别复习</li>
<li>每次复习不超过20个新词</li>
</ul>
<h2>方法五：主题分类法</h2>
<p>按主题整理词汇，复习时更有逻辑：</p>
<ul>
<li>🏠 家居：furniture, kitchen, bedroom, living room</li>
<li>🛒 购物：receipt, discount, refund, cashier</li>
<li>🏥 健康：appointment, prescription, symptom, recovery</li>
</ul>
<hr><p>关注<strong>英语陪跑Go</strong>，科学备考不焦虑。</p>'''},

    # ── PET写作指导 ─────────────────────────────────────────
    {'col': 'pet_write', 'title': 'PET写作Part 1邮件写作：模板+范文+高分词汇',
     'desc': 'PET写作Part 1要求写100字邮件。本文给出完整模板、评分标准和高分词汇。',
     'content': '''<h2>PET写作Part 1邮件写作：模板+范文+高分词汇</h2>
<p>PET Writing Part 1要求考生根据3个要点写一封约100字的邮件或笔记。满分为15分，评分维度包括任务完成度、语法、词汇和内容连贯性。</p>
<h2>黄金模板</h2>
<blockquote>
Dear [Name] / Dear Sir or Madam,<br><br>
[开头句：说明写信目的，1-2句]<br><br>
[主体：覆盖3个要点，每点2-3句]<br><br>
[结尾句：期待回复/表达感谢]<br><br>
Best wishes / Yours faithfully,<br>
[Your name]
</blockquote>
<h2>真题范文</h2>
<p><strong>题目：</strong>你想邀请英国朋友Sam参加你的生日聚会。写信给他：</p>
<ul><li>告知聚会时间地点</li><li>建议他穿什么</li><li>告诉他怎么到达</li></ul>
<blockquote>
Dear Sam,<br><br>
I'm having a birthday party on Saturday, 15th March at my house (12 Green Street). It starts at 6 p.m. and will finish around midnight.<br><br>
The theme is "1980s", so please wear colourful clothes — the more fun, the better! You can take the No. 3 bus from the city centre and get off at Green Street. It only takes about 15 minutes.<br><br>
I really hope you can come. Let me know as soon as possible!<br><br>
Best wishes,<br>
Li Ming
</blockquote>
<h2>高分词汇和句型</h2>
<ul>
<li>邀请：<em>I would like to invite you to… / You are welcome to join…</em></li>
<li>通知：<em>I am writing to inform you that… / I wanted to let you know…</em></li>
<li>请求：<em>Could you please… / Would it be possible to…</em></li>
<li>感谢：<em>Thank you for your help. / I really appreciate it.</em></li>
<li>期待：<em>I look forward to hearing from you. / I hope to see you soon.</em></li>
</ul>
<hr><p>关注<strong>英语陪跑Go</strong>，写作提分不难。</p>'''},

    {'col': 'pet_write', 'title': 'PET写作Part 2文章写作：记叙文和议论文各自怎么写',
     'desc': 'PET写作Part 2考记叙文或议论文，约100字。本文分开讲解两种文体的框架和技巧。',
     'content': '''<h2>PET写作Part 2文章写作：记叙文和议论文各自怎么写</h2>
<p>PET Writing Part 2要求考生写一篇约100字的短文，题材不固定，可以是故事（记叙文）或观点讨论（议论文）。</p>
<h2>记叙文框架</h2>
<p><strong>结构：</strong>背景 → 事件 → 结果/感受</p>
<p><strong>常用时态：</strong>过去简单时（did）、过去进行时（was doing）</p>
<blockquote>
<p><strong>题目：</strong>Write about a time when something unexpected happened to you.</p>
<p><strong>范文：</strong></p>
<p>Last summer, I was walking to school when I suddenly heard a strange noise coming from a bush. I stopped and looked carefully. To my surprise, I saw a tiny kitten stuck in the branches!</p>
<p>I carefully freed the kitten and took it home. My parents helped me find its owner. The experience taught me that small moments can make a big difference to someone's life.</p>
</blockquote>
<h2>议论文框架</h2>
<p><strong>结构：</strong>观点 → 理由1 → 理由2 → 总结</p>
<p><strong>常用连接词：</strong>firstly, secondly, however, in conclusion, on the other hand</p>
<blockquote>
<p><strong>题目：</strong>Should teenagers have part-time jobs?</p>
<p><strong>范文：</strong></p>
<p>I believe teenagers should have part-time jobs for several reasons. Firstly, working teaches young people the value of money and responsibility. Secondly, it provides useful work experience for their future careers.</p>
<p>However, studies must come first. A part-time job should not take up too much time. In conclusion, a balance between work and study is possible and beneficial.</p>
</blockquote>
<h2>通用技巧</h2>
<ul>
<li>第一段清楚点明主题</li>
<li>用连接词让文章更流畅</li>
<li>结尾句要有力，不要草草收尾</li>
<li>检查时态一致性</li>
</ul>
<hr><p>关注<strong>英语陪跑Go</strong>，写作得分轻松突破。</p>'''},

    {'col': 'pet_write', 'title': 'PET写作失分原因TOP5：这些错误你也在犯吗',
     'desc': '总结PET考生写作最常见的5类失分原因，附修改示范，对症下药提分更快。',
     'content': '''<h2>PET写作失分原因TOP5：这些错误你也在犯吗</h2>
<p>PET写作批改中，我们发现考生犯的错误惊人地相似。提前了解这些陷阱，备考时有意识地避开，可以显著提升得分。</p>
<h2>失分原因1：未覆盖所有要点</h2>
<p>Part 1有3个要点必须全覆盖，漏一个扣5分（任务完成度大项）。</p>
<p>❌ 错误：<em>写了2个要点，忽略了"如何到达"的信息。</em></p>
<p>✅ 解决：写完后对照题目，逐一检查每个要点是否在邮件中出现。</p>
<h2>失分原因2：时态混乱</h2>
<p>❌ 错误：<em>Yesterday I go to the park and see my friend.</em></p>
<p>✅ 修改：<em>Yesterday I went to the park and saw my friend.</em></p>
<p>规则：叙述过去的事用过去式，讲计划或请求用现在时/将来时。</p>
<h2>失分原因3：字数不足</h2>
<p>Part 1要求约100字，写60字会明显失分。字数不够时：</p>
<ul>
<li>为每个要点多加一个细节（why/how/when）</li>
<li>增加礼貌用语：<em>"I hope to hear from you soon."</em></li>
</ul>
<h2>失分原因4：重复词汇</h2>
<p>❌ 错误：<em>The party is good. The food is good. The people are good.</em></p>
<p>✅ 修改：<em>The party was wonderful. The food was delicious. Everyone was so friendly.</em></p>
<h2>失分原因5：缺少连接词</h2>
<p>句子之间没有过渡，文章读起来很突兀。</p>
<p>❌ 错误：<em>I like English. English is useful. I study every day.</em></p>
<p>✅ 修改：<em>I like English because it is very useful. That's why I study it every day.</em></p>
<hr><p>关注<strong>英语陪跑Go</strong>，写作不再失分。</p>'''},

    # ── PET阅读技巧 ─────────────────────────────────────────
    {'col': 'pet_read', 'title': 'PET阅读5个Part详解：每部分的做题顺序和策略',
     'desc': 'PET阅读共5部分，做题顺序影响得分。本文按部分讲解最优策略，附时间分配建议。',
     'content': '''<h2>PET阅读5个Part详解：每部分的做题顺序和策略</h2>
<p>PET Reading共5部分，35道题，建议总用时45分钟。合理分配时间、掌握每部分策略是高分的关键。</p>
<h2>Part 1 – 短文匹配（5题）</h2>
<p><strong>时间：</strong>5分钟 | <strong>难度：</strong>★★☆☆☆</p>
<p>读5个短文本（公告、短信、标识），每个文本有3个选项描述，选正确的。</p>
<p><strong>策略：</strong>先读选项，找关键词，再在文本中定位，注意否定和限制词。</p>
<h2>Part 2 – 信息配对（5题）</h2>
<p><strong>时间：</strong>8分钟 | <strong>难度：</strong>★★★☆☆</p>
<p>5人对应5段介绍，找出每人最适合的内容。</p>
<p><strong>策略：</strong>先读5人的需求（关键词），再对比5段描述，用排除法确定答案。</p>
<h2>Part 3 – 长文理解（5题）</h2>
<p><strong>时间：</strong>12分钟 | <strong>难度：</strong>★★★★☆</p>
<p>约450字的文章，5道四选一。</p>
<p><strong>策略：</strong>先读题目，带着问题读文章。答案通常按文章顺序出现。</p>
<h2>Part 4 – 词汇填空（5题）</h2>
<p><strong>时间：</strong>7分钟 | <strong>难度：</strong>★★★☆☆</p>
<p>短文中5处填空，每处4个词汇选项。</p>
<p><strong>策略：</strong>看词性（名词/动词/形容词），看搭配（固定搭配是关键）。</p>
<h2>Part 5 – 语法填空（5题）</h2>
<p><strong>时间：</strong>8分钟 | <strong>难度：</strong>★★★★☆</p>
<p>短文中5处填空，选一个最合适的语法词（介词、连词、冠词等）。</p>
<p><strong>策略：</strong>考察语法知识，注意句子结构和上下文逻辑。</p>
<h2>做题顺序建议</h2>
<ol>
<li>先做Part 1（最快，热身）</li>
<li>做Part 2（配对有规律，效率高）</li>
<li>做Part 4（词汇题，短文短）</li>
<li>做Part 3（长文，需要最多时间）</li>
<li>最后做Part 5（语法题，需要冷静思考）</li>
</ol>
<hr><p>关注<strong>英语陪跑Go</strong>，阅读高分不难。</p>'''},

    {'col': 'pet_read', 'title': 'PET阅读同义替换练习：100组常考词汇对照表',
     'desc': 'PET阅读答案几乎不会原文照搬，掌握同义替换是关键。本文整理100组高频同义表达。',
     'content': '''<h2>PET阅读同义替换练习：100组常考词汇对照表</h2>
<p>PET阅读最大的难点是"同义替换"——原文用A说，选项用B说，考查你是否理解意思相同。这个技能需要大量积累。</p>
<h2>动词类同义替换</h2>
<ul>
<li><em>purchase</em> = buy（购买）</li>
<li><em>obtain / acquire</em> = get（得到）</li>
<li><em>assist / support</em> = help（帮助）</li>
<li><em>construct / build</em> = make（建造）</li>
<li><em>demonstrate</em> = show（展示）</li>
<li><em>require / need</em> = want（需要）</li>
<li><em>refuse / decline</em> = say no（拒绝）</li>
<li><em>select / choose</em> = pick（选择）</li>
<li><em>repair / fix</em> = mend（修理）</li>
<li><em>commence / begin</em> = start（开始）</li>
</ul>
<h2>形容词类同义替换</h2>
<ul>
<li><em>enormous / huge</em> = very big（巨大的）</li>
<li><em>tiny / miniature</em> = very small（微小的）</li>
<li><em>exhausted / tired</em> = worn out（疲惫的）</li>
<li><em>delighted / pleased</em> = happy（高兴的）</li>
<li><em>furious / angry</em> = very mad（愤怒的）</li>
<li><em>brilliant / excellent</em> = very good（极好的）</li>
<li><em>dreadful / terrible</em> = very bad（糟糕的）</li>
<li><em>unusual / rare</em> = not common（不寻常的）</li>
</ul>
<h2>名词类同义替换</h2>
<ul>
<li><em>residence / dwelling</em> = home（住所）</li>
<li><em>employment / occupation</em> = job（工作）</li>
<li><em>journey / voyage</em> = trip（旅行）</li>
<li><em>method / approach</em> = way（方法）</li>
<li><em>aim / objective</em> = goal（目标）</li>
<li><em>concern / worry</em> = problem（担忧）</li>
</ul>
<h2>短语同义替换</h2>
<ul>
<li><em>at the moment</em> = currently, now（现在）</li>
<li><em>as a result</em> = therefore, so（因此）</li>
<li><em>in addition</em> = also, moreover（此外）</li>
<li><em>on the other hand</em> = however, but（另一方面）</li>
<li><em>at the end of the day</em> = ultimately（最终）</li>
</ul>
<h2>练习方法</h2>
<ol>
<li>做阅读题时，对照答案找出同义替换的词</li>
<li>建立自己的词汇替换本</li>
<li>每天练习5组同义词辨析</li>
</ol>
<hr><p>关注<strong>英语陪跑Go</strong>，阅读技能快速提升。</p>'''},

    # ── 每日英语 ─────────────────────────────────────────────
    {'col': 'daily', 'title': '每日英语 | 3月21日：春天来了，这些表达要会说',
     'desc': '今日主题：描述春天和季节变化的英文表达，含例句和练习题。',
     'content': '''<h2>今日主题：春天相关英语表达</h2>
<p>今天是3月21日，正式进入春天。用英语描述春天，你会几种说法？</p>
<h2>今日词组</h2>
<ul>
<li><strong>spring is in the air</strong> 春意盎然<br><em>Spring is in the air — flowers are blooming everywhere.</em></li>
<li><strong>blossom</strong> v./n. （花）开放；花<br><em>The cherry trees are in full blossom.</em></li>
<li><strong>mild weather</strong> 温和的天气<br><em>Spring brings mild weather after the cold winter.</em></li>
<li><strong>come alive</strong> 充满生机<br><em>The garden comes alive in spring.</em></li>
<li><strong>fresh start</strong> 全新开始<br><em>Spring always feels like a fresh start.</em></li>
</ul>
<h2>今日练习</h2>
<p>选出正确选项：</p>
<p>The flowers are starting to _______ after the long winter.<br>
A. blossom &nbsp; B. blossom &nbsp; C. blossoming &nbsp; D. blossomed</p>
<p><strong>答案：A（blossom，原形动词，句子时态是现在进行时：are starting to blossom）</strong></p>
<h2>今日造句挑战</h2>
<p>用"come alive"造一个关于春天的句子，写在评论区 💬</p>
<hr>
<p>📱 关注<strong>英语陪跑Go</strong>，每天一练，备考不焦虑。</p>'''},

    # ── 英语演讲 ──────────────────────────────────────────────
    {'col': 'speech', 'title': '英语演讲入门：5个让你不再发抖的实用技巧',
     'desc': '很多人一站上台英语就忘光。本文分享5个立竿见影的演讲技巧，帮你找到自信。',
     'content': '''<h2>英语演讲入门：5个让你不再发抖的实用技巧</h2>
<p>英语演讲对很多学生来说是"最恐怖的课堂任务"。但事实上，演讲技巧是可以学习和练习的，恐惧也会随着练习减少。</p>
<h2>技巧一：充分准备，不要背稿</h2>
<p>很多人试图把整篇演讲背下来，一卡壳就全乱了。更好的方法是：</p>
<ul>
<li>准备3-5个关键句子（开头、过渡、结尾）</li>
<li>用关键词制作提示卡，不用写完整句子</li>
<li>多次大声练习，而不是默读</li>
</ul>
<h2>技巧二：开头要有钩子</h2>
<p>前15秒决定听众是否会继续听。好的开头：</p>
<ul>
<li>提问：<em>"Have you ever wondered why...?"</em></li>
<li>惊人数据：<em>"Did you know that 90% of people...?"</em></li>
<li>小故事：<em>"Last year, something happened to me that changed my view..."</em></li>
</ul>
<h2>技巧三：慢说，停顿，呼吸</h2>
<p>紧张时人们会说话越来越快，听众跟不上。意识地放慢速度：</p>
<ul>
<li>每个要点之间停顿2-3秒</li>
<li>深呼吸可以降低心率，声音更稳定</li>
<li>停顿不是弱点，是给听众消化的时间</li>
</ul>
<h2>技巧四：用眼神交流</h2>
<p>不要一直看提示卡或天花板。尝试：</p>
<ul>
<li>在教室三个区域（左、中、右）轮流扫视</li>
<li>每个区域停留3-5秒</li>
<li>对某个点头的人多看一眼，能增强信心</li>
</ul>
<h2>技巧五：出错了怎么办</h2>
<p>每个演讲者都会出错，区别在于如何应对：</p>
<ul>
<li>忘词：<em>"Let me rephrase that..."</em> 然后换一种说法</li>
<li>说错了：<em>"Actually, what I meant to say is..."</em></li>
<li>最重要：微笑，继续，不要道歉</li>
</ul>
<hr><p>关注<strong>英语陪跑Go</strong>，英语口语和演讲能力同步提升。</p>'''},

    {'col': 'speech', 'title': '英语演讲模板：10个场景开场白一键套用',
     'desc': '不同场景的演讲需要不同的开场。本文给出10个常用场景的开场白模板，直接套用。',
     'content': '''<h2>英语演讲模板：10个场景开场白一键套用</h2>
<p>好的开场白是演讲成功的一半。根据不同场景选择合适的开场方式，能立刻抓住听众注意力。</p>
<h2>场景1：课堂汇报</h2>
<blockquote>Good morning/afternoon, everyone. Today, I'm going to talk about [topic]. I'll start by introducing the background, then explain the main points, and finally share my conclusion. Let's get started.</blockquote>
<h2>场景2：问题引入型</h2>
<blockquote>Let me start with a question: Have you ever [relevant question]? I'm sure many of you have. Today, I'd like to explore why this happens and what we can do about it.</blockquote>
<h2>场景3：数据引入型</h2>
<blockquote>According to a recent study, [surprising statistic]. This might surprise you, but it tells us something important about [topic]. Let me explain...</blockquote>
<h2>场景4：故事引入型</h2>
<blockquote>Let me tell you a short story. [One-sentence story]. This experience taught me [key message], which is exactly what I want to share with you today.</blockquote>
<h2>场景5：辩论赛</h2>
<blockquote>Good afternoon, judges, teachers and fellow students. I am [name], speaking for/against the motion that [topic]. My team firmly believes that... Here are our three main arguments.</blockquote>
<h2>结尾模板</h2>
<blockquote>
To sum up, I've talked about [point 1], [point 2] and [point 3]. The main takeaway is [key message]. I hope you found this interesting. Thank you for listening. I'm happy to take any questions.
</blockquote>
<hr><p>关注<strong>英语陪跑Go</strong>，英语演讲不再怵。</p>'''},
]


def main():
    conn = pymysql.connect(**DB)
    cur  = conn.cursor()
    print('连接成功，开始插入文章...\n')
    ok = 0
    for a in ARTICLES:
        cid = COL[a['col']]
        sql = ("INSERT INTO ep_news "
               "(title,content,description,class1,addtime,updatetime,lang,wap_ok,displaytype) "
               "VALUES (%s,%s,%s,%s,%s,%s,'cn',1,1)")
        try:
            cur.execute(sql, (a['title'], a['content'], a['desc'][:255],
                              cid, NOW, NOW))
            conn.commit()
            ok += 1
            print(f'  ✓ [{a["col"]}] {a["title"][:45]}')
        except Exception as e:
            print(f'  ✗ {a["title"][:40]} → {e}')
    conn.close()
    print(f'\n完成！成功插入 {ok}/{len(ARTICLES)} 篇文章')


if __name__ == '__main__':
    main()
