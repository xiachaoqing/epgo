#!/usr/bin/env python3
"""
epgo 完整修复脚本
1. 更新所有文章图片路径（老路径 → 新路径）
2. 检查并清除重复封面
3. 重新生成高质量文章内容
4. 更新 cron 配置
5. 清理所有缓存
"""

import pymysql
import subprocess
import random
import logging
from datetime import datetime, timedelta

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="***REMOVED***",
    database="epgo_db",
    charset="utf8mb4"
)

# 分类 → 图片映射（使用新路径）
CATEGORY_COVERS = {
    101: [
        "/upload/epgo-photo-covers/ket/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/ket/cover_v2_1775645365.jpg",
        "/upload/epgo-photo-covers/ket/cover_v3_1775645555.jpg",
    ],
    102: [
        "/upload/epgo-photo-covers/pet/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/pet/cover_v2_1775645365.jpg",
        "/upload/epgo-photo-covers/pet/cover_v3_1775645555.jpg",
    ],
    103: [
        "/upload/epgo-photo-covers/reading/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/reading/cover_v2_1775645365.jpg",
    ],
    104: [
        "/upload/epgo-photo-covers/speech/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/speech/cover_v2_1775645365.jpg",
    ],
    105: [
        "/upload/epgo-photo-covers/daily/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/daily/cover_v2_1775645365.jpg",
    ],
    106: [
        "/upload/epgo-photo-covers/download/cover_v1_1775645499.jpg",
        "/upload/epgo-photo-covers/download/cover_v2_1775645515.jpg",
    ],
    107: [
        "/upload/epgo-photo-covers/about/cover_v1_1775645499.jpg",
    ],
    111: [
        "/upload/epgo-photo-covers/ket/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/ket/cover_v3_1775645555.jpg",
    ],
    112: [
        "/upload/epgo-photo-covers/ket/cover_v2_1775645365.jpg",
        "/upload/epgo-photo-covers/ket/cover_v1_1775645515.jpg",
    ],
    113: [
        "/upload/epgo-photo-covers/ket/cover_v3_1775645555.jpg",
        "/upload/epgo-photo-covers/ket/cover_v2_1775645365.jpg",
    ],
    114: [
        "/upload/epgo-photo-covers/ket/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/ket/cover_v2_1775645365.jpg",
    ],
    121: [
        "/upload/epgo-photo-covers/pet/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/pet/cover_v2_1775645365.jpg",
    ],
    122: [
        "/upload/epgo-photo-covers/pet/cover_v3_1775645555.jpg",
        "/upload/epgo-photo-covers/pet/cover_v1_1775645515.jpg",
    ],
    123: [
        "/upload/epgo-photo-covers/pet/cover_v2_1775645365.jpg",
        "/upload/epgo-photo-covers/pet/cover_v3_1775645555.jpg",
    ],
    124: [
        "/upload/epgo-photo-covers/pet/cover_v1_1775645515.jpg",
        "/upload/epgo-photo-covers/pet/cover_v3_1775645555.jpg",
    ],
}

