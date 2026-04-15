#!/usr/bin/env python3
import pymysql

content = """<div>
<h2>关于英语陪跑GO</h2>
<p>英语陪跑GO 是专注于剑桥英语备考（KET / PET / FCE）的在线学习平台，致力于帮助中国学生系统、高效地备考剑桥系列英语考试，取得理想成绩。</p>

<h2>我们的使命</h2>
<p>让每一位备考剑桥英语的学生都能获得专业、系统的学习资源，不再为备考资料分散、方法不对路而烦恼。</p>

<h2>我们提供什么</h2>
<ul>
  <li><strong>KET备考（A2 Key）</strong>：真题解析、高频词汇、写作模板、听力技巧，系统覆盖全部考点</li>
  <li><strong>PET备考（B1 Preliminary）</strong>：阅读策略、写作范文、口语话题、词汇专题，全面备战</li>
  <li><strong>FCE备考（B2 First）</strong>：进阶英语学习，冲击B2水平</li>
  <li><strong>英语阅读</strong>：精选英文原文材料，配合考点讲解，提升阅读理解能力</li>
  <li><strong>每日英语</strong>：每日推送备考词汇、例句、语法小知识，坚持打卡积累</li>
  <li><strong>资料下载</strong>：历年真题、官方样题、备考笔记等学习资料免费下载</li>
</ul>

<h2>我们的优势</h2>
<ul>
  <li><strong>内容专注</strong>：只做剑桥英语备考，专注KET/PET/FCE，不泛不散</li>
  <li><strong>体系完整</strong>：从词汇到语法到题型到模拟，覆盖备考全阶段</li>
  <li><strong>持续更新</strong>：每日更新学习内容，紧跟考试动态</li>
  <li><strong>社群陪跑</strong>：微信公众号每日推送，学习不孤单</li>
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

conn = pymysql.connect(host='localhost', user='xiachaoqing', password='Xia@07090218', db='epgo_db', charset='utf8mb4')
cur = conn.cursor()
cur.execute("UPDATE ep_column SET content=%s WHERE id=107", (content,))
conn.commit()
print(f"Updated {cur.rowcount} row(s)")
conn.close()
