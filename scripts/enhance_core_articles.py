#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add article-specific practice blocks to the short, owned EPGO articles.

The script is dry-run by default.  On production, set EPGO_DB_CONFIG_SCRIPT to
the existing quality_monitor.py path so credentials stay outside this file:

  EPGO_DB_CONFIG_SCRIPT=/www/wwwroot/go.xiachaoqing.com/scripts/quality_monitor.py \
    python3 enhance_core_articles.py --dry-run
  ... --apply --backup /root/epgo_editorial_backup.json
"""
from __future__ import print_function

import argparse
import importlib.util
import json
import os
import sys
from datetime import datetime

import pymysql


ARTICLE_BLOCKS = {
    640: {
        "description": "用两周录音记录信息完整、表达清楚和互动修正，判断口语进步应该看哪些证据。",
        "html": """
<h2>网站练习：用证据记录口语进步</h2>
<p>口语进步不只体现在“说得更快”。每次录音后，先检查自己有没有回答完整，再检查句子之间是否有连接，最后看能不能根据对方的问题补充信息。这样比单纯比较口音更容易发现变化。</p>
<h3>三项记录</h3>
<ol><li><strong>信息完整：</strong>回答人物、时间、地点或原因时，至少给出两个相关信息。</li><li><strong>表达清楚：</strong>把一句过长的话拆成两句，避免因为追求复杂而说到一半停住。</li><li><strong>互动修正：</strong>对方没有听懂时，能用简单句换一种说法，而不是只重复原句。</li></ol>
<h3>自测题</h3>
<p>请用英语回答：<em>What did you do after school yesterday?</em> 第一遍只说事实，第二遍补充一个原因或感受。对比两次录音，分别标记“信息增加”和“停顿减少”的地方。</p>
<p><strong>参考标准：</strong>能说清楚做了什么、在哪里或和谁一起，并补充一个原因或感受，就已经完成了有效表达；不需要刻意使用生僻词。</p>
""",
    },
    639: {
        "description": "按可理解程度、重复意愿和延伸任务选择英语绘本，帮助家长安排一次真正能读完的阅读。",
        "html": """
<h2>网站练习：把绘本选择变成三步检查</h2>
<p>一本书是否适合孩子，不只看级别标签。先让孩子试读一小页：如果每句话都需要翻译，难度可能过高；如果完全没有新词和问题，重复价值又不够。最合适的材料应该让孩子大致看懂，同时保留少量可以通过上下文猜出的内容。</p>
<h3>选择前先看三点</h3>
<ul><li><strong>可理解程度：</strong>一页中大多数句子能独立读懂，少数关键词需要讲解。</li><li><strong>重复意愿：</strong>孩子愿意再次听或读，能指出喜欢的人物、动作或转折。</li><li><strong>延伸任务：</strong>读完后能画一幅图、说一句总结，或替换一个人物重新讲。</li></ul>
<h3>一次家庭试读</h3>
<p>先听原音，再由孩子选择一页朗读。家长只解释影响情节的词，不要逐词打断。读完问：<em>Who is in the story? What happened first? What happened next?</em></p>
<p><strong>参考标准：</strong>孩子能用自己的话说出人物和一个事件，并愿意继续读，就说明材料值得保留；如果只能逐句翻译，应先换更容易的读物。</p>
""",
    },
    638: {
        "description": "家庭每周四次短练习的任务、证据和中断恢复方法，帮助学习从一次突击变成稳定节奏。",
        "html": """
<h2>网站练习：一周四次短复习怎么排</h2>
<p>家庭复习最容易失败的地方，是把每次任务都安排得太大。可以把一周拆成四次 15～20 分钟：一次听力、一次阅读、一次词汇句型、一次口语或写作。每次只留下一个可以检查的结果，家长更容易判断孩子到底完成了什么。</p>
<h3>建议安排</h3>
<ol><li>周一：听一段熟悉材料，写下三个听到的关键词。</li><li>周三：读一篇短文，圈出一个转折词并说清它连接了什么。</li><li>周五：用本周词汇写两个自己的句子。</li><li>周日：录一分钟复述，记录一个做得好的地方和一个下周要改的地方。</li></ol>
<p>如果某次中断，不需要把任务加倍补回来。下一次从最短任务重新开始，并在记录表中写下中断原因：时间不够、材料太难，还是任务不清楚。</p>
<p><strong>参考标准：</strong>一周留下四份具体证据，比完成一次两小时突击更能帮助老师调整下一周计划。</p>
""",
    },
    637: {
        "description": "把测评分项、错误类型和时间投入转成可执行学习计划，而不是只盯着一个总分。",
        "html": """
