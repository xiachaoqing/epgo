#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成英语陪跑GO方向的Blogger文章（KET/PET/英语学习）
在本地运行，生成HTML文章文件到 /tmp/blogger-english/
"""
import os

OUTPUT_DIR = "/tmp/blogger-english"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ARTICLES = [
    # ── KET 备考 ──
    {
        "filename": "ket-reading-tips.html",
        "title": "KET阅读技巧：5个方法让你阅读分数提升20分",
        "labels": ["KET", "英语阅读", "剑桥英语", "备考技巧"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&q=80" alt="英语阅读备考" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>KET阅读部分（Reading）占总分的比重很大，很多同学在这里失分严重。本文总结了5个经过验证的阅读技巧，帮助你快速提升分数。</p>

<h2>一、先看题目再读文章</h2>
<figure><img src="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&q=80" alt="KET阅读策略" style="width:100%;border-radius:8px;"><figcaption>先看题目能帮你快速定位答案</figcaption></figure>
<p>很多同学习惯先通读全文，再去看题目。但KET考试时间有限，正确的做法是：</p>
<ol>
  <li>先快速浏览所有题目，了解考察点</li>
  <li>带着问题去读文章，快速定位关键信息</li>
  <li>找到答案后立即标记，不要反复阅读</li>
</ol>

<h2>二、识别关键词（Keywords）</h2>
<p>每道题都有关键词，比如人名、地名、时间、数字等。这些词在文章中通常原文出现或有同义替换。</p>
<p><strong>例题：</strong>When did Tom arrive at the airport?</p>
<p>关键词：Tom、arrive、airport → 在文章中找这几个词附近的内容即可。</p>

<h2>三、同义替换是陷阱也是关键</h2>
<p>KET阅读最常见的出题手法就是"同义替换"——题目用一个词，文章用另一个词表达同样的意思。</p>
<p>常见替换对：</p>
<ul>
  <li>big → large / huge</li>
  <li>happy → pleased / delighted</li>
  <li>buy → purchase</li>
  <li>start → begin / commence</li>
</ul>

<h2>四、不认识的单词先猜意思</h2>
<p>遇到生词不要慌，可以通过以下方法猜测意思：</p>
<ul>
  <li><strong>上下文推断</strong>：根据前后句子理解</li>
  <li><strong>词根词缀</strong>：un- 表示"不"，-tion 表示名词</li>
  <li><strong>跳过继续读</strong>：有时不影响答题</li>
</ul>

<h2>五、控制时间分配</h2>
<p>KET阅读部分建议时间分配：</p>
<ul>
  <li>Part 1（匹配题）：10分钟</li>
  <li>Part 2（填空）：8分钟</li>
  <li>Part 3（阅读理解）：12分钟</li>
  <li>检查时间：5分钟</li>
</ul>

<p>坚持练习，每天阅读一篇英文短文，30天内你的阅读速度和理解能力都会有明显提升。关注<strong>英语陪跑GO</strong>，每日推送备考资料！</p>
"""
    },
    {
        "filename": "ket-listening-guide.html",
        "title": "KET听力真题解析：这3种题型让你不再失分",
        "labels": ["KET", "英语听力", "剑桥英语", "真题解析"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80" alt="KET听力训练" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>KET听力（Listening）分为5个Part，每个Part难度和题型不同。很多同学反映听力"听懂了但做错了"，本文告诉你为什么，以及怎么解决。</p>

<h2>Part 1：图片选择题（5题）</h2>
<figure><img src="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&q=80" alt="听力图片题" style="width:100%;border-radius:8px;"><figcaption>图片选择题需要提前预判</figcaption></figure>
<p>这部分给你三张图，听录音选正确答案。</p>
<p><strong>关键技巧</strong>：播音前先看三张图的区别在哪里，预判考察点（颜色/数量/位置/时间）。录音会先用一个句子描述A或B（干扰项），再说出正确答案。</p>

<h2>Part 2：填写信息题（5题）</h2>
<p>听一段对话，填写表格或便条里的信息，通常考察数字、时间、地点、人名等。</p>
<p><strong>失分原因</strong>：拼写错误！"Tuesday"写成"Tuseday"直接失分。</p>
<p><strong>高频考点单词</strong>：Monday/Tuesday/Wednesday、January~December、数字1-1000。</p>

<h2>Part 3：对话选择题（5题）</h2>
<p>听较长对话，回答5道选择题。注意：答案不一定按顺序出现。</p>
<p><strong>技巧</strong>：听到第一个选项被提到时，别急着选，因为对话最终可能推翻它。要听完整段再做判断。</p>

<h2>每天练习方法</h2>
<ul>
  <li>用BBC Learning English：每集6分钟，适合KET水平</li>
  <li>做完真题后必须精听：每句话都要听懂</li>
  <li>跟读训练（Shadowing）：模仿语音语调，提升耳朵灵敏度</li>
</ul>

<p>想要更多KET备考资料，关注公众号<strong>英语陪跑GO</strong>，每天推送考点精讲！</p>
"""
    },
    {
        "filename": "ket-writing-email.html",
        "title": "KET写作邮件范文：5个万能模板（高分必备）",
        "labels": ["KET", "英语写作", "剑桥英语", "写作模板"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&q=80" alt="英语写作模板" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>KET写作Part 7是邮件/便条写作，要求写25个单词以上完成3个任务点。这部分是可以靠模板拿满分的！</p>

<h2>邮件基本结构</h2>
<pre style="background:#f5f5f5;padding:16px;border-radius:8px;overflow:auto;">
Hi [Name],

[Opening sentence - 开头句]
[Task 1 content]
[Task 2 content]
[Task 3 content]

[Closing]
[Your name]
</pre>

<h2>5个万能开头句</h2>
<figure><img src="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80" alt="写作开头句" style="width:100%;border-radius:8px;"><figcaption>好的开头句让写作更流畅</figcaption></figure>
<ul>
  <li>Thanks for your email. / Thank you for writing to me.</li>
  <li>I'm writing to tell you about...</li>
  <li>I'm so happy to hear from you!</li>
  <li>I hope you are doing well.</li>
  <li>I wanted to let you know that...</li>
</ul>

<h2>5个万能结尾句</h2>
<ul>
  <li>I hope to hear from you soon.</li>
  <li>Please write back when you can.</li>
  <li>Let me know what you think!</li>
  <li>Looking forward to seeing you.</li>
  <li>Best wishes, / See you soon,</li>
</ul>

<h2>3个任务点的处理方法</h2>
<p>KET邮件通常有3个任务，例如：</p>
<ul>
  <li>Say where you went（说去了哪里）</li>
  <li>Say what you did there（说做了什么）</li>
  <li>Invite your friend（邀请朋友）</li>
</ul>
<p>每个任务点至少写一句话，简洁完整即可，不要拐弯抹角。</p>

<h2>范文示例</h2>
<pre style="background:#f5f5f5;padding:16px;border-radius:8px;overflow:auto;">
Hi Tom,

I'm writing to tell you about my weekend trip. I went to
Shanghai with my family. We visited the Bund and ate
delicious food there! Would you like to come with us next
time? It would be great fun!

Best wishes,
Li Ming
</pre>
<p>字数：约60词，覆盖3个任务点，语言简单流畅，这就是满分邮件的标准。</p>
"""
    },
    {
        "filename": "pet-reading-long-text.html",
        "title": "PET阅读长文攻略：如何在限时内读懂复杂文章",
        "labels": ["PET", "英语阅读", "剑桥英语", "备考技巧"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80" alt="PET阅读备考" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>PET的阅读难度比KET高出一个档次，文章更长、词汇更难、逻辑更复杂。很多同学反映"时间不够用"，本文给出系统解决方案。</p>

<h2>PET阅读部分结构</h2>
<ul>
  <li><strong>Part 1</strong>：5段短文（告示/邮件），每段1题，选A/B/C</li>
  <li><strong>Part 2</strong>：5道配对题，把人和描述匹配</li>
  <li><strong>Part 3</strong>：长文章，5道选择题（A/B/C/D）</li>
  <li><strong>Part 4</strong>：文章+5题（正确/错误/文中未提及）</li>
  <li><strong>Part 5</strong>：填词（词汇选择），4选1，共6题</li>
</ul>

<h2>时间分配策略</h2>
<figure><img src="https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=800&q=80" alt="考试时间管理" style="width:100%;border-radius:8px;"><figcaption>合理的时间分配是PET高分关键</figcaption></figure>
<p>总时间45分钟，建议分配：</p>
<ul>
  <li>Part 1：8分钟</li>
  <li>Part 2：8分钟</li>
  <li>Part 3：10分钟</li>
  <li>Part 4：10分钟</li>
  <li>Part 5：5分钟</li>
  <li>检查：4分钟</li>
</ul>

<h2>长文阅读的"三遍法"</h2>
<ol>
  <li><strong>第一遍（1分钟）</strong>：快速扫读标题、首句、尾句，建立全文框架</li>
  <li><strong>第二遍（带题读）</strong>：针对每道题定位相关段落，精读关键句</li>
  <li><strong>第三遍（验证）</strong>：确认答案后检查是否有明显矛盾</li>
</ol>

<h2>Part 4 "未提及"的判断技巧</h2>
<p>这是PET最让人头疼的题型，区别：</p>
<ul>
  <li><strong>FALSE</strong>：文章明确说了相反的内容</li>
  <li><strong>NOT GIVEN</strong>：文章完全没提到这个信息</li>
</ul>
<p>判断技巧：如果你在文章中找不到任何相关词，选NOT GIVEN；如果找到了但意思相反，选FALSE。</p>
"""
    },
    {
        "filename": "english-grammar-tense.html",
        "title": "KET/PET必考语法：时态一网打尽（附练习题）",
        "labels": ["KET", "PET", "英语语法", "时态", "备考"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=800&q=80" alt="英语语法时态" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>时态是KET/PET语法题的核心考点，掌握以下6个时态，语法题得分率可以超过90%。</p>

<h2>1. 一般现在时（Simple Present）</h2>
<p><strong>用法</strong>：习惯、事实、规律</p>
<p>She <strong>studies</strong> English every day.<br>The sun <strong>rises</strong> in the east.</p>

<h2>2. 现在进行时（Present Continuous）</h2>
<p><strong>用法</strong>：正在发生的动作</p>
<p>He <strong>is playing</strong> football now.<br>They <strong>are having</strong> lunch at the moment.</p>

<h2>3. 一般过去时（Simple Past）</h2>
<figure><img src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80" alt="语法学习" style="width:100%;border-radius:8px;"><figcaption>时态是考试必考点</figcaption></figure>
<p><strong>用法</strong>：过去发生的事情（已结束）</p>
<p>I <strong>visited</strong> Beijing last year.<br>She <strong>didn't go</strong> to school yesterday.</p>

<h2>4. 现在完成时（Present Perfect）</h2>
<p><strong>用法</strong>：过去的动作对现在有影响</p>
<p>I <strong>have lived</strong> here for 5 years.<br>She <strong>has just finished</strong> her homework.</p>
<p>关键词：ever, never, already, just, yet, since, for</p>

<h2>5. 一般将来时（Simple Future）</h2>
<p><strong>用法</strong>：将要发生的事情</p>
<p>It <strong>will rain</strong> tomorrow.<br>I <strong>am going to</strong> study hard.</p>

<h2>6. 过去进行时（Past Continuous）</h2>
<p><strong>用法</strong>：过去某时刻正在进行的动作</p>
<p>When she called, I <strong>was sleeping</strong>.<br>They <strong>were watching</strong> TV at 8pm.</p>

<h2>练习题（答案在文末）</h2>
<ol>
  <li>She ______ (study) English when I called her.</li>
  <li>I ______ (never/visit) Paris before.</li>
  <li>The train ______ (leave) at 9am tomorrow.</li>
  <li>We ______ (play) football every Saturday.</li>
</ol>
<p><strong>答案</strong>：1. was studying  2. have never visited  3. will leave / leaves  4. play</p>
"""
    },
    {
        "filename": "ket-vocabulary-daily-life.html",
        "title": "KET高频词汇：日常生活主题100词（分类记忆）",
        "labels": ["KET", "词汇", "英语学习", "日常用语"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=800&q=80" alt="英语词汇记忆" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>KET词汇考察日常生活场景，本文按主题分类整理100个高频词，配上例句，帮你高效记忆。</p>

<h2>🏠 家庭与住所（20词）</h2>
<figure><img src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80" alt="家庭词汇" style="width:100%;border-radius:8px;"><figcaption>家庭场景是KET常考主题</figcaption></figure>
<ul>
  <li>bedroom 卧室 / living room 客厅 / bathroom 浴室</li>
  <li>kitchen 厨房 / garden 花园 / garage 车库</li>
  <li>furniture 家具 / sofa 沙发 / curtain 窗帘</li>
  <li>neighbour 邻居 / landlord 房东 / rent 租金</li>
  <li>move (house) 搬家 / share 合住 / tidy 整洁的</li>
</ul>

<h2>🍽️ 食物与餐饮（20词）</h2>
<ul>
  <li>breakfast/lunch/dinner 早/午/晚餐</li>
  <li>menu 菜单 / order 点餐 / waiter 服务员</li>
  <li>vegetarian 素食的 / delicious 美味的</li>
  <li>recipe 食谱 / ingredient 食材 / cook 烹饪</li>
  <li>takeaway 外卖 / café 咖啡馆 / bill 账单</li>
</ul>

<h2>🚌 交通出行（20词）</h2>
<ul>
  <li>bus stop 公交站 / train station 火车站</li>
  <li>platform 站台 / departure 出发 / arrival 到达</li>
  <li>delay 延误 / cancel 取消 / ticket 票</li>
  <li>journey 旅途 / passenger 乘客 / driver 司机</li>
  <li>traffic jam 堵车 / crossroads 十字路口</li>
</ul>

<h2>🛍️ 购物（20词）</h2>
<ul>
  <li>shop / store 商店 / supermarket 超市</li>
  <li>price 价格 / discount 折扣 / sale 打折</li>
  <li>receipt 收据 / refund 退款 / exchange 换货</li>
  <li>fitting room 试衣间 / size 尺码 / cash 现金</li>
  <li>credit card 信用卡 / queue 排队 / busy 繁忙的</li>
</ul>

<h2>💼 工作与学习（20词）</h2>
<ul>
  <li>job / work 工作 / office 办公室 / colleague 同事</li>
  <li>boss / manager 老板/经理 / salary 薪水</li>
  <li>homework 作业 / exam 考试 / grade 成绩</li>
  <li>university 大学 / subject 科目 / library 图书馆</li>
  <li>graduate 毕业 / study 学习 / practice 练习</li>
</ul>

<p>建议每天记一个主题（20词），5天内掌握全部100词。结合例句和场景记忆，效果远好于死记硬背！</p>
"""
    },
    {
        "filename": "pet-speaking-tips.html",
        "title": "PET口语考试攻略：考官最想听到的表达方式",
        "labels": ["PET", "英语口语", "剑桥英语", "口语技巧"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1543269664-56d93c1b41a6?w=800&q=80" alt="PET口语考试" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>PET口语（Speaking）分为4个Part，两人一组考试，持续约12-17分钟。很多同学因为紧张或不知道说什么而失分，本文给你最实用的应对策略。</p>

<h2>Part 1：回答考官问题（2-3分钟）</h2>
<p>考官会问你个人信息类问题，如家乡、爱好、学习等。</p>
<p><strong>答题模板：</strong></p>
<ul>
  <li>简短直接回答问题</li>
  <li>加一个理由或细节</li>
  <li>不要用一个词结束</li>
</ul>
<p>例：Q: Do you prefer reading books or watching films?<br>
A: I prefer <em>reading books</em> because I can use my imagination to picture the story. Also, I can read at my own speed.</p>

<h2>Part 2：描述图片（2-3分钟）</h2>
<figure><img src="https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?w=800&q=80" alt="口语描述图片" style="width:100%;border-radius:8px;"><figcaption>图片描述要有条理</figcaption></figure>
<p>给你一张图片，描述你看到的内容。</p>
<p><strong>万能开头：</strong>"This picture shows... / In this photo, I can see..."</p>
<p><strong>描述结构：</strong></p>
<ol>
  <li>总体描述（who/where）</li>
  <li>细节描述（what are they doing）</li>
  <li>推测或感受（I think... / It looks like...）</li>
</ol>

<h2>Part 3：与搭档讨论任务（2-3分钟）</h2>
<p>两人合作完成一个任务，如讨论朋友生日送什么礼物。</p>
<p><strong>有用的讨论用语：</strong></p>
<ul>
  <li>What do you think about...?</li>
  <li>I agree with you because...</li>
  <li>That's a good idea, but...</li>
  <li>How about we...? / Why don't we...?</li>
  <li>I'm not sure about that...</li>
</ul>

<h2>Part 4：讨论（2-3分钟）</h2>
<p>针对Part 3的话题，考官提问，两人讨论。这部分考察表达观点的能力。</p>
<p><strong>表达观点的句型：</strong></p>
<ul>
  <li>In my opinion, ... / I think that ...</li>
  <li>Personally, I believe ...</li>
  <li>The most important thing is ...</li>
  <li>On the other hand, ...</li>
</ul>

<h2>高分秘诀</h2>
<p>✅ 说错了不要停下来纠正，继续说<br>
✅ 不知道词汇时用简单词替代<br>
✅ 保持眼神交流，展示自信<br>
✅ 语速适中，不要太快也不要太慢</p>
"""
    },
    {
        "filename": "cambridge-english-levels.html",
        "title": "剑桥英语级别对照：KET/PET/FCE/CAE你在哪一级？",
        "labels": ["剑桥英语", "KET", "PET", "FCE", "英语水平"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=800&q=80" alt="剑桥英语级别" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>剑桥英语考试是全球认可度最高的英语资格认证之一，了解各级别的差异，可以帮你选择最适合自己的目标。</p>

<h2>剑桥英语主要级别</h2>
<figure><img src="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&q=80" alt="英语级别对照" style="width:100%;border-radius:8px;"><figcaption>从A2到C2，对应欧洲语言参考框架</figcaption></figure>

<table style="width:100%;border-collapse:collapse;margin:16px 0;">
<thead>
<tr style="background:#1565C0;color:white;">
  <th style="padding:10px;text-align:left;">考试名称</th>
  <th style="padding:10px;text-align:left;">CEFR级别</th>
  <th style="padding:10px;text-align:left;">适合人群</th>
  <th style="padding:10px;text-align:left;">用途</th>
</tr>
</thead>
<tbody>
<tr style="background:#f5f5f5;"><td style="padding:10px;">Pre-A1 Starters</td><td style="padding:10px;">Pre-A1</td><td style="padding:10px;">6-12岁儿童</td><td style="padding:10px;">英语启蒙</td></tr>
<tr><td style="padding:10px;">A1 Movers</td><td style="padding:10px;">A1</td><td style="padding:10px;">7-12岁</td><td style="padding:10px;">基础入门</td></tr>
<tr style="background:#f5f5f5;"><td style="padding:10px;">A2 Flyers</td><td style="padding:10px;">A2</td><td style="padding:10px;">8-12岁</td><td style="padding:10px;">初级认证</td></tr>
<tr><td style="padding:10px;"><strong>KET (A2 Key)</strong></td><td style="padding:10px;"><strong>A2</strong></td><td style="padding:10px;"><strong>初中生</strong></td><td style="padding:10px;"><strong>升学加分</strong></td></tr>
<tr style="background:#f5f5f5;"><td style="padding:10px;"><strong>PET (B1 Preliminary)</strong></td><td style="padding:10px;"><strong>B1</strong></td><td style="padding:10px;"><strong>高中生</strong></td><td style="padding:10px;"><strong>升学/出国</strong></td></tr>
<tr><td style="padding:10px;">FCE (B2 First)</td><td style="padding:10px;">B2</td><td style="padding:10px;">大学生</td><td style="padding:10px;">留学申请</td></tr>
<tr style="background:#f5f5f5;"><td style="padding:10px;">CAE (C1 Advanced)</td><td style="padding:10px;">C1</td><td style="padding:10px;">高级学习者</td><td style="padding:10px;">名校申请</td></tr>
<tr><td style="padding:10px;">CPE (C2 Proficiency)</td><td style="padding:10px;">C2</td><td style="padding:10px;">母语水平</td><td style="padding:10px;">顶级证书</td></tr>
</tbody>
</table>

<h2>KET (A2 Key) 适合谁？</h2>
<p>KET是初级认证，相当于初中英语水平。如果你能：</p>
<ul>
  <li>理解简单的日常英语</li>
  <li>写一封短邮件或便条</li>
  <li>用英语做简单的自我介绍</li>
</ul>
<p>那KET就是你的起点！</p>

<h2>PET (B1 Preliminary) 适合谁？</h2>
<p>PET是中级认证，相当于高中英语水平。如果你想出国留学、在国际化公司工作，PET是很好的敲门砖。</p>

<h2>该选KET还是PET？</h2>
<p>建议做一套KET真题：</p>
<ul>
  <li>阅读/听力得分≥70%：可以直接冲PET</li>
  <li>阅读/听力得分50-70%：先备考KET，通过后升级PET</li>
  <li>得分&lt;50%：从KET基础开始扎实学习</li>
</ul>
"""
    },
    {
        "filename": "english-study-plan-30days.html",
        "title": "30天KET备考计划（详细版）：每天只需1小时",
        "labels": ["KET", "学习计划", "英语备考", "30天"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800&q=80" alt="30天学习计划" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>很多同学问：如何在30天内系统备考KET？本文给出详细的每日计划，每天只需投入1小时，30天后你将对考试胸有成竹。</p>

<h2>备考前的准备</h2>
<ul>
  <li>下载官方真题（Cambridge A2 Key Official Practice Tests）</li>
  <li>关注公众号"英语陪跑GO"获取每日推送资料</li>
  <li>准备一本词汇本，随时记录生词</li>
</ul>

<h2>第1-10天：基础词汇 + 语法</h2>
<figure><img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&q=80" alt="英语学习小组" style="width:100%;border-radius:8px;"><figcaption>制定计划，坚持执行</figcaption></figure>
<table style="width:100%;border-collapse:collapse;">
<tr style="background:#EFF6FF;"><th style="padding:8px;text-align:left;">时间</th><th style="padding:8px;text-align:left;">任务</th></tr>
<tr><td style="padding:8px;">前20分钟</td><td style="padding:8px;">背20个KET高频词汇（用Anki或词汇本）</td></tr>
<tr style="background:#f9f9f9;"><td style="padding:8px;">中20分钟</td><td style="padding:8px;">学一个语法点（时态/介词/形容词比较级）</td></tr>
<tr><td style="padding:8px;">后20分钟</td><td style="padding:8px;">做10道语法练习题，检验学习效果</td></tr>
</table>

<h2>第11-20天：听力 + 阅读专项</h2>
<table style="width:100%;border-collapse:collapse;">
<tr style="background:#EFF6FF;"><th style="padding:8px;text-align:left;">时间</th><th style="padding:8px;text-align:left;">任务</th></tr>
<tr><td style="padding:8px;">前20分钟</td><td style="padding:8px;">听1段BBC Learning English（6分钟）并做笔记</td></tr>
<tr style="background:#f9f9f9;"><td style="padding:8px;">中20分钟</td><td style="padding:8px;">做1套KET阅读Part（真题）</td></tr>
<tr><td style="padding:8px;">后20分钟</td><td style="padding:8px;">精读错题，查生词，总结规律</td></tr>
</table>

<h2>第21-30天：模拟考试 + 查漏补缺</h2>
<table style="width:100%;border-collapse:collapse;">
<tr style="background:#EFF6FF;"><th style="padding:8px;text-align:left;">时间</th><th style="padding:8px;text-align:left;">任务</th></tr>
<tr><td style="padding:8px;">第21-25天</td><td style="padding:8px;">每天完成1套完整KET模拟题（限时）</td></tr>
<tr style="background:#f9f9f9;"><td style="padding:8px;">第26-28天</td><td style="padding:8px;">针对薄弱项（听/读/写）专项训练</td></tr>
<tr><td style="padding:8px;">第29-30天</td><td style="padding:8px;">轻度复习，保持状态，调整心态</td></tr>
</table>

<h2>每天必做的3件事</h2>
<ol>
  <li>背10个单词（用例句，不要只背中文）</li>
  <li>读一篇英文短文（100-200词）</li>
  <li>写5句英文日记（练习写作）</li>
</ol>

<p>坚持30天，你会发现英语能力有质的飞跃。欢迎关注<strong>英语陪跑GO</strong>，我们一起打卡备考！</p>
"""
    },
    {
        "filename": "pet-writing-article.html",
        "title": "PET写作文章题（Article）：考官评分标准+范文解析",
        "labels": ["PET", "英语写作", "剑桥英语", "写作范文"],
        "content": """
<figure><img src="https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800&q=80" alt="PET写作备考" style="width:100%;border-radius:8px;margin-bottom:16px;"><figcaption>Photo by Unsplash</figcaption></figure>

<p>PET写作Part 2要求写一篇100词左右的文章（Article）或故事（Story），是很多同学的失分点。本文解析评分标准并给出范文。</p>

<h2>评分标准（满分5分）</h2>
<ul>
  <li><strong>5分</strong>：内容完整，语言自然流畅，几乎无错误</li>
  <li><strong>4分</strong>：内容覆盖全面，语言基本准确，有少量错误</li>
  <li><strong>3分</strong>：内容基本完整，错误不影响理解</li>
  <li><strong>2分</strong>：部分内容缺失，有较多语言错误</li>
  <li><strong>1分</strong>：内容大量缺失，难以理解</li>
</ul>

<h2>Article（文章）的写作结构</h2>
<figure><img src="https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=800&q=80" alt="文章写作结构" style="width:100%;border-radius:8px;"><figcaption>清晰的结构是高分关键</figcaption></figure>
<ol>
  <li><strong>开头</strong>（2-3句）：引出话题，吸引读者</li>
  <li><strong>主体</strong>（4-6句）：2-3个论点或细节</li>
  <li><strong>结尾</strong>（1-2句）：总结或提出问题</li>
</ol>

<h2>真题范文解析</h2>
<p><strong>题目</strong>：Write an article for your school magazine about your favourite sport. You should:</p>
<ul>
  <li>describe the sport</li>
  <li>explain why you like it</li>
  <li>say how often you do it</li>
</ul>

<p><strong>范文（满分示例）：</strong></p>
<div style="background:#f5f5f5;padding:16px;border-radius:8px;border-left:4px solid #1565C0;">
<p><strong>My Favourite Sport: Swimming</strong></p>
<p>Have you ever tried swimming? It's one of the best sports you can do! Swimming is a great exercise that uses every muscle in your body.</p>
<p>I love swimming because it makes me feel relaxed and energetic at the same time. After a stressful week at school, jumping into the pool is the best feeling in the world. It's also good for your health — swimming regularly can improve your fitness and help you sleep better.</p>
<p>I go swimming at least twice a week, usually on Wednesdays and Saturdays. Why don't you give it a try?</p>
</div>

<h2>范文分析</h2>
<ul>
  <li>字数：约100词 ✓</li>
  <li>覆盖全部3个任务点 ✓</li>
  <li>有吸引人的开头问句 ✓</li>
  <li>语言自然，词汇丰富 ✓</li>
  <li>有结尾呼吁句 ✓</li>
</ul>

<h2>高频作文话题</h2>
<p>PET写作常见话题：最喜欢的运动/电影/食物/节日/旅游地点。建议每种话题准备一篇练习文，考试时灵活调用。</p>
"""
    },
]

for article in ARTICLES:
    filepath = os.path.join(OUTPUT_DIR, article["filename"])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article["content"].strip())
    print(f"已生成: {article['filename']}")

print(f"\n共生成 {len(ARTICLES)} 篇文章到 {OUTPUT_DIR}")

# 同时输出发布命令
print("\n发布命令（在本地运行）：")
print("cd ~/blogger-publisher")
for a in ARTICLES:
    labels = ",".join(a["labels"])
    print(f'python3 -c "')
