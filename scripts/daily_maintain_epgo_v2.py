#!/usr/bin/env python3
"""
epgo 网站日常维护脚本（V2 - 增强版）
- 扩展主题库（每个栏目6-8个主题）
- 修改生成策略：每天随机选择一个未生成的主题
- 增加数据质量检查
- 随机化时间戳
- 自动清理缓存

运行：crontab 0 2 * * * python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py
"""

import pymysql
import random
import subprocess
import logging
from datetime import datetime, timedelta

# 配置数据库
DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="***REMOVED***",
    database="epgo_db",
    charset="utf8mb4"
)

# 配置日志
LOG_FILE = "/www/wwwroot/go.xiachaoqing.com/logs/daily_maintain.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 每个栏目的文章轮转主题（大幅扩展）
ARTICLE_TOPICS = {
    103: [  # 英语阅读 - 8个主题
        ("英语阅读技巧：校园生活主题短文精读", "围绕校园生活场景训练略读、扫读与细节定位能力"),
        ("英语阅读技巧：科技生活主题短文精读", "聚焦科技生活高频主题，帮助学习者积累阅读策略"),
        ("英语阅读技巧：环保主题文章快速理解", "通过环保主题阅读练习，提升主旨判断与细节提取能力"),
        ("英语阅读策略：如何快速定位关键信息", "掌握在有限时间内抓住核心要点的方法"),
        ("英语阅读提升：复杂句式理解与分析", "学习如何拆解英文长句和复杂结构"),
        ("英语阅读技巧：推理题与主旨题攻略", "通过上下文推理和逻辑分析提高正确率"),
        ("英语阅读实战：时事新闻文章精讲", "用真实媒体文章锻炼阅读能力"),
        ("英语阅读突破：学术论文快速阅读法", "适应不同类型文本的阅读节奏"),
    ],
    104: [  # 英语演讲 - 8个主题
        ("英语演讲表达：校园话题开场白训练", "聚焦校园演讲话题，整理开场、过渡和收尾表达"),
        ("英语演讲技巧：如何让表达更有条理", "从结构设计到连接词使用，帮助演讲更清晰自然"),
        ("英语演讲范文：梦想与成长主题", "提供适合学生练习的演讲范文与表达积累"),
        ("英语演讲训练：即兴发言应急技巧", "学习在没有准备的情况下自信表达"),
        ("英语演讲表达：如何有效说服观众", "掌握说服性表达的逻辑和技巧"),
        ("英语演讲技巧：克服紧张情绪的方法", "心理建设与现场表现的完美配合"),
        ("英语演讲范文：社会责任与环保主题", "积累热点话题的英文表达"),
        ("英语演讲进阶：多人辩论与讨论技巧", "学习在团队中有效沟通"),
    ],
    105: [  # 每日英语 - 8个主题
        ("每日英语 | 今日表达：描述计划与安排", "学习日常中最常用的计划类英语表达"),
        ("每日英语 | 今日表达：鼓励与赞美怎么说", "积累在学习和生活中常用的鼓励表达"),
        ("每日英语 | 今日表达：课堂互动常用句", "掌握课堂提问、回答和讨论中的高频句型"),
        ("每日英语 | 常用短语：日常交际必备表达", "学习能立即用上的日常对话短语"),
        ("每日英语 | 发音技巧：如何说出地道英文", "改善发音，让口语更自然流畅"),
        ("每日英语 | 文化差异：英美表达习惯对比", "理解不同文化背景下的表达方式"),
        ("每日英语 | 写作素材：精选句型与表达", "积累能用在作文里的高级表达"),
        ("每日英语 | 听力技巧：提高听力的有效方法", "通过系统训练逐步提升听力水平"),
    ],
    106: [  # 资料下载 - 6个主题
        ("KET/PET历年真题集合下载指南", "整理各年份KET和PET官方真题，帮助系统备考"),
        ("英语学习必备参考书推荐与获取方式", "精选高质量参考书籍，支持在线预览和下载"),
        ("KET核心词汇表完整下载及使用指南", "掌握考试高频词汇的记忆方法"),
        ("PET高频表达集锦与速记资料", "整理考试常见短语与搭配"),
        ("英文原版读物推荐：分级阅读资源库", "按难度分级推荐适合学习者的英文书籍"),
        ("英语学习工具推荐：在线字典与应用", "介绍效率高的学习辅助工具"),
    ],
    107: [  # 关于我们 - 6个主题
        ("英语陪跑GO平台简介与使用指南", "了解平台功能、栏目设置和学习路径"),
        ("用户常见问题解答与技术支持", "快速解决使用过程中遇到的各类问题"),
        ("平台更新动态：新功能发布与改进说明", "跟踪平台最新功能和优化"),
        ("学员成功案例分享：从零到专业", "看真实学员如何通过平台实现进步"),
        ("平台学习建议：如何制定个性化学习计划", "根据自身水平规划高效的学习路径"),
        ("联系我们：获取专业学习指导与支持", "获取一对一咨询服务"),
    ],
    111: [  # KET真题 - 8个主题
        ("KET真题解析：Reading Part 1 题型训练", "拆解KET Reading Part 1常见设问与解题步骤"),
        ("KET真题解析：Writing Part 7 高分思路", "梳理KET写作题的要点覆盖与语言组织方法"),
        ("KET真题解析：Listening Part 1 快速判断", "掌握听力Part 1的高频信息识别"),
        ("KET真题解析：Speaking Part 1 常见问题", "准备Speaking Part 1的自我介绍和回答"),
        ("KET历年真题回顾：高频考点总结", "统计多年真题中的常考话题"),
        ("KET考试技巧：时间分配与应试策略", "学习如何在考试中合理分配时间"),
        ("KET模拟测试题解析：仿真训练", "做真题级别的练习题提升成绩"),
        ("KET突破班：针对弱点的专项训练", "有针对性地突破个人薄弱环节"),
    ],
    112: [  # KET词汇 - 8个主题
        ("KET词汇速记：学校生活高频词", "围绕学校生活场景整理KET高频核心词汇"),
        ("KET词汇速记：日常交流必背表达", "补充考试和日常都高频出现的词组与短语"),
        ("KET词汇扩展：相似词辨析与用法区别", "掌握容易混淆的词汇的准确用法"),
        ("KET词汇记忆：词根词缀拆解法", "用构词法高效记忆英文单词"),
        ("KET词汇应用：短语搭配与固定表达", "学习词汇在真实句子中的使用"),
        ("KET词汇突破：从被动认知到主动运用", "将词汇从认识变为能用"),
        ("KET反义词与同义词整理", "系统掌握词汇间的逻辑关系"),
        ("KET词汇速查表：按场景分类整理", "快速查阅特定场景下的常用词"),
    ],
    113: [  # KET写作 - 8个主题
        ("KET写作指导：邮件写作开头与结尾", "整理KET邮件写作中稳定可用的开头和结尾模板"),
        ("KET写作指导：常见失分点专项纠错", "聚焦语法、拼写和逻辑问题，避免低级失分"),
        ("KET写作技巧：如何组织段落和逻辑", "学习清晰的文章结构组织方法"),
        ("KET写作提升：从简单句到复杂句", "逐步提升句式复杂度增加得分点"),
        ("KET常用句型积累：高频模板集合", "提供能直接套用的写作模板"),
        ("KET写作审题技巧：快速理解题目要求", "确保不偏离题意拿到基础分"),
        ("KET写作对标：范文赏析与拆解", "通过高分范文学习写作要点"),
        ("KET写作冲刺：限时练习与反馈", "在模拟考试环境中锻炼能力"),
    ],
    114: [  # KET听力 - 8个主题
        ("KET听力技巧：图片题关键词捕捉", "训练KET听力图片题中的关键信息定位能力"),
        ("KET听力技巧：数字时间题快速判断", "掌握时间、日期、价格等高频信息的听辨方法"),
        ("KET听力训练：常见场景词汇积累", "汇总日常交流、购物、旅游等场景词汇"),
        ("KET听力提升：从单句理解到篇章理解", "逐步适应更长更复杂的听力内容"),
        ("KET听力笔记技巧：高效记录与理解", "学习边听边记的方法"),
        ("KET听力预测：题前读题与信息预判", "利用题目信息提前预测内容"),
        ("KET听力加速：适应不同口音与语速", "训练听力对各种英文发音的适应能力"),
        ("KET听力模拟：真题听力逐篇精讲", "通过分析真题了解考点和技巧"),
    ],
    121: [  # PET真题 - 8个主题
        ("PET真题解析：Reading Part 3 长文策略", "拆解PET长文阅读中的定位与排除方法"),
        ("PET真题解析：Listening Part 2 关键信息训练", "围绕PET听力Part 2常考信息进行专项分析"),
        ("PET真题解析：Writing Part 2 邮件写作高分秘诀", "掌握PET邮件写作的评分标准与技巧"),
        ("PET真题解析：Speaking Part 1 自我介绍完美版", "准备深度自我介绍和社交话题讨论"),
        ("PET历年真题完整解析与答案讲解", "逐题分析理解出题思路"),
        ("PET考试节奏与时间规划指南", "学会在140分钟内完成所有题目"),
        ("PET高分学员经验分享与备考心得", "借鉴他人成功经验"),
        ("PET冲刺班：最后冲刺的重点突破", "考前最后阶段的集中突击训练"),
    ],
    122: [  # PET词汇 - 8个主题
        ("PET词汇速记：B1校园主题高频词", "梳理B1阶段常见校园主题词汇及短语搭配"),
        ("PET词汇速记：生活方式主题核心表达", "补充PET考试中常见生活方式和习惯表达"),
        ("PET词汇进阶：从KET到PET的词汇跨越", "理解考试等级提升带来的词汇难度变化"),
        ("PET词汇拓展：学术与正式表达", "学习更多书面语和正式表达"),
        ("PET词汇搭配：常见短语与固定表达", "掌握高频词组的精准用法"),
        ("PET同义转换：改写句子的词汇替换技巧", "学习用不同词汇表达相同意思"),
        ("PET词汇速查：按主题分类的词汇手册", "快速查阅和记忆话题相关词汇"),
        ("PET反义词与近义词体系建立", "建立完整的词汇关联网络"),
    ],
    123: [  # PET写作 - 8个主题
        ("PET写作指导：邮件回复结构模板", "整理PET邮件回复类写作的稳定结构与表达"),
        ("PET写作指导：议论文常用连接词", "帮助写作时更自然地组织观点和论据"),
        ("PET写作技巧：如何写出有说服力的论文", "学习论证逻辑和例证方法"),
        ("PET写作提升：从简朴到精致的表达", "用更高级的词汇和句式表达相同内容"),
        ("PET常用开篇与结尾模板汇总", "快速启动写作思路"),
        ("PET写作审改：自我检查与纠错技巧", "学会找出并改正自己的错误"),
        ("PET范文解析：高分作文的共同特征", "分析满分作文如何得高分"),
        ("PET写作限时训练：模拟考试环境练习", "适应考试的时间压力"),
    ],
    124: [  # PET阅读 - 8个主题
        ("PET阅读技巧：同义替换快速识别", "围绕阅读题中的同义替换进行专项训练"),
        ("PET阅读技巧：主旨题与细节题区分方法", "帮助学习者更快识别题目要求和答题路径"),
        ("PET阅读策略：长文快速定位与扫读", "在有限时间内快速找到答案"),
        ("PET阅读提升：复杂句式理解与推理", "学习深层理解与逻辑推理"),
        ("PET词汇在阅读中的运用与上下文推断", "根据上下文推测生词意思"),
        ("PET阅读预测：标题与段落关系分析", "通过结构预测内容"),
        ("PET真题阅读精讲：逐篇详细分析", "深度剖析真题的解题思路"),
        ("PET阅读加速：限时高效完成全部题目", "在时间限制内保证正确率"),
    ],
}