<h2>网站练习：把测评结果变成下一周任务</h2>
<p>测评总分只能告诉我们结果，不能直接告诉我们该怎么练。先把错题按“词汇不认识、题干没读懂、证据找错、表达不完整”分组，再看哪一类错误出现最多。下一周只优先处理一个主要问题，计划才不会变成一长串口号。</p>
<h3>转换步骤</h3>
<ol><li>记录每个分项的正确率和完成时间。</li><li>给每道错题写一句真正的原因，而不是只写“粗心”。</li><li>选择一个高频错误，安排三次短练习，每次留下答案或录音。</li></ol>
<p>例如阅读题错在“把转折后的信息漏掉”，任务就应该是每天找出一段含 <em>but</em>、<em>however</em> 或 <em>although</em> 的句子，并说明前后观点如何变化。</p>
<p><strong>参考标准：</strong>计划中每一项都应该能回答“练什么、练几次、留下什么证据”。如果回答不了，就继续缩小任务。</p>
""",
    },
    636: {
        "description": "PET 听力长对话抓取变化、时间和最终决定的笔记法，减少听到关键词就急着选答案。",
        "html": """
<h2>网站练习：长对话只记变化和决定</h2>
<p>PET 长对话不要求把每句话写下来。笔记的作用是保留人物从“原来的想法”到“最后决定”的变化。听到地点、时间、价格或计划改变时，用箭头或简短词组记录，比抄完整句更可靠。</p>
<h3>四个信号</h3>
<ul><li><strong>原计划：</strong>人物一开始准备做什么。</li><li><strong>转折：</strong>出现 but、actually、instead 或问题原因。</li><li><strong>新信息：</strong>时间、地点、数量或条件发生变化。</li><li><strong>最终决定：</strong>对话结束时真正执行的安排。</li></ul>
<p>练习时可以先不看选项，只写“原计划 → 变化 → 最终决定”。第二遍再核对选项，检查自己是否被重复出现的旧信息干扰。</p>
<p><strong>参考标准：</strong>正确答案通常对应最后被确认的信息，而不是最早出现的关键词。</p>
""",
    },
    635: {
        "description": "PET 口语讨论的回应、理由和追问练习，帮助孩子在互动中完成观点表达。",
        "html": """
<h2>网站练习：先回应，再提出理由</h2>
<p>PET 口语讨论不是两个人轮流背答案。一个完整回应至少包括三步：先接住同伴的观点，再说自己的选择，最后给出一个具体理由。如果只说 <em>I agree</em> 或 <em>I think so</em>，对话很快就会中断。</p>
<h3>可直接套用的结构</h3>
<p><em>I agree with you because... However, I think ... may be better because...</em> 先回应并不代表必须同意，也可以礼貌地补充不同看法。说完后，再问一句 <em>What do you think?</em> 把话题交回给同伴。</p>
<p><strong>自测：</strong>选择“周末活动”或“学校社团”话题，连续完成“回应—理由—追问”三轮。录音后检查自己是否真的回应了对方，而不是只说自己的准备句。</p>
<p><strong>参考标准：</strong>每轮都有明确选择、具体理由和一次互动，就比单独堆叠高级词汇更有效。</p>
""",
    },
    634: {
        "description": "PET 写作中邮件与文章的读者、语气和结构选择，帮助孩子先完成沟通任务再润色句子。",
        "html": """
