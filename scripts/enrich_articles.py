#!/usr/bin/env python3
"""
扩充文章内容，为简短的文章添加更详实的学习建议、例子和实用技巧
在服务器上直接运行

用法:
    python3 enrich_articles.py              # 扩充所有内容短于 300 字的文章
    python3 enrich_articles.py --dry-run    # 预览模式
    python3 enrich_articles.py --class 101  # 只扩充特定栏目的文章
"""

import os
import sys
import argparse
import logging
from datetime import datetime

try:
    import pymysql
except ImportError:
    print("缺少依赖，请运行: pip3 install pymysql")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# ─── 配置 ───────────────────────────────────────────────
DB = dict(
    host="127.0.0.1", port=3306,
    user="xiachaoqing", password="***REMOVED***",
    database="epgo_db", charset="utf8mb4"
)

# 内容扩展模板库
CONTENT_EXTENSIONS = {
    # KET 相关
    101: {
        "keywords": ["词汇", "阅读", "写作", "听力", "备考"],
        "extension": """
<h3>高频考点速记</h3>
<ul>
  <li><strong>词汇积累</strong>：KET 要求掌握约 1500 个词汇。建议用词汇卡片或App辅助记忆，每天20-30个为宜。</li>
  <li><strong>语法核心</strong>：一般过去式、现在完成式、被动语态是KET考查重点，务必掌握构成和用法。</li>
  <li><strong>阅读速率</strong>：平均每分钟 100-120 词为目标，通过略读和扫读训练可快速提升。</li>
  <li><strong>听力技巧</strong>：注意开头和结尾信息，数字、地点、人名是常考细节。</li>
  <li><strong>写作要点</strong>：结构完整、表达准确、逻辑清晰是评分重点。勿过度修辞，简洁达意为上。</li>
</ul>

<h3>周期复习计划</h3>
<table border="1" cellpadding="8" cellspacing="0" style="width:100%; border-collapse:collapse;">
  <tr style="background:#f0f0f0;">
    <th>周期</th>
    <th>学习重点</th>
    <th>建议时间</th>
  </tr>
  <tr>
    <td>第1周</td>
    <td>词汇+基础语法第一轮</td>
    <td>每天1.5小时</td>
  </tr>
  <tr>
    <td>第2-3周</td>
    <td>阅读题型+听力基础</td>
    <td>每天2小时</td>
  </tr>
  <tr>
    <td>第4周</td>
    <td>模拟考试+查漏补缺</td>
    <td>每天1.5小时</td>
  </tr>
</table>

<h3>常见误区避坑</h3>
<ul>
  <li>❌ 盲目刷题而不总结：做题本质是暴露问题。每做完一套题，必须复盘错因。</li>
  <li>❌ 忽视听力和口语：KET考查四技能，听力和口语往往是弱项。建议从第一周就开始坚持听。</li>
  <li>❌ 词汇孤立记忆：单词需放在句子和语境中学习，效率会高得多。</li>
  <li>❌ 考前突击：KET是考查综合能力的考试，短期突击效果有限。稳定的长期学习才是保障。</li>
</ul>

<h3>学习资源推荐</h3>
<p>
  • <strong>官方真题集</strong>：Cambridge KET 官方公开试卷（PDF 或书籍版）<br/>
  • <strong>词汇App</strong>：Anki、不背单词等支持定制词库<br/>
  • <strong>听力练习</strong>：BBC Learning English 中级内容、Podcast 英语学习频道<br/>
  • <strong>写作反馈</strong>：Lang-8 或本地英语学习小组的同学互批
</p>
"""
    },

    # PET 相关
    102: {
        "keywords": ["B1", "真题", "写作", "阅读"],
        "extension": """
<h3>PET 考查要点详解</h3>
<ul>
  <li><strong>阅读理解深度</strong>：PET 阅读不仅考"找信息"，更考"理解隐含意思"。同义替换、推理判断是难点。</li>
  <li><strong>写作完整度</strong>：150 字以上短文写作，需展现完整的观点表达能力和语言多样性。</li>
  <li><strong>听力语速加快</strong>：相比KET，PET听力语速约快20%，信息密度更高。需提前适应。</li>
  <li><strong>口语互动性</strong>：PET 口语考查真实对话能力，不是背诵模板。要有即时反应能力。</li>
  <li><strong>词汇深度</strong>：PET 要求约 2500 词，且包括短语搭配和习语。</li>
</ul>

<h3>分项备考进度表</h3>
<table border="1" cellpadding="8" cellspacing="0" style="width:100%; border-collapse:collapse;">
  <tr style="background:#f0f0f0;">
    <th>技能</th>
    <th>周期1-2</th>
    <th>周期3-4</th>
    <th>周期5-6</th>
  </tr>
  <tr>
    <td>阅读</td>
    <td>单题型练习</td>
    <td>混合题型</td>
    <td>全真模拟</td>
  </tr>
  <tr>
    <td>写作</td>
    <td>结构学习+模板</td>
    <td>独立写作</td>
    <td>互批与修改</td>
  </tr>
  <tr>
    <td>听力</td>
    <td>基础单词辨音</td>
    <td>段落理解</td>
    <td>全文概括</td>
  </tr>
  <tr>
    <td>口语</td>
    <td>单词发音</td>
    <td>短句表达</td>
    <td>对话演练</td>
  </tr>
</table>

<h3>备考时间规划</h3>
<p>
  建议总周期 8-12 周。如时间紧张，可在强项上时间相对少投，在弱项上增加投入。<br/>
  每周安排 1-2 套全真模拟考，找到自己的做题节奏和时间分配策略。
</p>

<h3>常见失分原因复盘</h3>
<ul>
  <li><strong>阅读</strong>：字面意思和引申义混淆；信息遗漏导致选错</li>
  <li><strong>写作</strong>：表达不够自然；缺少举例或展开</li>
  <li><strong>听力</strong>：一个单词没听清就放弃了后续内容；速度跟不上</li>
  <li><strong>口语</strong>：过度紧张导致表达中断；没有充分理解考官提问</li>
</ul>
"""
    },

    # 阅读相关
    103: {
        "keywords": ["阅读技巧", "短文精读"],
        "extension": """
<h3>阅读方法论体系</h3>
<ul>
  <li><strong>略读 (Skimming)</strong>：快速浏览全文获取主旨。不读每个词，而是抓题目、小标题和首尾句。</li>
  <li><strong>扫读 (Scanning)</strong>：带着具体问题快速查找关键信息。眼睛沿着预期答案特征扫过文本。</li>
  <li><strong>精读 (Detailed Reading)</strong>：逐句理解，捕捉语法结构和修辞手法。用于难题和长句理解。</li>
  <li><strong>批判性阅读</strong>：不盲目接受观点，识别作者立场、论证方式和可能的逻辑漏洞。</li>
</ul>

<h3>主题相关词汇积累</h3>
<p>本篇涉及的主题相关高频词汇和短语搭配，建议收集到笔记本，配合具体例句理解。</p>

<h3>分段理解检查清单</h3>
<ul>
  <li>□ 段落主题句是什么？</li>
  <li>□ 段落内部逻辑是什么？（时间顺序/因果/对比）</li>
  <li>□ 本段对应的题目是哪些？</li>
  <li>□ 本段有哪些易混淆或难理解的表达？</li>
  <li>□ 我能否用自己的话总结本段内容？</li>
</ul>

<h3>课后练习建议</h3>
<p>
  1. 完成本文对应的理解题<br/>
  2. 标记出文中的难句子，逐句分析语法结构<br/>
  3. 复述文章主要观点（口头或书面）<br/>
  4. 查找3-5个新词汇，造句练习<br/>
  5. 思考：我的阅读理解有什么弱点需要改进？
</p>
"""
    },

    # 演讲相关
    104: {
        "keywords": ["演讲", "表达"],
        "extension": """
<h3>英语演讲的三大支柱</h3>
<ul>
  <li><strong>逻辑清晰</strong>：观点明确 → 论据充分 → 结论有力。不要信息堆砌，而要有理有据。</li>
  <li><strong>语言自然</strong>：避免过度复杂的句子。日常化表达往往比花哨修辞更有感染力。</li>
  <li><strong>心理建设</strong>：讲话时紧张很正常。关键是管理紧张情绪，让观众感受到你的热情而非焦虑。</li>
</ul>

<h3>演讲结构标准框架</h3>
<table border="1" cellpadding="8" cellspacing="0" style="width:100%; border-collapse:collapse;">
  <tr style="background:#f0f0f0;">
    <th>环节</th>
    <th>占比</th>
    <th>关键任务</th>
  </tr>
  <tr>
    <td>开场 (Opening)</td>
    <td>10%</td>
    <td>吸引注意力，介绍话题，设立预期</td>
  </tr>
  <tr>
    <td>主体 (Body)</td>
    <td>75%</td>
    <td>分点展开，每点配例子或数据</td>
  </tr>
  <tr>
    <td>收尾 (Conclusion)</td>
    <td>15%</td>
    <td>总结观点，升华意义，呼吁行动</td>
  </tr>
</table>

<h3>常用开场和结尾模板</h3>
<p>
  <strong>开场示例：</strong><br/>
  • Good morning, everyone. I'm here today to talk about...<br/>
  • Have you ever wondered why...? That's what I'd like to explore with you.<br/>
  • Let me start with a question: ...<br/>
  <br/>
  <strong>结尾示例：</strong><br/>
  • In conclusion, the key takeaway is...<br/>
  • So, let's remember that... and take action by...<br/>
  • Thank you for listening. I'd be happy to answer any questions.
</p>

<h3>表达自然度提升技巧</h3>
<ul>
  <li><strong>使用连接词</strong>：first, then, however, on the other hand ... 帮助观众跟上思路</li>
  <li><strong>适度停顿</strong>：别连贯讲个不停。停顿让观众消化，也给自己缓冲时间。</li>
  <li><strong>语调升降变化</strong>：用抑扬顿挫表达热情，声调平如水不会吸引人。</li>
  <li><strong>肢体语言</strong>：自然的手势、眼神接触都加强表现力。但别过度表演。</li>
  <li><strong>互动感</strong>：偶尔向观众提问，邀请反馈，制造互动感。</li>
</ul>

<h3>演讲排练检查清单</h3>
<ul>
  <li>□ 能否不看稿件流畅讲完？</li>
  <li>□ 重点突出了吗？</li>
  <li>□ 时间把控好了吗？</li>
  <li>□ 有没有令人困惑的表达需要简化？</li>
  <li>□ 肢体和眼神自然吗？</li>
</ul>
"""
    },

    # 每日英语相关
    105: {
        "keywords": ["每日表达", "日常"],
        "extension": """
<h3>今日表达在实际场景中的应用</h3>
<p>
  这些表达不仅适用于教科书，更是日常交流中的高频用语。理解其背后的社交语境和使用条件，
  比单纯背诵更能帮助你自然地运用。
</p>

<h3>相关短语搭配与变体</h3>
<ul>
  <li>记住不仅是单个短语，还要学习其常用搭配和时态变化</li>
  <li>例如：not only ... but also, both ... and, either ... or 等的灵活使用</li>
  <li>注意英美表达的微妙区别</li>
</ul>

<h3>对话示例与模拟练习</h3>
<p>
  以下是包含今日表达的真实对话场景。建议和学习伙伴轮流扮演两个角色，增强实战感。
</p>

<h3>常见误用陷阱</h3>
<ul>
  <li>❌ 中文思维直译：很多中文自然的表达在英文里不地道</li>
  <li>❌ 时态混乱：同一段对话里跳跃不同时态</li>
  <li>❌ 忽视上下文：同样的词汇在不同语境里含义或用法不同</li>
</ul>

<h3>巩固与扩展</h3>
<ul>
  <li>✓ 今天学的表达，明天是否能在新语境里重新组织使用？</li>
  <li>✓ 能否想到3-5个近义的表达方式？</li>
  <li>✓ 这个表达和你之前学的某个表达有什么联系？</li>
  <li>✓ 你在真实生活或剧集中见过这个表达吗？</li>
</ul>

<h3>每日微习惯建议</h3>
<p>
  不要一次学完就忘。建议：<br/>
  📅 第1天：学习，做题<br/>
  📅 第2天：复习，造句<br/>
  📅 第3天：应用，创作例句<br/>
  📅 第7天：再次复习，整理到主题笔记<br/>
  📅 第30天：在真实对话中主动使用
</p>
"""
    },
}

