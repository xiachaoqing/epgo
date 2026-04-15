import pymysql
from datetime import datetime

DB = dict(host='localhost', user='xiachaoqing', password='Xia@07090218', db='epgo_db', charset='utf8mb4')

TOPICS = {
    103: [
        ('英语阅读技巧：校园生活主题短文精读', '围绕校园生活场景，训练略读、扫读与细节定位能力。'),
        ('英语阅读技巧：科技生活主题短文精读', '聚焦科技生活高频主题，帮助学习者积累阅读策略和核心表达。'),
        ('英语阅读技巧：环保主题文章快速理解', '通过环保主题阅读练习，提升主旨判断与细节提取能力。'),
    ],
    104: [
        ('英语演讲表达：校园话题开场白训练', '聚焦校园演讲话题，整理开场、过渡和收尾表达。'),
        ('英语演讲技巧：如何让表达更有条理', '从结构设计到连接词使用，帮助演讲更清晰自然。'),
        ('英语演讲范文：梦想与成长主题', '提供适合学生练习的演讲范文与表达积累。'),
    ],
    105: [
        ('每日英语 | 今日表达：描述计划与安排', '学习日常中最常用的计划类英语表达。'),
        ('每日英语 | 今日表达：鼓励与赞美怎么说', '积累在学习和生活中常用的鼓励表达。'),
        ('每日英语 | 今日表达：课堂互动常用句', '掌握课堂提问、回答和讨论中的高频句型。'),
    ],
    111: [
        ('KET真题解析：Reading Part 1 题型训练', '拆解KET Reading Part 1常见设问方式与解题步骤。'),
        ('KET真题解析：Writing Part 7 高分思路', '梳理KET写作题的要点覆盖与语言组织方法。'),
    ],
    112: [
        ('KET词汇速记：学校生活高频词', '围绕学校生活场景整理KET高频核心词汇。'),
        ('KET词汇速记：日常交流必背表达', '补充考试和日常都高频出现的词组与短语。'),
    ],
    113: [
        ('KET写作指导：邮件写作开头与结尾', '整理KET邮件写作中稳定可用的开头和结尾模板。'),
        ('KET写作指导：常见失分点专项纠错', '聚焦语法、拼写和逻辑问题，避免低级失分。'),
    ],
    114: [
        ('KET听力技巧：图片题关键词捕捉', '训练KET听力图片题中的关键信息定位能力。'),
        ('KET听力技巧：数字时间题快速判断', '掌握时间、日期、价格等高频信息的听辨方法。'),
    ],
    121: [
        ('PET真题解析：Reading Part 3 长文策略', '拆解PET长文阅读中的定位与排除方法。'),
        ('PET真题解析：Listening Part 2 关键信息训练', '围绕PET听力Part 2常考信息进行专项分析。'),
    ],
    122: [
        ('PET词汇速记：B1校园主题高频词', '梳理B1阶段常见校园主题词汇及短语搭配。'),
        ('PET词汇速记：生活方式主题核心表达', '补充PET考试中常见生活方式和习惯表达。'),
    ],
    123: [
        ('PET写作指导：邮件回复结构模板', '整理PET邮件回复类写作的稳定结构与表达。'),
        ('PET写作指导：议论文常用连接词', '帮助写作时更自然地组织观点和论据。'),
    ],
    124: [
        ('PET阅读技巧：同义替换快速识别', '围绕阅读题中的同义替换进行专项训练。'),
        ('PET阅读技巧：主旨题与细节题区分方法', '帮助学习者更快识别题目要求和答题路径。'),
    ],
}

IMG_MAP = {
    103: '/upload/epgo-covers/reading.png',
    104: '/upload/epgo-covers/speech.png',
    105: '/upload/epgo-covers/daily.png',
    111: '/upload/epgo-covers/ket.png',
    112: '/upload/epgo-covers/ket.png',
    113: '/upload/epgo-covers/ket.png',
    114: '/upload/epgo-covers/ket.png',
    121: '/upload/epgo-covers/pet.png',
    122: '/upload/epgo-covers/pet.png',
    123: '/upload/epgo-covers/pet.png',
    124: '/upload/epgo-covers/pet.png',
}

CONTENT_TMPL = '''<p>{desc}</p>
<h3>学习重点</h3>
<ul>
  <li>明确本篇主题中的高频表达和关键词</li>
  <li>结合题型或场景理解表达的实际使用方式</li>
  <li>完成一轮复盘，整理自己的错题和笔记</li>
</ul>
<h3>练习建议</h3>
<p>建议把本文内容和既有学习资料配套使用，先阅读理解，再做关键词提取，最后尝试复述或写出自己的总结。</p>
<p>每天坚持一篇小专题，长期积累后会明显提升阅读、写作或考试表现。</p>
'''

COLUMN_ORDER = [103,104,105,111,112,113,114,121,122,123,124]

conn = pymysql.connect(**DB)
cur = conn.cursor()

today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
added = 0

for cid in COLUMN_ORDER:
    cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND class1=%s", (cid,))
    count = cur.fetchone()[0]
    idx = count % len(TOPICS[cid])
    title, desc = TOPICS[cid][idx]
    cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND class1=%s AND title=%s", (cid, title))
    exists = cur.fetchone()[0]
    if exists:
        title = f"{title}（{datetime.now().strftime('%m-%d')}更新）"
    content = CONTENT_TMPL.format(desc=desc)
    sql = "INSERT INTO ep_news (title,description,content,class1,class2,class3,no_order,wap_ok,img_ok,imgurl,com_ok,issue,hits,updatetime,addtime,lang,recycle,displaytype,publisher) VALUES (%s,%s,%s,%s,0,0,0,1,1,%s,1,%s,%s,%s,%s,%s,0,1,%s)"
    cur.execute(sql, (title, desc, content, cid, IMG_MAP[cid], 'admin', 0, today, today, 'cn', 'system'))
    added += 1

conn.commit()
print(f'added={added}')
cur.execute("SELECT class1,COUNT(*) FROM ep_news WHERE recycle=0 AND class1 IN (103,104,105,111,112,113,114,121,122,123,124) GROUP BY class1 ORDER BY class1")
for row in cur.fetchall():
    print(row)
conn.close()