<h2>网站练习：先确定读者，再决定语气</h2>
<p>PET 写作落笔前先问三个问题：我在写给谁？对方需要知道什么？我希望对方做什么？写给朋友的邮件可以自然一些，写给不熟悉的人则要更完整、更礼貌。语气选对了，内容结构才不会跑偏。</p>
<h3>检查结构</h3>
<ol><li>开头说明写信或写文章的目的。</li><li>中间按题目要求逐项完成信息，不要只写自己最熟悉的一项。</li><li>结尾给出回应、建议或下一步安排。</li></ol>
<p>例如邀请朋友参加活动，不能只写活动很有趣，还要交代时间、地点和需要对方准备的事情。写完后用题目中的三个任务逐一打勾。</p>
<p><strong>参考标准：</strong>先确保每项任务都有信息，再检查连接词、时态和拼写；不要为了使用难词牺牲清楚度。</p>
""",
    },
    633: {
        "description": "PET 阅读同义替换的关键词拆解和范围核对方法，避免只凭相同单词寻找答案。",
        "html": """
<h2>网站练习：把题干改写成自己的关键词</h2>
<p>PET 阅读题干和原文常常不会使用完全相同的词。做题时先圈出题干中的人物、动作、时间和原因，再预测可能出现的同义表达。例如题干中的 <em>not happy</em> 可能对应原文的 <em>disappointed</em>，但还要回到完整句子核对范围。</p>
<h3>三步定位</h3>
<ol><li>删掉不影响定位的功能词，只保留核心信息。</li><li>把核心词换成一个简单的同义或解释性表达。</li><li>找到段落后，向前后各读一句，确认主语、时间和否定范围。</li></ol>
<p><strong>自测：</strong>选一道做错的题，把题干改写成三个中文关键词，再回到原文找对应句，写下“相同信息”和“容易误判的信息”。</p>
<p><strong>参考标准：</strong>定位只是第一步，答案必须同时满足题干的对象、范围和语气。</p>
""",
    },
    632: {
        "description": "PET 阅读长文选择题的题干改写、证据定位和排除推断方法，减少凭印象选答案。",
        "html": """
<h2>网站练习：先找证据，再判断作者意思</h2>
<p>长文选择题最容易出现“文章大概看懂，但选项总差一点”。原因通常是把自己的常识当成作者观点。先把题干改写成一个具体问题，再去段落中寻找能直接支持它的句子，最后排除扩大范围或改变语气的选项。</p>
<h3>证据表</h3>
<ul><li><strong>题目问什么：</strong>事实、原因、态度还是推断。</li><li><strong>原文证据：</strong>哪句话直接支持判断。</li><li><strong>选项问题：</strong>是否换了对象、时间、程度或因果关系。</li></ul>
<p>如果题目问作者态度，注意 <em>surprisingly</em>、<em>unfortunately</em>、<em>even though</em> 这类表达，它们往往比名词本身更能说明语气。</p>
<p><strong>参考标准：</strong>每个答案旁边都能写出原文依据；如果只能说“感觉像”，就还没有完成判断。</p>
""",
    },
    631: {
        "description": "KET 口语个人信息回答的完整句和录音复盘方法，让简短回答也有清楚结构。",
        "html": """
<h2>网站练习：把个人信息说成完整回答</h2>
<p>KET 口语第一部分的问题看起来简单，但只回答一个词很难展示表达能力。可以用“直接回答＋一个细节”的结构：先回答事实，再补充时间、原因、地点或感受。</p>
<h3>示例</h3>
<p>问题：<em>What do you do after school?</em><br>基础回答：<em>I go home.</em><br>完整回答：<em>I usually go home and read for twenty minutes because reading helps me relax.</em></p>
<p>练习时准备五个常见话题：学校、爱好、家庭、周末和朋友。每个话题录一段 20～30 秒的回答，第二遍只改一个问题，例如补充原因或减少重复的 <em>very</em>。</p>
<p><strong>参考标准：</strong>回答与问题相关，有一个具体细节，语法错误不会妨碍理解，就已经达成第一步目标。</p>
""",
    },
    630: {
        "description": "KET 图片故事如何用问题、行动和结果组织时间线，帮助孩子从看图说词发展到连续表达。",
        "html": """