# 其他栏目的通用扩展
DEFAULT_EXTENSION = """
<h3>本篇核心知识点</h3>
<ul>
  <li>深化理解：本文涉及的关键概念和解题思路</li>
  <li>高频考点：总结本主题中容易出错或高频出现的题目类型</li>
  <li>知识联系：本知识点与之前学过内容的关联与区别</li>
</ul>

<h3>进阶拓展建议</h3>
<p>
  学完本篇后，建议进一步探索相关的进阶话题，比如：
</p>
<ul>
  <li>相似题型的变体形式</li>
  <li>更复杂的语境应用</li>
  <li>相关话题的深度思考</li>
</ul>

<h3>复习与巩固计划</h3>
<ul>
  <li>次日复习：回看本文标题，不看正文能否回忆要点？</li>
  <li>一周后：完成本文对应的练习题，检验理解程度</li>
  <li>两周后：整理到笔记本或知识管理工具，建立主题体系</li>
  <li>一月后：回顾，思考应用场景与价值</li>
</ul>

<h3>错题反思模板</h3>
<ul>
  <li>我为什么做错了？（知识缺陷 / 理解不足 / 粗心）</li>
  <li>正确答案背后的原理是什么？</li>
  <li>我可以如何改进，避免再犯同样的错误？</li>
  <li>这个错误暴露出我学习方法中的哪些问题？</li>
</ul>
"""