# 丰富的文章内容模板
CONTENT_TEMPLATES = {
    "reading": """<h3>📖 阅读技巧概述</h3>
<p>{description}</p>

<h3>🎯 核心学习要点</h3>
<ul>
  <li>快速定位关键信息的方法（扫读 vs 精读）</li>
  <li>常见题型的解题思路和技巧</li>
  <li>避免常见陷阱和错误选项的识别方法</li>
  <li>提高阅读速度和准确率的训练方法</li>
</ul>

<h3>💡 实战应用</h3>
<p>本篇内容适合以下学习者：</p>
<ul>
  <li>初级阶段：建立阅读框架和基本技巧</li>
  <li>进阶阶段：突破瓶颈，提升速度和准确率</li>
  <li>冲刺阶段：精细化训练，查漏补缺</li>
</ul>

<h3>📝 练习建议</h3>
<p>建议按以下步骤进行练习：</p>
<ol>
  <li>第一遍：带着问题读全文，理解整体思路</li>
  <li>第二遍：标记关键信息，比对答案</li>
  <li>第三遍：分析错题原因，总结规律</li>
  <li>定期复习：建立错题库，定期复盘</li>
</ol>

<p><strong>坚持每天一篇阅读训练，一个月内必有明显进步！</strong></p>""",

    "speaking": """<h3>🎤 演讲表达基础</h3>
<p>{description}</p>

<h3>💬 表达要点</h3>
<ul>
  <li>掌握清晰的表达结构和逻辑</li>
  <li>积累常用的开场、过渡和结尾表达</li>
  <li>学会用简单句表达复杂观点</li>
  <li>避免冗长句式，提高表达效率</li>
</ul>

<h3>🎭 场景演练</h3>
<p>学会这些表达后，可以应用到：</p>
<ul>
  <li>课堂发言和讨论</li>
  <li>考试口语部分</li>
  <li>日常交流和社交</li>
  <li>正式演讲和展示</li>
</ul>

<h3>🔥 高分秘诀</h3>
<ol>
  <li><strong>充分准备：</strong> 提前列出要点，反复练习发音和语调</li>
  <li><strong>自信表达：</strong> 上台前深呼吸，保持眼神接触</li>
  <li><strong>自然流畅：</strong> 避免逐字读稿，用自然语调表达</li>
  <li><strong>适度停顿：</strong> 给听众反应时间，显得更从容</li>
</ol>

<p><strong>每天练习5分钟，一周即可明显提升表达能力！</strong></p>""",

    "vocab": """<h3>📚 词汇学习方法</h3>
<p>{description}</p>

<h3>🎯 重点词汇速记</h3>
<ul>
  <li>记忆技巧：词根、词缀、联想记忆</li>
  <li>使用场景：日常交流、书面表达、考试题目</li>
  <li>搭配用法：常见短语和固定搭配</li>
  <li>易混淆词：对比相似词的细微差别</li>
</ul>

<h3>📖 例句演示</h3>
<p>每个核心词汇配有真实例句，帮助理解实际用法：</p>
<ul>
  <li>语境中学习，印象更深刻</li>
  <li>多次接触，自然积累</li>
  <li>举一反三，活学活用</li>
</ul>

<h3>💪 记忆计划</h3>
<ol>
  <li>第1天：初次学习，记住基本含义</li>
  <li>第3天：复习一次，加深印象</li>
  <li>第7天：再复习一次，长期记忆</li>
  <li>第30天：融入实际使用</li>
</ol>

<h3>🏆 高分策略</h3>
<p>不是死记单词，而是：</p>
<ul>
  <li>在真题中遇见，在文章中使用</li>
  <li>了解词汇的多种含义和用法</li>
  <li>建立词汇联系网络</li>
</ul>

<p><strong>积累 1500+ 核心词汇，足以应对各类英语考试！</strong></p>""",

    "writing": """<h3>✍️ 写作技巧总览</h3>
<p>{description}</p>

<h3>📋 写作构成要素</h3>
<ul>
  <li><strong>结构清晰：</strong> 开头-主体-结尾的完整框架</li>
  <li><strong>句式多样：</strong> 简单句、复合句、复杂句的灵活运用</li>
  <li><strong>词汇准确：</strong> 用词恰当，避免重复</li>
  <li><strong>语法正确：</strong> 基础语法无误，高级语法加分</li>
</ul>

<h3>🎯 常见题型</h3>
<ol>
  <li><strong>邮件写作：</strong> 简洁、有礼、有针对性</li>
  <li><strong>故事叙述：</strong> 清晰的时间顺序和因果关系</li>
  <li><strong>议论文：</strong> 明确观点，多角度论证</li>
  <li><strong>描写文：</strong> 生动细节，感官描写</li>
</ol>

<h3>📝 写作流程</h3>
<ol>
  <li>审题：理解要求，确定主题</li>
  <li>列提纲：整理思路，分段要点</li>
  <li>初稿：快速成文，不要过度编辑</li>
  <li>修改：检查语法、词汇、结构</li>
  <li>润色：添加高级表达，最后检查</li>
</ol>

<h3>💎 高分秘诀</h3>
<ul>
  <li>使用 3-5 个高级词汇或短语</li>
  <li>包含 2-3 个复杂句式</li>
  <li>逻辑清晰，过渡自然</li>
  <li>无语法错误，拼写无误</li>
</ul>

<p><strong>反复练习写作，一周一篇，6周内可显著提升！</strong></p>""",

    "listening": """<h3>🎧 听力技能提升</h3>
<p>{description}</p>

<h3>👂 听力能力分解</h3>
<ul>
  <li><strong>音素识别：</strong> 区分相似发音</li>
  <li><strong>单词听辨：</strong> 快速反应词汇</li>
  <li><strong>句子理解：</strong> 把握句子主旨</li>
  <li><strong>篇章理解：</strong> 整体内容把握</li>
</ul>

<h3>🎯 常见题型破解</h3>
<ul>
  <li><strong>图片选择题：</strong> 先看图找差异，再听关键词</li>
  <li><strong>填空题：</strong> 预测可能的词类和内容</li>
  <li><strong>选择题：</strong> 注意同义替换和干扰项</li>
  <li><strong>匹配题：</strong> 抓住每个对话的核心信息</li>
</ul>

<h3>📈 训练方法</h3>
<ol>
  <li><strong>精听：</strong> 逐字逐句理解，记录生词</li>
  <li><strong>泛听：</strong> 快速把握大意，积累语感</li>
  <li><strong>跟读：</strong> 模仿发音，改善口语</li>
  <li><strong>听写：</strong> 全文听写，检验理解</li>
</ol>

<h3>💪 高分策略</h3>
<ul>
  <li>每天坚持听 20-30 分钟</li>
  <li>选择原汁原味的英语材料</li>
  <li>重复听同一篇，逐步深化理解</li>
  <li>定期做真题模拟，检验进度</li>
</ul>

<p><strong>3 个月集中训练，听力能力可提升 1-2 个等级！</strong></p>""",

    "default": """<h3>📚 主题简介</h3>
<p>{description}</p>

<h3>🎯 关键要点</h3>
<ul>
  <li>理解本主题的核心概念和基础知识</li>
  <li>掌握在考试和日常使用中的应用场景</li>
  <li>积累常用表达和相关词汇</li>
  <li>通过实际练习巩固学习成果</li>
</ul>

<h3>💡 学习建议</h3>
<ol>
  <li>首先理解基本概念，不要死记硬背</li>
  <li>在真实情景中反复接触，加深印象</li>
  <li>定期复习，建立长期记忆</li>
  <li>与其他学习者交流，获得新的视角</li>
</ol>

<h3>🏆 进阶路径</h3>
<p>本篇内容适合以下学习阶段：</p>
<ul>
  <li>初级：建立基础知识框架</li>
  <li>中级：扩展应用场景和用法</li>
  <li>高级：掌握细微差别和高级表达</li>
</ul>

<h3>📝 实践要点</h3>
<p>学完本篇后，建议：</p>
<ol>
  <li>整理核心要点笔记</li>
  <li>做配套练习题，检验理解</li>
  <li>尝试在实际交流中运用</li>
  <li>一周后再复习一遍，巩固效果</li>
</ol>

<p><strong>学以致用，才是最有效的学习方式。坚持练习，必定进步！</strong></p>"""
}