<h2>网站练习：用时间线把三幅图连起来</h2>
<p>图片故事不需要一开始就追求复杂句。先回答每幅图的三个问题：谁在做什么？发生了什么变化？结果是什么？再用 <em>first</em>、<em>then</em>、<em>finally</em> 把三幅图连接起来。</p>
<h3>从词到句</h3>
<p>看到雨伞、男孩和公园，可以先写 <em>a boy / carry an umbrella / go to the park</em>，再组合成 <em>First, a boy carried an umbrella to the park.</em> 最后加上原因或结果：<em>He wanted to help his sister.</em></p>
<p><strong>自测：</strong>随机选择三张图片，每张先说一句事实，再补一句变化。录音后检查是否出现了人物、动作和结果，而不是只罗列名词。</p>
<p><strong>参考标准：</strong>故事顺序清楚、每幅图都有信息、连接词使用自然，比使用少量高级词更重要。</p>
""",
    },
    629: {
        "description": "KET 邮件写作如何先完成三项沟通任务，再检查语气和格式，避免只写自己熟悉的内容。",
        "html": """
<h2>网站练习：先完成三项任务，再检查邮件</h2>
<p>KET 邮件写作最稳妥的做法不是先想漂亮句子，而是先把题目要求拆成三个动作。每完成一项就做标记，确保对方真正能从邮件中得到需要的信息。</p>
<h3>四格检查表</h3>
<ol><li>开头回应对方的来信或问题。</li><li>任务一：补充第一个具体信息。</li><li>任务二：补充第二个具体信息或提出建议。</li><li>结尾说明希望对方下一步做什么，并使用合适的结束语。</li></ol>
<p>例如题目要求介绍一次活动、说明时间并邀请朋友，三个部分缺一不可。写完后把每个任务对应的句子圈出来，再检查人称、时态和标点。</p>
<p><strong>参考标准：</strong>内容完整、语气适合朋友之间的交流、句子清楚，就比堆砌复杂表达更稳。</p>
""",
    },
    628: {
        "description": "KET 开放完形如何先判断词性、搭配和句子关系，把猜答案变成有依据的检查。",
        "html": """
<h2>网站练习：开放完形先判断需要哪一类词</h2>
<p>开放完形不能只看空格前面的一个词。先读完整句子，再观察空格在句中的位置：它需要名词、动词、形容词、介词，还是一个连接上下文的词。判断词性后，再检查固定搭配和单复数。</p>
<h3>三层检查</h3>
<ol><li><strong>句法：</strong>空格在句子中承担什么成分。</li><li><strong>搭配：</strong>前后词是否形成常见表达，例如 <em>interested in</em>。</li><li><strong>语境：</strong>填入后是否符合整段的时间、人物和逻辑。</li></ol>
<p>填完后至少从头到尾再读一遍。有些答案局部看起来正确，但会和下一句的转折或代词指代冲突。</p>
<p><strong>参考标准：</strong>每个答案都能说出“词性＋搭配或语境依据”，才算真正完成检查。</p>
""",
    },
    627: {
        "description": "KET 阅读匹配题如何拆解人物需求并核对多个条件，避免看到相同关键词就立即配对。",
        "html": """
<h2>网站练习：匹配题先拆需求，再核对条件</h2>
<p>匹配题中的人物和短文可能使用不同表达。先把人物需求拆成“想做什么、时间限制、地点或对象”三个条件，再在每篇短文中寻找能同时满足的证据。只出现一个相同单词，不代表真正匹配。</p>
<h3>记录方式</h3>
<p>可以在草稿上写成：<em>人物 A = activity + weekend + with a friend</em>。找到候选短文后，分别在原文中圈出活动、时间和对象，少一个条件就先保留而不要确定。</p>
<p><strong>自测：</strong>做完一道题后，解释为什么另外两个选项不符合。能说清“时间不对”或“对象不对”，说明你是在核对条件，而不是凭关键词猜。</p>
<p><strong>参考标准：</strong>答案需要满足人物的整体需求，不能只满足其中一个词。</p>
""",
    },
    626: {
        "description": "KET 阅读短通知如何定位动作、时间、对象和限制条件，先确认信息再选择答案。",
        "html": """