# ─── 工具函数 ─────────────────────────────────────────────

def get_content_extension(class_id, title, content):
    """根据栏目和标题，选择合适的内容扩展"""
    if class_id in CONTENT_EXTENSIONS:
        template = CONTENT_EXTENSIONS[class_id]
        # 检查标题或内容中是否包含关键词
        for keyword in template["keywords"]:
            if keyword.lower() in title.lower() or keyword.lower() in content.lower():
                return template["extension"]
    return DEFAULT_EXTENSION


def enrich_article(article_id, class_id, title, current_content, dry_run=False):
    """扩充单篇文章"""
    current_len = len(current_content)

    # 内容长度超过 500 字（去HTML标签）的不再扩充
    if current_len > 2000:
        log.debug("文章 %d 已足够丰富 (%d字), 跳过", article_id, current_len)
        return False

    extension = get_content_extension(class_id, title, current_content)
    new_content = current_content + extension

    if not dry_run:
        conn = pymysql.connect(**DB)
        cur = conn.cursor()
        try:
            cur.execute("UPDATE ep_news SET content=%s WHERE id=%s", (new_content, article_id))
            conn.commit()
            log.info("✓ 文章 %d《%s》已扩充 (原 %d 字 → 约 %d 字)",
                    article_id, title[:30], current_len, len(new_content))
            return True
        finally:
            cur.close()
            conn.close()
    else:
        log.info("[DRY] 文章 %d《%s》将扩充 (原 %d 字 → 约 %d 字)",
                article_id, title[:30], current_len, len(new_content))
        return True