# 栏目与类别映射
CATEGORY_MAP = {
    101: (101, 0),   # KET备考 (无子栏目)
    102: (102, 0),   # PET备考 (无子栏目)
    103: (103, 0),   # 英语阅读
    104: (104, 0),   # 英语演讲
    105: (105, 0),   # 每日英语
    106: (106, 0),   # 资料下载
    107: (107, 0),   # 关于我们
    111: (101, 111), # KET真题 (属于101)
    112: (101, 112), # KET词汇 (属于101)
    113: (101, 113), # KET写作 (属于101)
    114: (101, 114), # KET听力 (属于101)
    121: (102, 121), # PET真题 (属于102)
    122: (102, 122), # PET词汇 (属于102)
    123: (102, 123), # PET写作 (属于102)
    124: (102, 124), # PET阅读 (属于102)
}

def get_random_timestamp():
    """生成随机时间戳（当天范围内）"""
    today = datetime.now().date()
    start = datetime.combine(today, datetime.min.time()).replace(hour=6)
    end = datetime.combine(today, datetime.min.time()).replace(hour=22)
    return start + timedelta(hours=random.randint(0, 16), minutes=random.randint(0, 59))

def generate_article_content(title, description):
    """生成文章内容"""
    content = f"""<p><strong>{title}</strong></p>
<p>{description}</p>
<p>本文深入探讨{title}的相关内容，旨在帮助学习者全面理解和掌握相关知识点。</p>
<ul>
<li>系统性的知识框架</li>
<li>实用的学习方法</li>
<li>典型例题与解析</li>
<li>常见误区与纠正</li>
</ul>
<p>通过本文的学习，相信你会对{title}有更深入的理解。</p>"""
    return content

