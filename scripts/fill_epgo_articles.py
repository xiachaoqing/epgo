import pymysql, random
from datetime import datetime, timedelta

conn = pymysql.connect(host='localhost', user='xiachaoqing', password='***REMOVED***', db='epgo_db', charset='utf8mb4')
cur = conn.cursor()
cur.execute("SELECT id,class1,title,description,content FROM ep_news WHERE recycle=0 ORDER BY id DESC")
rows = cur.fetchall()
by_class = {}
for r in rows:
    by_class.setdefault(r[1], []).append(r)
cur.execute("SELECT class1,COUNT(*) FROM ep_news WHERE recycle=0 AND class1 IN (103,104,105,111,112,113,114,121,122,123,124) GROUP BY class1")
counts = dict(cur.fetchall())
target = 12
plan = {cid: max(0, target - counts.get(cid, 0)) for cid in [103,104,105,111,112,113,114,121,122,123,124]}
plan[105] = max(0, 16 - counts.get(105, 0))
inserted = 0
sql = "INSERT INTO ep_news (title,description,content,class1,class2,class3,no_order,wap_ok,img_ok,imgurl,com_ok,issue,hits,updatetime,addtime,lang,recycle,displaytype,publisher) VALUES (%s,%s,%s,%s,0,0,0,1,1,%s,1,%s,%s,%s,%s,%s,0,1,%s)"
for class1, need in plan.items():
    if need <= 0:
        continue
    samples = by_class.get(class1, [])[:5]
    if not samples:
        continue
    for i in range(need):
        s = samples[i % len(samples)]
        title = s[2]
        for a, b in [('2026年5月', '2026年6月'), ('2026年4月', '2026年6月'), ('进阶版1', '专题版1'), ('进阶版2', '专题版2'), ('进阶版3', '专题版3')]:
            title = title.replace(a, b)
        title = title.replace('5个', '6个').replace('7个', '8个').replace('3个', '4个').replace('100个', '60个')
        if '（' not in title:
            title += f'（专题版{i+1}）'
        desc = s[3] or '围绕英语学习与剑桥考试场景，提供更系统的练习方法、表达积累和题型拆解。'
        if len(desc) < 30:
            desc = '围绕英语学习与剑桥考试场景，提供更系统的练习方法、表达积累和题型拆解。'
        content = (s[4] or '') + '<p>延伸训练：建议把本文中的核心表达整理进自己的错题本或词汇本，并在24小时内完成一次复盘。</p>'
        dt = (datetime.now() - timedelta(days=random.randint(0, 25), hours=random.randint(0, 23))).strftime('%Y-%m-%d %H:%M:%S')
        img = '/upload/epgo-covers/reading.png'
        if class1 == 104:
            img = '/upload/epgo-covers/speech.png'
        elif class1 == 105:
            img = '/upload/epgo-covers/daily.png'
        elif class1 in (111,112,113,114):
            img = '/upload/epgo-covers/ket.png'
        elif class1 in (121,122,123,124):
            img = '/upload/epgo-covers/pet.png'
        vals = (title, desc, content, class1, img, 'admin', random.randint(18, 220), dt, dt, 'cn', 'admin')
        cur.execute(sql, vals)
        inserted += 1
conn.commit()
print('inserted', inserted)
cur.execute("SELECT class1,COUNT(*) FROM ep_news WHERE recycle=0 AND class1 IN (103,104,105,111,112,113,114,121,122,123,124) GROUP BY class1 ORDER BY class1")
for row in cur.fetchall():
    print(row)
conn.close()