def process_articles(class_id=None, dry_run=False):
    """批量扩充文章"""
    conn = pymysql.connect(**DB)
    cur = conn.cursor(pymysql.cursors.DictCursor)

    log.info("=" * 60)
    log.info("开始扩充文章内容")
    log.info("=" * 60)

    if dry_run:
        log.warning("⚠ 预览模式，不会实际修改数据库")

    # 查询需要扩充的文章
    if class_id:
        sql = """
            SELECT id, class1, title, content FROM ep_news
            WHERE recycle=0 AND class1=%s AND LENGTH(content) < 2000
            ORDER BY id DESC LIMIT 100
        """
        cur.execute(sql, (class_id,))
    else:
        sql = """
            SELECT id, class1, title, content FROM ep_news
            WHERE recycle=0 AND LENGTH(content) < 2000
            ORDER BY class1, id DESC LIMIT 500
        """
        cur.execute(sql)

    articles = cur.fetchall()
    cur.close()
    conn.close()

    if not articles:
        log.info("没有需要扩充的文章")
        return 0

    log.info("共发现 %d 篇内容短于 2000 字的文章", len(articles))
    log.info("")

    count = 0
    for article in articles:
        if enrich_article(
            article["id"],
            article["class1"],
            article["title"],
            article["content"],
            dry_run=dry_run
        ):
            count += 1

    log.info("")
    log.info("=" * 60)
    log.info("✅ 完成！共扩充 %d 篇文章", count)
    log.info("=" * 60)

    return count


def main():
    parser = argparse.ArgumentParser(description="扩充文章内容")
    parser.add_argument("--class", type=int, dest="class_id", default=None,
                        help="只扩充指定栏目 ID 的文章")
    parser.add_argument("--dry-run", action="store_true",
                        help="预览模式，不实际修改数据库")
    args = parser.parse_args()

    process_articles(class_id=args.class_id, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