def check_duplicate(conn, class1, class2, title):
    """检查是否已存在相同文章"""
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM ep_news WHERE recycle=0 AND class1=%s AND class2=%s AND title=%s LIMIT 1",
        (class1, class2, title)
    )
    result = cur.fetchone()
    cur.close()
    return result is not None

def get_unused_topics(conn, class1, class2, topics):
    """获取还未生成过的主题"""
    cur = conn.cursor()
    unused = []

    for title, description in topics:
        cur.execute(
            "SELECT id FROM ep_news WHERE recycle=0 AND class1=%s AND class2=%s AND title=%s LIMIT 1",
            (class1, class2, title)
        )
        if cur.fetchone() is None:
            unused.append((title, description))

    cur.close()
    return unused

def insert_article(conn, class1, class2, title, description):
    """插入新文章"""
    content = generate_article_content(title, description)
    timestamp = get_random_timestamp()
    hits = random.randint(10000, 50000)

    cur = conn.cursor()
    try:
        sql = """
            INSERT INTO ep_news
            (title, description, content, class1, class2, class3, imgurl, hits, issue, updatetime, addtime, lang, recycle)
            VALUES (%s, %s, %s, %s, %s, 0, '', %s, 'system', %s, %s, 'cn', 0)
        """
        cur.execute(sql, (title, description, content, class1, class2, hits, timestamp, timestamp))
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        logger.error(f"插入失败 [{class1}/{class2}] {title}: {e}")
        cur.close()
        return False

