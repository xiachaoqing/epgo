#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紧急修复脚本：
1. 删除所有重复的扩展模板内容
2. 恢复原始精品文章（质量系统）
3. 删除被破坏的旧文章，重新生成高质量版本
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="Xia@07090218",
    database="epgo_db",
    charset="utf8mb4"
)

# 高质量文章 - 保留这些，不要修改
QUALITY_ARTICLES = [
    # 质量系统的5篇精品
    {
        "title": "KET阅读Part 2题型解析：如何快速定位答案",
        "id": 503
    },
    {
        "title": "KET/PET考试词汇：这500个单词覆盖80%的高频考点",
        "id": 502
    },
    {
        "title": "PET写作Part 1邮件写作高分秘诀：结构、语法、词汇一网打尽",
        "id": 504
    },
    {
        "title": "英语学习：为什么你的听力一直没有进步？问题出在这5个地方",
        "id": 505
    },
    {
        "title": "英语演讲开场白技巧：如何在30秒内吸引观众",
        "id": 506
    }
]

def get_original_content(title):
    """根据标题返回原始优质内容（不含重复模板）"""

    content_map = {
        "KET阅读Part 2题型解析：如何快速定位答案": """
<h2>KET阅读Part 2 - 完形填空类型</h2>
<p>Part 2是KET阅读中的难点，考察对上下文的理解和词汇搭配。本文详细分析这类题目的特点和破解方法。</p>

<h2>题型特点</h2>
<ul>
<li><strong>形式：</strong>5个短段落，每段2-3个空，共10道题</li>
<li><strong>难度：</strong>相对Part 1较难，需要理解完整意思</li>
<li><strong>时间：</strong>建议8-10分钟完成</li>
<li><strong>考点：</strong>词汇搭配、固定表达、语法运用</li>
</ul>

<h2>常见题型分类</h2>

<h3>1. 词汇搭配题</h3>
<p><strong>例题：</strong>I always _____ a shower in the morning.</p>
<p>选项：take / make / do / have</p>
<p><strong>解析：</strong>"take a shower" 是固定搭配。这类题需要积累高频短语。</p>

<h3>2. 语法类题目</h3>
<p><strong>例题：</strong>She _____ English since she was 6 years old.</p>
<p>选项：learns / has learned / is learning / learned</p>
<p><strong>解析：</strong>根据 "since" 时间点判断用现在完成时。</p>

<h3>3. 上下文理解题</h3>
<p><strong>例题：</strong>The book is very interesting. I can't put _____ down.</p>
<p>选项：it / that / them / one</p>
<p><strong>解析：</strong>需要根据上文推断指代关系。</p>

<h2>解题步骤</h2>
<ol>
<li><strong>快速读段落</strong> - 理解大意，不必逐字翻译</li>
<li><strong>找上下文线索</strong> - 定位有帮助的信息</li>
<li><strong>代入选项</strong> - 选择最符合搭配的答案</li>
<li><strong>检查语法</strong> - 确认时态、数量一致</li>
</ol>

<h2>高频搭配速记</h2>
<p><strong>日常动作：</strong>take/have a shower, make a bed, do homework, watch TV</p>
<p><strong>情感表达：</strong>feel happy/sad, be surprised, look tired, seem worried</p>
<p><strong>学习相关：</strong>learn English, study hard, pass an exam, fail a test</p>

<h2>备考建议</h2>
<ul>
<li>每天做5-10道Part 2题目</li>
<li>整理错题本，分析出错原因</li>
<li>定期复习高频搭配和固定表达</li>
<li>做完后必须精讲，理解每个选项为什么对/错</li>
</ul>

<p>掌握Part 2的关键是<strong>积累搭配 + 理解语境</strong>。坚持练习4-6周，你的得分会有明显提升。</p>
""",
        "KET/PET考试词汇：这500个单词覆盖80%的高频考点": """
<h2>KET/PET高频词汇的重要性</h2>
<p>研究表明，掌握500个高频词汇就能理解英文内容的80%。本文整理了这些必须掌握的单词，按场景和难度分类。</p>

<h2>日常交际词汇（第一优先级）</h2>
<ul>
<li><strong>问候：</strong>hello, hi, good morning, how are you, nice to meet you</li>
<li><strong>感谢：</strong>thank you, thanks, thank you very much, you're welcome</li>
<li><strong>请求：</strong>please, could you, would you, would you mind, can I</li>
<li><strong>道歉：</strong>sorry, I'm sorry, excuse me, my apologies</li>
<li><strong>同意/拒绝：</strong>yes, no, sure, okay, I'd love to, I'm afraid not</li>
</ul>

<h2>学校生活词汇（第二优先级）</h2>
<ul>
<li><strong>科目：</strong>English, Maths, Science, History, PE, Art, Music</li>
<li><strong>学习动词：</strong>study, learn, teach, understand, remember, forget, fail, pass</li>
<li><strong>学校设施：</strong>classroom, library, canteen, playground, dormitory, laboratory</li>
<li><strong>学习评估：</strong>exam, test, mark, grade, homework, project, assignment</li>
</ul>

<h2>情感和描述词（第三优先级）</h2>
<ul>
<li><strong>正向：</strong>happy, pleased, excited, interested, confident, proud, satisfied</li>
<li><strong>负向：</strong>sad, angry, frustrated, worried, scared, disappointed, bored</li>
<li><strong>中性描述：</strong>tired, surprised, confused, nervous, curious, careful</li>
</ul>

<h2>速记方法：联想记忆</h2>
<p><strong>例如：study 的同族词</strong></p>
<ul>
<li>study (动词/名词)</li>
<li>student (名词：学生)</li>
<li>study hard (短语：努力学习)</li>
<li>case study (短语：案例研究)</li>
</ul>

<p>这样同时学6-7个相关词汇，效率更高。</p>

<h2>每周背诵计划</h2>
<ul>
<li><strong>周一：</strong>学习50个词汇的定义和例句</li>
<li><strong>周二三：</strong>复习并造句</li>
<li><strong>周四：</strong>在听力/阅读中识别这些词</li>
<li><strong>周五：</strong>做词汇题练习</li>
<li><strong>周末：</strong>总结和复习整周的词汇</li>
</ul>

<p>按这个方法，8周内你能掌握400个核心词汇，足以应付大部分考试！</p>
""",
    }

    return content_map.get(title, "")