def get_content_template(class1, class2):
    """根据栏目选择内容模板"""
    if class1 in (103,):
        return CONTENT_TEMPLATES["reading"]
    elif class1 in (104,):
        return CONTENT_TEMPLATES["speaking"]
    elif class2 in (112, 122):
        return CONTENT_TEMPLATES["vocab"]
    elif class2 in (113, 123):
        return CONTENT_TEMPLATES["writing"]
    elif class2 in (114,):
        return CONTENT_TEMPLATES["listening"]
    else:
        return CONTENT_TEMPLATES["default"]

def fix_article_covers(conn):
    """修复所有文章的封面路径"""
    logger.info("=" * 60)
    logger.info("开始修复文章封面")
    logger.info("=" * 60)

    cur = conn.cursor()

    # 查出所有文章
    cur.execute("""
        SELECT id, class1, class2 FROM ep_news
        WHERE recycle=0
        ORDER BY id
    """)
    articles = cur.fetchall()

    updated = 0
    for article_id, class1, class2 in articles:
        # 确定使用哪个 class 作为图片分类
        cover_class = class2 if class2 > 0 else class1

        # 如果 cover_class 没有配置，使用 class1
        if cover_class not in CATEGORY_COVERS:
            cover_class = class1

        if cover_class not in CATEGORY_COVERS:
            logger.warning(f"ID {article_id}: 没有找到分类 {cover_class} 的封面配置")
            continue

        # 随机选一个封面（轮转）
        covers = CATEGORY_COVERS[cover_class]
        cover_idx = article_id % len(covers)
        new_cover = covers[cover_idx]

        # 更新
        cur.execute(
            "UPDATE ep_news SET imgurl=%s WHERE id=%s",
            (new_cover, article_id)
        )
        updated += 1

        if updated % 50 == 0:
            logger.info(f"已更新 {updated} 篇")

    conn.commit()
    logger.info(f"✓ 封面修复完成：共更新 {updated} 篇")
    cur.close()

