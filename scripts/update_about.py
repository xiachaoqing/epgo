#!/usr/bin/env python3
import os
import re

import pymysql


def load_db_config():
    """Read the deployment's existing MetInfo DB config without storing a secret."""
    path = os.environ.get("EPGO_DB_CONFIG", "config/config_db.php")
    raw = open(path, encoding="utf-8").read()

    def value(name):
        match = re.search(rf"{name}\s*=\s*\"([^\"]*)\"", raw)
        if not match:
            raise RuntimeError(f"Missing database setting: {name}")
        return match.group(1)

    return {
        "host": value("con_db_host"),
        "user": value("con_db_id"),
        "password": value("con_db_pass"),
        "db": value("con_db_name"),
    }

content = """<div>
<h2>关于英语陪跑GO</h2>
<p>英语陪跑GO 是专注于剑桥英语学习（KET / PET / FCE）的在线平台，帮助学生和家长把词汇、阅读、听力、写作与口语练习整理成可执行、可复盘的学习路径。</p>

<h2>我们的使命</h2>
<p>让每一位备考剑桥英语的学生都能获得专业、系统的学习资源，不再为备考资料分散、方法不对路而烦恼。</p>

<h2>我们提供什么</h2>
<ul>
  <li><strong>KET备考（A2 Key）</strong>：高频词汇、阅读、写作和听力方法，配合自编练习逐步复盘</li>
  <li><strong>PET备考（B1 Preliminary）</strong>：阅读策略、写作表达、口语任务和词汇专题</li>
  <li><strong>FCE备考（B2 First）</strong>：面向进阶学习者的阅读、词汇、写作、听力和口语指南</li>
  <li><strong>英语阅读与演讲</strong>：围绕真实学习场景拆解文章结构、证据和表达方式</li>
  <li><strong>学习记录表</strong>：记录练习证据、错误原因和下一步行动，帮助形成稳定复习节奏</li>
  <li><strong>学习指南索引</strong>：集中浏览已完成编辑复核的原创文章和专题</li>
</ul>

<h2>我们的优势</h2>
<ul>
  <li><strong>内容专注</strong>：围绕 KET/PET/FCE 和英语综合能力持续整理</li>
  <li><strong>过程可复盘</strong>：文章不只给结论，还提供证据、错误分类和下一步练习</li>
  <li><strong>边界清晰</strong>：自编示例会注明，不冒充 Cambridge 官方材料，也不承诺考试结果</li>
  <li><strong>持续维护</strong>：根据读者反馈修订文章，并保留作者、更新时间和纠错入口</li>
</ul>

<h2>剑桥英语级别说明</h2>
<table style="width:100%;border-collapse:collapse;font-size:14px;margin:12px 0;">
<tr style="background:#1e3a8a;color:white;">
  <th style="padding:8px 12px;text-align:left;">考试名称</th>
  <th style="padding:8px 12px;text-align:left;">CEFR等级</th>
  <th style="padding:8px 12px;text-align:left;">适合人群</th>
</tr>
<tr style="background:#f8f9fa;"><td style="padding:8px 12px;">KET (A2 Key)</td><td style="padding:8px 12px;">A2</td><td style="padding:8px 12px;">初中生，英语入门认证</td></tr>
<tr><td style="padding:8px 12px;">PET (B1 Preliminary)</td><td style="padding:8px 12px;">B1</td><td style="padding:8px 12px;">高中生，留学申请加分</td></tr>
<tr style="background:#f8f9fa;"><td style="padding:8px 12px;">FCE (B2 First)</td><td style="padding:8px 12px;">B2</td><td style="padding:8px 12px;">大学生，国际化职场</td></tr>
</table>

<h2>联系我们</h2>
<ul>
  <li>微信公众号：搜索 <strong>英语陪跑GO</strong> 关注，获取每日备考推送</li>
  <li>网站留言：通过网站底部留言功能联系我们</li>
</ul>

<p style="margin-top:24px;padding:16px 20px;background:#EFF6FF;border-radius:8px;border-left:4px solid #2563EB;line-height:1.8;">
<strong>备考路上，我们一起陪跑。</strong><br>
无论你是刚开始准备KET，还是已经在冲刺PET / FCE，英语陪跑GO都在这里为你提供支持。
</p>
</div>"""

conn = pymysql.connect(charset="utf8mb4", **load_db_config())
cur = conn.cursor()
cur.execute(
    "UPDATE ep_column SET content=%s, description=%s, keywords=%s WHERE id=107",
    (
        content,
        "英语陪跑GO介绍：提供KET、PET、FCE剑桥英语学习指南、原创练习和学习记录工具。",
        "英语陪跑GO,KET,PET,FCE,英语学习指南,学习记录表",
    ),
)
conn.commit()
print(f"Updated {cur.rowcount} row(s)")
conn.close()
