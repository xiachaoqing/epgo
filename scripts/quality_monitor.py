#!/usr/bin/env python3
"""
quality_monitor.py - 文章质量监测脚本（长期维护）

用途: 每周自动扫描所有文章，检测低质量内容，生成报告
脚本类型: 长期运行（weekly cron）
触发方式: crontab - 每周一早上9点运行

crontab配置:
  0 9 * * 1 python3 /www/wwwroot/go.xiachaoqing.com/scripts/quality_monitor.py

修改历史:
  2026-04-16 v1.0 - 初始版本
"""

import pymysql
import logging
import os
import re
import json
from datetime import datetime, timedelta
from collections import defaultdict

# ========== 配置 ==========
DB = dict(
    host="127.0.0.1",
    port=3306,
    user="xiachaoqing",
    password="Xia@07090218",
    database="epgo_db",
    charset="utf8mb4"
)

SITE_ROOT = "/www/wwwroot/go.xiachaoqing.com"
LOG_DIR = f"{SITE_ROOT}/logs"
REPORT_DIR = f"{SITE_ROOT}/docs/quality_reports"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

LOG_FILE = f"{LOG_DIR}/quality_monitor.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ========== 扫描函数 ==========

def scan_all_articles():
    """扫描所有文章，检测质量问题"""
    conn = pymysql.connect(**DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, content, description, class1, addtime, issue
        FROM ep_news
        WHERE recycle=0
        ORDER BY addtime DESC
    """)

    articles = []
    for row in cur.fetchall():
        articles.append({
            'id': row[0],
            'title': row[1],
            'content': row[2],
            'description': row[3],
            'class1': row[4],
            'addtime': row[5],
            'issue': row[6],
        })

    cur.close()
    conn.close()
    return articles

def check_article_quality(article):
    """检查单篇文章的质量问题"""
    issues = []
    title = article['title']
    content = article['content']
    desc = article['description']

    # 1. 长度检查
    content_len = len(content)
    if content_len < 2000:
        issues.append({'type': 'length', 'severity': 'critical', 'msg': f'内容过短: {content_len}字节'})

    # 2. 模板检查
    if re.search(r'学习重点.*理解.*主题中的核心表达|关键要点.*理解本主题的核心概念|本篇重点', content):
        issues.append({'type': 'template', 'severity': 'critical', 'msg': '检测到模板化内容'})

    # 3. 描述检查
    if desc == title:
        issues.append({'type': 'description', 'severity': 'high', 'msg': '摘要等于标题'})
    if len(desc) < 30:
        issues.append({'type': 'description', 'severity': 'high', 'msg': f'摘要过短: {len(desc)}字'})

    # 4. 结构检查
    h2_count = len(re.findall(r'<h2>', content))
    if h2_count < 3:
        issues.append({'type': 'structure', 'severity': 'medium', 'msg': f'h2标题过少: {h2_count}个'})

    # 5. 重复内容检查（和其他文章比较）
    content_hash = hashlib.md5(content[:500].encode()).hexdigest()

    # 6. Markdown检查
    if re.search(r'^(#{1,6} |[\*\-] |\d+\. )', content, re.MULTILINE):
        issues.append({'type': 'format', 'severity': 'high', 'msg': 'Markdown格式混用'})

    return issues

def scan_duplicates():
    """扫描重复内容"""
    conn = pymysql.connect(**DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT LEFT(content,300) as c300, COUNT(*) as cnt, GROUP_CONCAT(id) as ids
        FROM ep_news
        WHERE recycle=0
        GROUP BY LEFT(content,300)
        HAVING cnt>1
    """)

    duplicates = []
    for row in cur.fetchall():
        duplicates.append({
            'count': row[1],
            'ids': row[2].split(','),
            'preview': row[0][:100] + '...' if row[0] else ''
        })

    cur.close()
    conn.close()
    return duplicates

# ========== 报告生成 ==========

def generate_report(articles, duplicates):
    """生成质量报告"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    report_file = f"{REPORT_DIR}/quality_report_{report_date}.md"

    # 统计各类问题
    stats = defaultdict(int)
    severity_stats = defaultdict(int)
    issue_by_severity = defaultdict(list)

    for article in articles:
        issues = check_article_quality(article)
        for issue in issues:
            stats[issue['type']] += 1
            severity_stats[issue['severity']] += 1
            issue_by_severity[issue['severity']].append({
                'id': article['id'],
                'title': article['title'],
                'issue': issue['msg']
            })

    # 生成Markdown报告
    report = f"""# 文章质量监测报告

**生成日期**: {report_date}
**总文章数**: {len(articles)}
**有问题的文章**: {len([a for a in articles if check_article_quality(a)])}

## 问题统计

| 问题类型 | 数量 |
|--------|------|
"""

    for issue_type, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        report += f"| {issue_type} | {count} |\n"

    report += f"\n## 严重性分布\n\n"
    for severity in ['critical', 'high', 'medium']:
        count = severity_stats.get(severity, 0)
        icon = '🔴' if severity == 'critical' else '🟡' if severity == 'high' else '🟢'
        report += f"- {icon} {severity.upper()}: {count}\n"

    # 重复内容详情
    report += f"\n## 重复内容检测\n\n"
    report += f"**重复组总数**: {len(duplicates)}\n\n"
    for dup in duplicates[:10]:  # 只显示前10个
        report += f"- {dup['count']}篇重复: IDs={','.join(map(str,dup['ids'])[:3])}...\n"

    # 严重问题详情
    report += f"\n## 严重问题详情\n\n"
    for severity in ['critical', 'high']:
        issues = issue_by_severity.get(severity, [])
        if issues:
            report += f"\n### {severity.upper()} ({len(issues)}个)\n\n"
            for issue in issues[:20]:  # 只显示前20个
                report += f"- ID {issue['id']}: {issue['title'][:50]} - {issue['issue']}\n"

    # 建议
    report += f"\n## 建议\n\n"
    if stats.get('length', 0) > 20:
        report += "- ⚠️ 有超过20篇文章内容过短，需要扩展\n"
    if stats.get('template', 0) > 10:
        report += "- 🔴 有超过10篇文章使用模板，需要重写\n"
    if len(duplicates) > 5:
        report += "- 🔴 有过多重复内容，严重影响SEO\n"

    # 写入文件
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    log.info(f"报告已生成: {report_file}")
    return report_file

# ========== 主流程 ==========

def main():
    log.info("="*60)
    log.info("文章质量监测启动")
    log.info("="*60)

    # 扫描所有文章
    log.info("扫描所有文章...")
    articles = scan_all_articles()
    log.info(f"共 {len(articles)} 篇文章")

    # 检查重复
    log.info("检测重复内容...")
    duplicates = scan_duplicates()
    log.info(f"找到 {len(duplicates)} 个重复组")

    # 生成报告
    log.info("生成质量报告...")
    report_file = generate_report(articles, duplicates)

    # 统计严重问题
    critical_count = 0
    for article in articles:
        issues = check_article_quality(article)
        for issue in issues:
            if issue['severity'] == 'critical':
                critical_count += 1

    log.info(f"检测完成。严重问题: {critical_count}")

    if critical_count > 50:
        log.warning(f"⚠️ 严重问题过多({critical_count})，建议执行改写脚本")
    elif critical_count > 10:
        log.warning(f"⚠️ 存在{critical_count}个严重问题，需要关注")
    else:
        log.info("✓ 质量良好")

if __name__ == "__main__":
    main()