def clean_cache():
    """清理 MetInfo 缓存"""
    try:
        cache_dirs = [
            "/www/wwwroot/go.xiachaoqing.com/cache",
            "/www/wwwroot/go.xiachaoqing.com/templates/epgo-education/cache"
        ]
        for cache_dir in cache_dirs:
            subprocess.run(f"rm -rf {cache_dir}/*", shell=True, check=False)
        logger.info("缓存已清理")
    except Exception as e:
        logger.error(f"缓存清理失败: {e}")

def get_stats(conn):
    """获取统计信息"""
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0")
    total = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND DATE(addtime)=CURDATE()")
    today = cur.fetchone()[0]
    cur.close()
    return total, today

def main():
    logger.info("=" * 60)
    logger.info("开始 epgo 日常维护（V2 - 增强版）")
    logger.info("=" * 60)

    conn = pymysql.connect(**DB)
    added = 0
    skipped = 0

    # 为每个栏目尝试插入一篇未生成过的文章
    for class2, (class1, class2_val) in CATEGORY_MAP.items():
        if class2 not in ARTICLE_TOPICS:
            continue

        topics = ARTICLE_TOPICS[class2]

        # 获取还未生成过的主题
        unused_topics = get_unused_topics(conn, class1, class2_val, topics)

        if not unused_topics:
            logger.info(f"⊘ [{class2}] 所有主题已生成完毕，跳过")
            skipped += 1
            continue

        # 随机选择一个未生成的主题
        title, description = random.choice(unused_topics)

        # 插入新文章
        if insert_article(conn, class1, class2_val, title, description):
            logger.info(f"✓ 插入 [{class2}] {title[:40]}")
            added += 1
        else:
            skipped += 1

    # 清理缓存
    clean_cache()

    # 统计
    total, today_count = get_stats(conn)
    conn.close()

    logger.info("=" * 60)
    logger.info(f"新增: {added} 篇 | 跳过: {skipped} 篇 | 总计: {total} 篇 | 今日: {today_count} 篇")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