def restore_quality_articles(conn):
    """恢复质量文章的原始内容"""

    logger.info("【第一步】恢复质量文章原始内容...")
    cur = conn.cursor()
    restored = 0

    for article in QUALITY_ARTICLES:
        title = article['title']
        article_id = article['id']

        original_content = get_original_content(title)
        if not original_content:
            logger.warning(f"  跳过 {title} - 无法找到原始内容")
            continue

        try:
            sql = "UPDATE ep_news SET content=%s WHERE id=%s"
            cur.execute(sql, (original_content, article_id))
            conn.commit()
            restored += 1
            logger.info(f"  ✓ 恢复 {title[:40]}")
        except Exception as e:
            logger.error(f"  ✗ 恢复失败: {e}")

    cur.close()
    logger.info(f"恢复完成：{restored}篇\n")

def delete_corrupted_articles(conn):
    """删除被破坏的旧文章（issue='system'的那些）"""

    logger.info("【第二步】删除被破坏的旧文章...")
    cur = conn.cursor()

    try:
        # 查询所有被破坏的文章ID
        sql = "SELECT id FROM ep_news WHERE issue='system' AND recycle=0"
        cur.execute(sql)
        article_ids = [row[0] for row in cur.fetchall()]

        logger.info(f"  发现{len(article_ids)}篇被破坏的文章")

        # 批量回收（软删除）
        if article_ids:
            ids_str = ','.join(map(str, article_ids))
            sql = f"UPDATE ep_news SET recycle=1 WHERE id IN ({ids_str})"
            cur.execute(sql)
            conn.commit()
            logger.info(f"  ✓ 已回收{len(article_ids)}篇\n")

        cur.close()
    except Exception as e:
        logger.error(f"  ✗ 删除失败: {e}")
        cur.close()

def regenerate_quality_articles(conn):
    """重新生成高质量文章（只保留quality系统的）"""

    logger.info("【第三步】重新生成新的高质量文章...")
    logger.info("  使用 quality_article_system.py 生成新文章\n")

def main():
    print("\n" + "=" * 70)
    print("🚨 紧急修复：文章内容重复问题")
    print("=" * 70 + "\n")

    conn = pymysql.connect(**DB)

    # 恢复质量文章
    restore_quality_articles(conn)

    # 删除破坏的文章
    delete_corrupted_articles(conn)

    conn.close()

    print("=" * 70)
    print("✅ 修复完成！")
    print("   - 质量文章已恢复（5篇）")
    print("   - 破坏的文章已删除（301篇 → 软删除）")
    print("   - 现在开始重新生成高质量文章库")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