<h2>网站练习：短通知先找四类信息</h2>
<p>短通知字数不多，但一个介词或时间词就可能改变答案。阅读时先找四类信息：谁要做什么、什么时候做、对谁有效、有没有限制条件。把这些信息放在一起，才能判断通知真正要求的动作。</p>
<h3>四问法</h3>
<ol><li><strong>动作：</strong>需要报名、携带、等待还是改变地点。</li><li><strong>时间：</strong>开始时间、截止时间和持续时间是否不同。</li><li><strong>对象：</strong>通知针对所有人，还是只针对某个小组。</li><li><strong>限制：</strong>是否需要提前预约、携带材料或满足年龄条件。</li></ol>
<p>遇到 <em>until</em>、<em>before</em>、<em>only</em>、<em>instead</em> 时要特别慢下来，它们经常决定选项能不能成立。</p>
<p><strong>参考标准：</strong>先用中文或简单英文复述通知，再看选项，能减少被表面关键词带偏。</p>
""",
    },
    625: {
        "description": "三个月熏听如何选择可理解材料、安排输出并用证据判断效果，避免只播放却没有学习反馈。",
        "html": """
<h2>网站练习：熏听计划要留下可观察的结果</h2>
<p>熏听不是把音频一直放在后台就结束了。材料要大致听懂，长度要能重复，三个月内还要逐步加入跟读、复述或关键词记录。每周只增加一个难度，孩子更容易保持。</p>
<h3>三阶段安排</h3>
<ol><li><strong>第一个月：</strong>固定一套短材料，先听懂场景和人物，积累重复次数。</li><li><strong>第二个月：</strong>每周选一段跟读，记录两个连读或重音现象。</li><li><strong>第三个月：</strong>听完后用自己的话复述主要信息，偶尔加入稍长材料。</li></ol>
<p>每周留下三项证据：听过几次、能说出什么、下次要改什么。这样才能区分“听过”与“听懂并能使用”。</p>
<p><strong>参考标准：</strong>不追求每天时长极长，而是让材料难度、重复次数和输出任务保持稳定。</p>
""",
    },
    624: {
        "description": "背过的单词如何放进句子、搭配、替换和真实任务里，帮助词汇从认识变成能表达。",
        "html": """
<h2>网站练习：一个单词至少完成四次使用</h2>
<p>只会说出中文意思，说明单词还没有进入可使用状态。可以为一个新词安排四次接触：先放回原句，再找一个常见搭配，替换成自己的信息，最后在口头或书面任务中用一次。</p>
<h3>示例：<em>suggest</em></h3>
<p>原句：<em>She suggested going by bus.</em> 搭配：<em>suggest doing something</em>。替换：<em>I suggested meeting at six.</em> 任务：给朋友提出一个周末安排，并说明原因。</p>
<p>复习时不要只遮住中文意思，可以遮住搭配的一部分，让孩子先根据句子结构补出来，再检查拼写和语气。</p>
<p><strong>参考标准：</strong>能在新情境中正确使用单词，才是真正的“会用”；单独认读只是第一步。</p>
""",
    },
    623: {
        "description": "用四项最小记录复盘英语学习计划，决定下周只调整哪一个问题，避免计划越写越复杂。",
        "html": """
<h2>网站练习：每周复盘只看四项记录</h2>
<p>复盘不是重新写一份漂亮计划，而是用本周证据做一个小决定。建议只记录完成次数、最常见错误、最有效的任务和下周要保留的一件事。记录越简单，越容易坚持。</p>
<h3>四项记录</h3>
<ul><li>完成了几次，哪一次最容易开始。</li><li>哪一类错误重复出现，是否影响理解。</li><li>哪种任务让孩子能留下清楚答案、录音或作品。</li><li>下周只调整一个变量：时间、难度、材料或反馈方式。</li></ul>
<p>例如本周阅读完成三次，但每次都超时，下周先减少文章长度而不是增加学习时间。等速度稳定后，再逐步恢复长度。</p>
<p><strong>参考标准：</strong>复盘最后应该得到一个明确动作，而不是一页无法执行的批评。</p>
""",
    },
    622: {
        "description": "孩子每天听英语却不愿开口时，用 15 分钟完成整体听、跟读、替换和复述。",
        "html": """