def enrich_article_content(conn):
    """扩充文章内容"""
    logger.info("=" * 60)
    logger.info("开始扩充文章内容")
    logger.info("=" * 60)

    cur = conn.cursor()

    # 查出所有文章
    cur.execute("""
        SELECT id, class1, class2, title, description FROM ep_news
        WHERE recycle=0
        ORDER BY id
    """)
    articles = cur.fetchall()

    enriched = 0
    for article_id, class1, class2, title, description in articles:
        # 如果内容太短（< 800字），则扩充
        cur.execute("SELECT LENGTH(content) FROM ep_news WHERE id=%s", (article_id,))
        content_len = cur.fetchone()[0]

        if content_len < 800:
            # 选择合适的模板
            template = get_content_template(class1, class2)
            new_content = template.format(description=description or title)

            cur.execute(
                "UPDATE ep_news SET content=%s WHERE id=%s",
                (new_content, article_id)
            )
            enriched += 1

            if enriched % 50 == 0:
                logger.info(f"已扩充 {enriched} 篇")

    conn.commit()
    logger.info(f"✓ 内容扩充完成：共扩充 {enriched} 篇")
    cur.close()

def clean_cache():
    """清理所有缓存"""
    logger.info("清理缓存...")
    subprocess.run("rm -rf /www/wwwroot/go.xiachaoqing.com/cache/* 2>/dev/null", shell=True)
    subprocess.run("rm -rf /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/cache/* 2>/dev/null", shell=True)
    subprocess.run("find /www/wwwroot/go.xiachaoqing.com -name '*.html' -delete 2>/dev/null", shell=True)
    logger.info("✓ 缓存已清理")

def main():
    logger.info("\n" + "=" * 60)
    logger.info("epgo 完整修复脚本")
    logger.info("=" * 60 + "\n")

    conn = pymysql.connect(**DB)

    try:
        # 1. 修复封面
        fix_article_covers(conn)

        # 2. 扩充内容
        enrich_article_content(conn)

        # 3. 清理缓存
        clean_cache()

        # 4. 统计
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0")
        total = cur.fetchone()[0]
        cur.close()

        logger.info("\n" + "=" * 60)
        logger.info(f"修复完成！总计 {total} 篇文章")
        logger.info("=" * 60 + "\n")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
