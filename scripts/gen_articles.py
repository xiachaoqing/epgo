#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语陪跑GO - 内容生成器
生成高质量的英语学习文章，用于演示和初始化内容

用法：
  python3 gen_articles.py              # 生成所有文章
  python3 gen_articles.py --ket        # 仅生成KET相关
  python3 gen_articles.py --pet        # 仅生成PET相关
  python3 gen_articles.py --dry        # 只预览不入库
"""

from __future__ import print_function
import sys
import time
from datetime import datetime, timedelta
import random
import pymysql

# 数据库配置
DB = dict(
    host='localhost',
    user='xiachaoqing',
    password='***REMOVED***',
    db='epgo_db',
    charset='utf8mb4',
    port=3306
)

# 栏目ID
COLUMNS = {
    'reading': 103,
    'ket': 128,
    'ket_exam': 111,
    'ket_word': 112,
    'ket_write': 113,
    'ket_listen': 114,
    'pet': 115,
    'pet_exam': 116,
}

DRY_RUN = '--dry' in sys.argv
FILTER = None
if '--ket' in sys.argv:
    FILTER = 'ket'
elif '--pet' in sys.argv:
    FILTER = 'pet'

# 高质量文章数据
ARTICLES = [
    # ============ KET真题解析 ============
    {
        'col': 'ket_exam',
        'title': 'KET 2024年真题解析：Reading Part 1完全攻略',
        'content': '''
        <h2>KET 2024年真题解析：Reading Part 1完全攻略</h2>
        <p>Cambridge English: Key（KET）是剑桥英语认证中的初级水平考试。Reading and Writing部分占总分的50%，而Reading Part 1作为阅读部分的开篇，难度不高但容易出错。</p>

        <h3>Part 1 题型介绍</h3>
        <p>Reading Part 1包含5道题目，每题呈现一个短文本（如邮件、短信、启事等）和5个选项。你需要从5个选项中选择最适当的句子来回答问题。</p>
        <ul>
            <li><strong>题量：</strong>5道题</li>
            <li><strong>时间分配：</strong>8-10分钟</li>
            <li><strong>难度：</strong>初级</li>
            <li><strong>题型：</strong>理解单一短文，选择正确答案</li>
        </ul>

        <h3>真题解析示例</h3>
        <p><strong>题目：</strong></p>
        <pre>
Text: "Meet me at the café near the station. I'll be there at 3 p.m. on Friday."
Question: When does the writer want to meet?
A) At the station
B) At 2 p.m.
C) At 3 p.m.
D) On Saturday
E) Near the station
        </pre>

        <p><strong>答案解析：</strong>正确答案是 C) At 3 p.m.</p>
        <p>虽然文本中提到了"café near the station"和"Friday"，但问题问的是"when"（什么时候），因此关键信息是"3 p.m. on Friday"。答案C最直接地回答了这个问题。</p>

        <h3>备考建议</h3>
        <ol>
            <li><strong>快速扫描：</strong>快速读完短文，理解大意</li>
            <li><strong>找关键词：</strong>根据问题找出短文中的关键词</li>
            <li><strong>排除法：</strong>先排除明显错误的选项</li>
            <li><strong>逻辑检查：</strong>选出答案后再读一遍确保语句通顺</li>
        </ol>

        <p>通过大量练习真题，你会发现Part 1虽然看似简单，但关键是要培养快速定位信息和理解句意的能力。</p>
        ''',
        'desc': 'KET Reading Part 1是考试的入门部分，考察基本的文本理解能力。本文详解真题结构、解题思路和备考建议。',
    },

    {
        'col': 'ket_exam',
        'title': 'KET 2024年写作真题详解：Part 2邮件写作',
        'content': '''
        <h2>KET 2024年写作真题详解：Part 2邮件写作</h2>
        <p>KET的Writing Part 2要求考生写一封约100字的邮件或笔记。这部分考察的是实际英语交流能力和基本的商务写作技能。</p>

        <h3>题型分析</h3>
        <p><strong>题目形式：</strong>通常给出3个要点，要求你围绕这些要点写一封邮件。</p>
        <p><strong>字数要求：</strong>约100字（±10%）</p>
        <p><strong>时间分配：</strong>15-20分钟</p>

        <h3>真题示例</h3>
        <pre>
You want to book a room at a hotel. Write an email to the hotel owner.
Include:
1. When you want to stay
2. What type of room you need
3. The number of people
        </pre>

        <h3>范文示例</h3>
        <pre>
Dear Sir/Madam,

I would like to book a room at your hotel from 20th to 25th June.
We need a double room with a bathroom. There are three people in
our group. Could you tell me the price for this room and the
available dates?

Thank you for your help. I look forward to hearing from you.

Yours faithfully,
John Smith
        </pre>

        <h3>写作要点</h3>
        <ul>
            <li><strong>结构清晰：</strong>包含greeting、body和closing</li>
            <li><strong>涵盖所有要点：</strong>不能遗漏题目给出的任何要点</li>
            <li><strong>语言简洁：</strong>使用简单但准确的句型</li>
            <li><strong>拼写正确：</strong>检查动词时态和基本拼写</li>
            <li><strong>礼貌用语：</strong>使用"Please"、"Thank you"等客套语</li>
        </ul>

        <h3>常见错误</h3>
        <ol>
            <li>字数过少或过多（超过110字）</li>
            <li>遗漏题目中的关键信息</li>
            <li>使用过于复杂的句式</li>
            <li>忘记使用正式的邮件格式</li>
            <li>时态混乱（如混用过去式和现在式）</li>
        </ol>
        ''',
        'desc': '邮件写作是KET写作的主要形式。本文通过真题示例和范文讲解，帮助考生掌握邮件结构和表达技巧。',
    },

    # ============ KET词汇速记 ============
    {
        'col': 'ket_word',
        'title': 'KET考试高频词汇大全：A-L部分',
        'content': '''
        <h2>KET考试高频词汇大全：A-L部分</h2>
        <p>KET考试要求掌握约1500个单词和短语。其中有一些高频词汇会反复出现在不同题型中。掌握这些词汇是通过考试的基础。</p>

        <h3>高频词汇分类</h3>

        <h4>日常交际（Communication）</h4>
        <table border="1" cellpadding="5">
            <tr>
                <td><strong>词汇</strong></td>
                <td><strong>中文</strong></td>
                <td><strong>例句</strong></td>
            </tr>
            <tr>
                <td>appointment</td>
                <td>约会，预约</td>
                <td>I have an appointment at the dentist.</td>
            </tr>
            <tr>
                <td>conversation</td>
                <td>对话，交谈</td>
                <td>We had a long conversation about the weather.</td>
            </tr>
            <tr>
                <td>explain</td>
                <td>解释</td>
                <td>Can you explain the meaning of this word?</td>
            </tr>
            <tr>
                <td>introduce</td>
                <td>介绍</td>
                <td>Let me introduce my friend, Tom.</td>
            </tr>
            <tr>
                <td>language</td>
                <td>语言</td>
                <td>English is my second language.</td>
            </tr>
        </table>

        <h4>食物和饮料（Food &amp; Drink）</h4>
        <table border="1" cellpadding="5">
            <tr>
                <td><strong>词汇</strong></td>
                <td><strong>中文</strong></td>
                <td><strong>例句</strong></td>
            </tr>
            <tr>
                <td>apple</td>
                <td>苹果</td>
                <td>An apple a day keeps the doctor away.</td>
            </tr>
            <tr>
                <td>bread</td>
                <td>面包</td>
                <td>I eat bread for breakfast.</td>
            </tr>
            <tr>
                <td>cheese</td>
                <td>奶酪</td>
                <td>Would you like some cheese on your pizza?</td>
            </tr>
            <tr>
                <td>drink</td>
                <td>饮料</td>
                <td>What would you like to drink?</td>
            </tr>
            <tr>
                <td>juice</td>
                <td>果汁</td>
                <td>Would you like orange juice or apple juice?</td>
            </tr>
        </table>

        <h3>记忆技巧</h3>
        <ul>
            <li><strong>词根词缀法：</strong>如 un-（否定）+ happy = unhappy</li>
            <li><strong>联想记忆：</strong>将相关词汇组合起来记忆，如餐厅相关：menu, dish, waiter</li>
            <li><strong>造句练习：</strong>用新单词造句，加深印象</li>
            <li><strong>重复复习：</strong>每天复习5-10个新单词，定期回顾</li>
        </ul>
        ''',
        'desc': 'KET词汇虽然数量多，但掌握高频词和常用搭配是重点。本文整理了分类词汇和记忆技巧。',
    },

    {
        'col': 'ket_word',
        'title': '如何快速背诵KET核心短语：短语搭配大全',
        'content': '''
        <h2>如何快速背诵KET核心短语：短语搭配大全</h2>
        <p>很多考生背单词时忽视了短语（phrasal verbs）和短语搭配（collocations），但这在阅读理解中经常出现。掌握常用短语能大大提升答题速度。</p>

        <h3>常用动词短语</h3>
        <ul>
            <li><strong>bring</strong>: bring back（归还），bring forward（提前）</li>
            <li><strong>carry</strong>: carry on（继续），carry out（实施）</li>
            <li><strong>come</strong>: come across（碰到），come back（回来），come on（加油）</li>
            <li><strong>cut</strong>: cut down（减少），cut off（中断）</li>
            <li><strong>get</strong>: get along（相处），get back（回来），get up（起床）</li>
            <li><strong>give</strong>: give up（放弃），give back（归还）</li>
            <li><strong>go</strong>: go on（继续），go back（回去），go for（选择）</li>
            <li><strong>look</strong>: look after（照顾），look for（寻找），look forward（期待）</li>
            <li><strong>put</strong>: put on（穿上），put up（搭建），put off（推迟）</li>
            <li><strong>take</strong>: take off（起飞），take care（照顾），take part（参加）</li>
        </ul>

        <h3>名词搭配</h3>
        <table border="1" cellpadding="5">
            <tr>
                <td><strong>表达</strong></td>
                <td><strong>含义</strong></td>
            </tr>
            <tr>
                <td>make a decision</td>
                <td>做出决定</td>
            </tr>
            <tr>
                <td>make progress</td>
                <td>取得进步</td>
            </tr>
            <tr>
                <td>take advice</td>
                <td>接受建议</td>
            </tr>
            <tr>
                <td>take a break</td>
                <td>休息</td>
            </tr>
            <tr>
                <td>have a look</td>
                <td>看一看</td>
            </tr>
            <tr>
                <td>have a try</td>
                <td>试一试</td>
            </tr>
        </table>

        <h3>背诵建议</h3>
        <ol>
            <li>不要孤立地背短语，要在句子中理解</li>
            <li>多做填空题，在实际应用中学习</li>
            <li>制作短语卡片，分类复习</li>
            <li>听力学习：通过英文歌曲或新闻积累短语</li>
        </ol>
        ''',
        'desc': '短语搭配是英语学习的重点难点。本文归纳了KET常考短语，并提供实用背诵方法。',
    },

    # ============ KET写作指导 ============
    {
        'col': 'ket_write',
        'title': 'KET写作从0到120分：5个必练题型',
        'content': '''
        <h2>KET写作从0到120分：5个必练题型</h2>
        <p>KET的Writing部分共120分钟，包含5个不同的写作任务。每个任务有不同的要求和评分标准。掌握每个题型的套路是得分的关键。</p>

        <h3>Part 1 - 补全对话</h3>
        <p><strong>题型：</strong>给出开头，完成一段6个句子的对话。</p>
        <p><strong>字数：</strong>通常6-8字/句</p>
        <p><strong>难度：</strong>最简单</p>
        <p><strong>技巧：</strong>
        <ul>
            <li>注意上下文逻辑</li>
            <li>回应对方问题，不能答非所问</li>
            <li>保持对话自然感</li>
        </ul>
        </p>

        <h3>Part 2 - 邮件/笔记写作</h3>
        <p><strong>题型：</strong>根据3个要点写邮件或笔记，约100字</p>
        <p><strong>难度：</strong>简单-中等</p>
        <p><strong>技巧：</strong>
        <ul>
            <li>必须涵盖全部3个要点</li>
            <li>使用正式的邮件格式</li>
            <li>简洁明了，避免啰嗦</li>
        </ul>
        </p>

        <h3>Part 3 - 短文描述</h3>
        <p><strong>题型：</strong>根据图片或提示写150-180字的短文</p>
        <p><strong>难度：</strong>中等</p>
        <p><strong>技巧：</strong>
        <ul>
            <li>详细描述图片细节</li>
            <li>组织好段落结构</li>
            <li>使用丰富的形容词和动词</li>
        </ul>
        </p>

        <h3>Part 4 - 故事写作</h3>
        <p><strong>题型：</strong>根据开头和3个关键词续写故事，200-250字</p>
        <p><strong>难度：</strong>较难</p>
        <p><strong>技巧：</strong>
        <ul>
            <li>故事要有逻辑，事件发展自然</li>
            <li>必须涵盖所有关键词</li>
            <li>用不同时态讲述过去事件</li>
        </ul>
        </p>

        <h3>评分标准</h3>
        <table border="1" cellpadding="5">
            <tr>
                <td><strong>维度</strong></td>
                <td><strong>权重</strong></td>
                <td><strong>要求</strong></td>
            </tr>
            <tr>
                <td>任务完成度</td>
                <td>40%</td>
                <td>是否回答了题目要求的所有内容</td>
            </tr>
            <tr>
                <td>语言使用</td>
                <td>30%</td>
                <td>语法、词汇、拼写的准确性</td>
            </tr>
            <tr>
                <td>段落组织</td>
                <td>20%</td>
                <td>段落间的逻辑连接和清晰度</td>
            </tr>
            <tr>
                <td>格式</td>
                <td>10%</td>
                <td>是否符合题目格式要求（如邮件格式）</td>
            </tr>
        </table>
        ''',
        'desc': 'KET写作包含5个不同题型，每个都有特定技巧。本文逐一分析并提供实用备考建议。',
    },

    # ============ KET听力技巧 ============
    {
        'col': 'ket_listen',
        'title': 'KET听力Part 1-4技巧详解：从基础到高分',
        'content': '''
        <h2>KET听力Part 1-4技巧详解：从基础到高分</h2>
        <p>KET听力考试共40分钟，分为4个部分，考察的是日常生活中的听力理解能力。与阅读不同，听力无法重复听取，所以策略和技巧尤为重要。</p>

        <h3>Part 1 - 单句理解</h3>
        <p><strong>形式：</strong>5个独立的句子，每个听一次</p>
        <p><strong>任务：</strong>选择与听到的句子意思相符的图片或选项</p>
        <p><strong>技巧：</strong>
        <ul>
            <li>快速浏览选项，预测可能的答案</li>
            <li>关注关键词和短语</li>
            <li>注意否定词（not, no, never）</li>
            <li>听完整句子再做选择</li>
        </ul>
        </p>

        <h3>Part 2 - 对话理解</h3>
        <p><strong>形式：</strong>5段对话，每段较短，听两次</p>
        <p><strong>任务：</strong>根据对话回答问题（通常是5个选择题）</p>
        <p><strong>技巧：</strong>
        <ul>
            <li>提前30秒预读问题</li>
            <li>在第一遍听时集中注意力</li>
            <li>记下关键信息（人物、地点、数字）</li>
            <li>注意转折词（but, however, actually）后的信息</li>
        </ul>
        </p>

        <h3>Part 3 - 长对话理解</h3>
        <p><strong>形式：</strong>1段较长对话或多人对话，听两次</p>
        <p><strong>任务：</strong>回答6个关于对话的问题</p>
        <p><strong>技巧：</strong>
        <ul>
            <li>快速浏览6个问题，了解话题</li>
            <li>做笔记，记录Who, What, Where, When, Why, How</li>
            <li>注意对话中的细节改变（如价格、时间调整）</li>
            <li>第二遍听时填补遗漏的答案</li>
        </ul>
        </p>

        <h3>Part 4 - 独白/讲座</h3>
        <p><strong>形式：</strong>1个较长的独白或讲座，听两次</p>
        <p><strong>任务：</strong>根据内容完成10个句子（填空或多选）</p>
        <p><strong>技巧：</strong>
        <ul>
            <li>预读待填空的句子，了解所需信息类型</li>
            <li>做详细笔记，包括数字、名称、日期</li>
            <li>注意同义表达（如不同的表述同一个概念）</li>
            <li>认真检查拼写和语法</li>
        </ul>
        </p>

        <h3>通用备考建议</h3>
        <ol>
            <li><strong>每天听15-20分钟：</strong>建立对英语的敏感度</li>
            <li><strong>看英文电视剧/电影：</strong>学习自然的发音和表达</li>
            <li><strong>做听力笔记：</strong>记录关键词而非整句</li>
            <li><strong>查阅听力文本：</strong>查证答案，学习新词汇</li>
            <li><strong>模拟考试：</strong>在规定时间内完成全套题目</li>
        </ol>
        ''',
        'desc': 'KET听力共4个部分，难度逐步递增。本文详细分析每部分的技巧和备考方法。',
    },

    # ============ 阅读文章 ============
    {
        'col': 'reading',
        'title': '英文阅读技巧：如何用Skimming和Scanning快速找到答案',
        'content': '''
        <h2>英文阅读技巧：如何用Skimming和Scanning快速找到答案</h2>
        <p>在英语学习中，阅读速度和理解准确性往往成为学生的痛点。特别是在考试环境下，时间压力会进一步降低理解质量。掌握两种基本的阅读技巧——skimming和scanning——能显著提升阅读效率。</p>

        <h3>什么是Skimming（略读）</h3>
        <p><strong>定义：</strong>快速浏览文章获取主要观点或主题，而不关注细节。</p>
        <p><strong>使用场景：</strong>
        <ul>
            <li>预览文章结构和内容</li>
            <li>找出每段的主题句</li>
            <li>确定文章的总体意思</li>
            <li>决定是否值得深入阅读</li>
        </ul>
        </p>
        <p><strong>操作步骤：</strong>
        <ol>
            <li>读标题和副标题</li>
            <li>读第一和最后一段</li>
            <li>快速浏览每段的第一句（通常是主题句）</li>
            <li>注意黑体词、数字和标点符号</li>
        </ol>
        </p>

        <h3>什么是Scanning（查读）</h3>
        <p><strong>定义：</strong>快速扫描文章寻找特定信息，如日期、数字、名字等。</p>
        <p><strong>使用场景：</strong>
        <ul>
            <li>找某个特定人物或地点</li>
            <li>找时间、日期或数字</li>
            <li>找答案中的关键词</li>
            <li>验证特定信息的准确性</li>
        </ul>
        </p>
        <p><strong>操作步骤：</strong>
        <ol>
            <li>确定你要查找的信息类型</li>
            <li>预测这个信息可能长什么样（如日期通常是XX/XX）</li>
            <li>从左到右、从上到下快速扫描</li>
            <li>找到后停止扫描，深入阅读相关段落</li>
        </ol>
        </p>

        <h3>实战示例</h3>
        <p><strong>题目：</strong>What time does the museum close?</p>
        <p>你可以预测答案可能是一个时间表达（如"5 PM"或"17:00"），然后扫描文本寻找时间词。一旦找到museum和closing time的相关信息，再仔细阅读那一段。</p>

        <h3>Skimming vs Scanning</h3>
        <table border="1" cellpadding="5">
            <tr>
                <td><strong>特点</strong></td>
                <td><strong>Skimming</strong></td>
                <td><strong>Scanning</strong></td>
            </tr>
            <tr>
                <td>目标</td>
                <td>获取总体理解</td>
                <td>查找具体信息</td>
            </tr>
            <tr>
                <td>阅读顺序</td>
                <td>从上到下，有系统</td>
                <td>跳跃式，按需要</td>
            </tr>
            <tr>
                <td>用眼方式</td>
                <td>浏览每一行</td>
                <td>快速扫过很多内容</td>
            </tr>
            <tr>
                <td>理解深度</td>
                <td>浅层理解</td>
                <td>局部深层理解</td>
            </tr>
        </table>

        <h3>为什么这些技巧很重要</h3>
        <ul>
            <li><strong>节省时间：</strong>在限时考试中至关重要</li>
            <li><strong>提高准确率：</strong>目标明确，减少歧义</li>
            <li><strong>增强信心：</strong>有策略的阅读比盲目阅读效果好</li>
            <li><strong>灵活应对：</strong>可根据不同题型调整策略</li>
        </ul>
        ''',
        'desc': '快速有效的阅读技巧是英语学习的核心能力。本文讲解略读和查读的原理与实战应用。',
    },

    {
        'col': 'reading',
        'title': '英语口语中的日常短语：学会这100个表达，和外国人聊天无压力',
        'content': '''
        <h2>英语口语中的日常短语：学会这100个表达，和外国人聊天无压力</h2>
        <p>很多学生的英语成绩不错，但一到实际交流就卡壳。这是因为日常口语和考试英语有很大差异。学会常用的日常短语和习语是提高口语能力的快捷方式。</p>

        <h3>问候和告别</h3>
        <ul>
            <li><strong>Hey, what's up?</strong> - 嘿，怎么样？（非常随意）</li>
            <li><strong>How have you been?</strong> - 你最近怎么样？（热情的问候）</li>
            <li><strong>I've got to run.</strong> - 我得走了</li>
            <li><strong>See you around.</strong> - 回头见（不确定何时见面）</li>
            <li><strong>Catch you later!</strong> - 待会儿见</li>
        </ul>

        <h3>表达意见和同意</h3>
        <ul>
            <li><strong>I think so too.</strong> - 我也这样认为</li>
            <li><strong>That sounds good to me.</strong> - 对我来说听起来不错</li>
            <li><strong>I couldn't agree more.</strong> - 我完全同意</li>
            <li><strong>Fair point!</strong> - 有道理！</li>
            <li><strong>You've got a point there.</strong> - 你说得有点道理</li>
            <li><strong>I beg to differ.</strong> - 我持不同意见</li>
        </ul>

        <h3>询问和帮助</h3>
        <ul>
            <li><strong>Can I give you a hand?</strong> - 我能帮你吗？</li>
            <li><strong>What's the matter?</strong> - 怎么了？</li>
            <li><strong>Need a hand with that?</strong> - 需要帮忙吗？</li>
            <li><strong>What's wrong?</strong> - 什么出问题了？</li>
            <li><strong>Don't worry about it.</strong> - 别担心</li>
        </ul>

        <h3>感谢和道歉</h3>
        <ul>
            <li><strong>Thanks a million!</strong> - 太感谢你了</li>
            <li><strong>I owe you one.</strong> - 我欠你一个人情</li>
            <li><strong>My bad.</strong> - 是我的错</li>
            <li><strong>Sorry about that.</strong> - 为此道歉</li>
            <li><strong>No worries!</strong> - 没事！（澳大利亚英语常用）</li>
        </ul>

        <h3>表达感情</h3>
        <ul>
            <li><strong>That's awesome!</strong> - 太棒了</li>
            <li><strong>I'm over the moon!</strong> - 我高兴极了</li>
            <li><strong>I'm fed up with this.</strong> - 我受够了</li>
            <li><strong>I'm so frustrated.</strong> - 我太沮丧了</li>
            <li><strong>That's hilarious!</strong> - 太搞笑了</li>
        </ul>

        <h3>实用建议</h3>
        <ol>
            <li><strong>听英文播客或YouTube：</strong>学习自然的表达方式</li>
            <li><strong>和语言交换伙伴练习：</strong>实战应用新表达</li>
            <li><strong>造句记忆：</strong>不要孤立地背短语</li>
            <li><strong>观看英文电视剧：</strong>在情境中学习口语</li>
            <li><strong>重复练习：</strong>直到成为肌肉记忆</li>
        </ol>
        ''',
        'desc': '日常口语表达是实用英语的核心。本文整理常用短语和习语，帮助提升交流能力。',
    },
]

def insert_article(conn, col_id, title, content, desc):
    """插入文章"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = """INSERT INTO ep_news
        (title, content, description, class1, addtime, updatetime, lang, wap_ok)
        VALUES (%s,%s,%s,%s,%s,%s,'cn',1)"""
    try:
        cur = conn.cursor()
        cur.execute(sql, (title, content, desc[:255], col_id, now, now))
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        print('  错误: {}'.format(e))
        return None


def main():
    print('\n' + '='*60)
    print('[{}] KET/PET英语学习 - 内容初始化'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('='*60)

    if DRY_RUN:
        print('⚠️  DRY RUN 模式 - 仅预览\n')

    # 过滤文章
    articles = ARTICLES
    if FILTER == 'ket':
        articles = [a for a in articles if a['col'].startswith('ket')]
        print('📌 仅生成KET文章\n')
    elif FILTER == 'pet':
        articles = [a for a in articles if a['col'].startswith('pet')]
        print('📌 仅生成PET文章\n')

    conn = None
    if not DRY_RUN:
        try:
            conn = pymysql.connect(**DB)
            print('✓ 数据库连接成功\n')
        except Exception as e:
            print('✗ 连接失败: {}\n'.format(e))
            return

    count = 0
    for article in articles:
        col_id = COLUMNS[article['col']]
        title = article['title']
        content = article['content']
        desc = article['desc']

        print('[{}] {}'.format(article['col'], title[:40]))

        if DRY_RUN:
            print('  -> [预览] 栏目ID: {}，摘要: {}'.format(col_id, desc[:50]))
        else:
            if conn:
                nid = insert_article(conn, col_id, title, content, desc)
                if nid:
                    print('  -> 入库 ID={}'.format(nid))
                    count += 1

        time.sleep(0.5)

    if conn:
        conn.close()

    print('\n' + '='*60)
    print('✓ 完成！共生成 {} 篇文章'.format(count if not DRY_RUN else len(articles)))
    print('='*60 + '\n')


if __name__ == '__main__':
    main()