<h2>网站练习：15 分钟家庭陪练四步走</h2>
<p>孩子不愿开口时，先不要要求完整背诵。把一次陪练拆成四步，每一步都很短：第一遍整体听，第二遍跟读一句，第三遍替换一个词，第四遍用自己的话复述。</p>
<h3>具体流程</h3>
<ol><li>2 分钟：只听材料，猜人物和场景。</li><li>5 分钟：选择两句跟读，关注节奏而不是口音。</li><li>4 分钟：替换人物、地点或动作，造出自己的句子。</li><li>4 分钟：不看原文复述主要信息，卡住时允许回听。</li></ol>
<p>家长反馈时只指出一个优点和一个下一步，例如“你把时间说清楚了，下次再补充原因”。具体反馈比反复说“大胆一点”更容易让孩子继续表达。</p>
<p><strong>参考标准：</strong>每天留下一个完整句或一段短录音，就比强迫孩子一次说很长更可持续。</p>
""",
    },
    651: {
        "description": "KET/PET 考前一周按常见失误做短练习、保持熟悉节奏，并核对考点要求。",
        "html": """
<h2>网站练习：考前一周只做可控调整</h2>
<p>考前一周不适合突然更换整套材料或把学习时间翻倍。先查看最近三次练习中最常见的两个错误，再安排短而熟悉的任务，目标是保持判断节奏和信心。</p>
<h3>七天检查表</h3>
<ul><li>前四天：每天练一个分项，保留错题原因或录音。</li><li>第五天：完成一次小范围综合练习，检查时间分配。</li><li>第六天：只复习高频错误和常见表达，不再追新难题。</li><li>第七天：确认考试材料、时间和路线，保证睡眠。</li></ul>
<p><strong>参考标准：</strong>考前最后一周的任务是稳定已经学会的能力，而不是用陌生难题制造新的焦虑。</p>
""",
    },
}


def load_db_config():
    path = os.environ.get("EPGO_DB_CONFIG_SCRIPT", "")
    if not path:
        raise RuntimeError("set EPGO_DB_CONFIG_SCRIPT to an existing server-side DB config script")
    spec = importlib.util.spec_from_file_location("epgo_db_config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config = getattr(module, "DB", None) or getattr(module, "DEFAULT_DB", None)
    if not config:
        raise RuntimeError("no DB or DEFAULT_DB mapping found in config script")
    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write changes; default is dry-run")
    parser.add_argument("--backup", default="", help="JSON backup path required with --apply")
    args = parser.parse_args()
    if args.apply and not args.backup:
        parser.error("--backup is required with --apply")

    conn = pymysql.connect(**load_db_config(), cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    ids = tuple(ARTICLE_BLOCKS)
    placeholders = ",".join(["%s"] * len(ids))
    cur.execute(
        "SELECT id,title,content,description,class1,issue,updatetime FROM ep_news "
        "WHERE recycle=0 AND id IN (" + placeholders + ")",
        ids,
    )
    rows = {int(row["id"]): row for row in cur.fetchall()}
    missing = sorted(set(ids) - set(rows))
    if missing:
        raise RuntimeError("missing article IDs: {}".format(",".join(map(str, missing))))

    updates = []
    for article_id, block in ARTICLE_BLOCKS.items():
        row = rows[article_id]
        marker = "<!-- epgo-editorial-v2:{} -->".format(article_id)
        if marker in (row["content"] or ""):
            print("skip already enhanced", article_id, row["title"])
            continue
        content = (row["content"] or "").rstrip() + "\n" + marker + block["html"]
        updates.append((article_id, row, content, block["description"]))
        print("plan", article_id, row["title"], "bytes", len(row["content"] or ""), "->", len(content))

    if not args.apply:
        print("dry-run only; planned updates:", len(updates))
        conn.close()
        return

    backup = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "article_ids": list(ids),
        "rows": rows,
    }
    with open(args.backup, "w", encoding="utf-8") as fh:
        json.dump(backup, fh, ensure_ascii=False, default=str)

    try:
        for article_id, row, content, description in updates:
            cur.execute(
                "UPDATE ep_news SET content=%s,description=%s,issue='editorial-v2',updatetime=NOW() WHERE id=%s",
                (content, description, article_id),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("updated", len(updates), "articles; backup", args.backup)


if __name__ == "__main__":
    main()
