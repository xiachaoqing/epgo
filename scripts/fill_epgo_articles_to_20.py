import pymysql, random
from datetime import datetime, timedelta

DB = dict(host='localhost', user='xiachaoqing', password='Xia@07090218', db='epgo_db', charset='utf8mb4')

TOPICS = {
    103: ['学校生活', '科技生活', '环境保护', '文化艺术', '旅行出行', '健康饮食', '体育运动', '职业规划', '购物消费', '社会热点'],
    104: ['梦想与成长', '校园生活', '科技创新', '环境保护', '文化交流', '职业规划', '团队合作', '健康生活', '时间管理', '阅读习惯'],
    105: ['课堂表达', '时间安排', '天气描述', '鼓励赞美', '情绪表达', '学习计划', '校园交流', '旅行表达', '日常礼貌', '目标管理'],
    111: ['Reading Part 1', 'Reading Part 2', 'Reading Part 3', 'Writing Part 7', 'Writing Part 8', 'Listening Part 1', 'Listening Part 2', 'Listening Part 3'],
    112: ['学校生活', '食物饮料', '交通出行', '购物消费', '兴趣爱好', '自然环境', '日常交流', '科技数码'],
    113: ['邮件写作', '邀请回复', '活动通知', '日常记录', '图片描述', '句型升级', '连接词使用', '常见失分点'],
    114: ['图片题', '时间题', '地点题', '数字题', '人物关系题', '同义替换题', '短对话题', '关键信息题'],
    121: ['Reading Part 1', 'Reading Part 2', 'Reading Part 3', 'Reading Part 4', 'Listening Part 1', 'Listening Part 2', 'Writing Part 1', 'Writing Part 2'],
    122: ['校园主题', '科技主题', '环境主题', '旅行主题', '健康主题', '媒体主题', '生活方式', '社会交往'],
    123: ['邮件回复', '记叙文', '观点表达', '连接词', '开头结尾', '语法纠错', '高分句型', '任务拆解'],
    124: ['主旨题', '细节题', '同义替换', '段落匹配', '长文定位', '排除法', '速读技巧', '信息筛选'],
}

TITLE_TMPL = {
    103: '英语阅读技巧：{topic}主题短文精读与训练',
    104: '英语演讲提升：{topic}主题表达训练',
    105: '每日英语 | {topic}高频表达整理',
    111: 'KET真题解析：{topic}专项突破',
    112: 'KET词汇速记：{topic}核心词汇清单',
    113: 'KET写作指导：{topic}高分模板',
    114: 'KET听力技巧：{topic}答题训练',
    121: 'PET真题解析：{topic}专项讲解',
    122: 'PET词汇速记：{topic}核心表达积累',
    123: 'PET写作指导：{topic}写作方法',
    124: 'PET阅读技巧：{topic}解题思路',
}

DESC_TMPL = '围绕{topic}场景整理高频表达、常见题型与实用训练方法，帮助学习者更系统地提升英语能力。'

IMG_MAP = {
    103: '/upload/epgo-covers/reading.png', 104: '/upload/epgo-covers/speech.png', 105: '/upload/epgo-covers/daily.png',
    111: '/upload/epgo-covers/ket.png', 112: '/upload/epgo-covers/ket.png', 113: '/upload/epgo-covers/ket.png', 114: '/upload/epgo-covers/ket.png',
    121: '/upload/epgo-covers/pet.png', 122: '/upload/epgo-covers/pet.png', 123: '/upload/epgo-covers/pet.png', 124: '/upload/epgo-covers/pet.png',
}

CONTENT_TMPL = '''<p>{desc}</p>
<h3>本篇重点</h3>
<ul>
<li>理解 {topic} 主题中的核心表达与常见用法</li>
<li>梳理该主题在阅读、写作或考试中的高频出现方式</li>
<li>完成一次小练习，把输入转化为输出</li>
</ul>
<h3>学习建议</h3>
<p>建议先通读全文，再整理关键词和表达搭配，最后用自己的话进行复述或写出小结，这样更容易形成长期记忆。</p>
<p>如果你正在准备 KET / PET，也可以把本篇内容和真题训练结合起来，提升迁移使用能力。</p>
'''

TARGET = 20
COLUMN_IDS = [103,104,105,111,112,113,114,121,122,123,124]

conn = pymysql.connect(**DB)
cur = conn.cursor()
cur.execute("SELECT class1,COUNT(*) FROM ep_news WHERE recycle=0 AND class1 IN (103,104,105,111,112,113,114,121,122,123,124) GROUP BY class1")
counts = dict(cur.fetchall())
inserted = 0
sql = "INSERT INTO ep_news (title,description,content,class1,class2,class3,no_order,wap_ok,img_ok,imgurl,com_ok,issue,hits,updatetime,addtime,lang,recycle,displaytype,publisher) VALUES (%s,%s,%s,%s,0,0,0,1,1,%s,1,%s,%s,%s,%s,%s,0,1,%s)"
for cid in COLUMN_IDS:
    need = max(0, TARGET - counts.get(cid, 0))
    topics = TOPICS[cid]
    for i in range(need):
        topic = topics[(counts.get(cid,0) + i) % len(topics)]
        title = TITLE_TMPL[cid].format(topic=topic)
        cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND class1=%s AND title=%s", (cid, title))
        if cur.fetchone()[0]:
            title = f"{title}（专题{i+1}）"
        desc = DESC_TMPL.format(topic=topic)
        content = CONTENT_TMPL.format(topic=topic, desc=desc)
        dt = (datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))).strftime('%Y-%m-%d %H:%M:%S')
        vals = (title, desc, content, cid, IMG_MAP[cid], 'admin', random.randint(10, 260), dt, dt, 'cn', 'system')
        cur.execute(sql, vals)
        inserted += 1
conn.commit()
print('inserted', inserted)
cur.execute("SELECT class1,COUNT(*) FROM ep_news WHERE recycle=0 AND class1 IN (103,104,105,111,112,113,114,121,122,123,124) GROUP BY class1 ORDER BY class1")
for row in cur.fetchall():
    print(row)
conn.close()
