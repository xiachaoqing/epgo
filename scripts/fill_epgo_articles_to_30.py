import pymysql, random
from datetime import datetime, timedelta

DB = dict(host='localhost', user='xiachaoqing', password='Xia@07090218', db='epgo_db', charset='utf8mb4')
TARGET = 30
COLUMN_IDS = [103,104,105,111,112,113,114,121,122,123,124]

TOPICS = {
    103: ['学校生活', '科技生活', '环境保护', '文化艺术', '旅行出行', '健康饮食', '体育运动', '职业规划', '购物消费', '社会热点', '媒体素养', '城市发展', '家庭关系', '阅读习惯', '时间管理'],
    104: ['梦想与成长', '校园生活', '科技创新', '环境保护', '文化交流', '职业规划', '团队合作', '健康生活', '时间管理', '阅读习惯', '数字时代', '运动精神', '志愿服务', '自我管理', '公共表达'],
    105: ['课堂表达', '时间安排', '天气描述', '鼓励赞美', '情绪表达', '学习计划', '校园交流', '旅行表达', '日常礼貌', '目标管理', '购物表达', '请假说明', '电话沟通', '兴趣爱好', '安排活动'],
    111: ['Reading Part 1', 'Reading Part 2', 'Reading Part 3', 'Writing Part 7', 'Writing Part 8', 'Listening Part 1', 'Listening Part 2', 'Listening Part 3', 'Listening Part 4', 'Listening Part 5'],
    112: ['学校生活', '食物饮料', '交通出行', '购物消费', '兴趣爱好', '自然环境', '日常交流', '科技数码', '身体健康', '节日文化'],
    113: ['邮件写作', '邀请回复', '活动通知', '日常记录', '图片描述', '句型升级', '连接词使用', '常见失分点', '时间安排', '活动总结'],
    114: ['图片题', '时间题', '地点题', '数字题', '人物关系题', '同义替换题', '短对话题', '关键信息题', '地图题', '多选题'],
    121: ['Reading Part 1', 'Reading Part 2', 'Reading Part 3', 'Reading Part 4', 'Listening Part 1', 'Listening Part 2', 'Writing Part 1', 'Writing Part 2', 'Speaking Part 1', 'Speaking Part 2'],
    122: ['校园主题', '科技主题', '环境主题', '旅行主题', '健康主题', '媒体主题', '生活方式', '社会交往', '职业启蒙', '文化活动'],
    123: ['邮件回复', '记叙文', '观点表达', '连接词', '开头结尾', '语法纠错', '高分句型', '任务拆解', '时间类写作', '活动类写作'],
    124: ['主旨题', '细节题', '同义替换', '段落匹配', '长文定位', '排除法', '速读技巧', '信息筛选', '句意判断', '标题匹配'],
}

TITLE_TMPL = {
    103: '英语阅读专题：{topic}主题精读训练',
    104: '英语演讲专题：{topic}主题表达训练',
    105: '每日英语 | {topic}实用表达积累',
    111: 'KET真题解析：{topic}高频考点拆解',
    112: 'KET词汇速记：{topic}词汇与短语整理',
    113: 'KET写作指导：{topic}写作训练',
    114: 'KET听力技巧：{topic}题型专项',
    121: 'PET真题解析：{topic}高频考点讲解',
    122: 'PET词汇速记：{topic}高频表达整理',
    123: 'PET写作指导：{topic}高分写作方法',
    124: 'PET阅读技巧：{topic}专项提升',
}

IMG_MAP = {103:'/upload/epgo-covers/reading.png',104:'/upload/epgo-covers/speech.png',105:'/upload/epgo-covers/daily.png',111:'/upload/epgo-covers/ket.png',112:'/upload/epgo-covers/ket.png',113:'/upload/epgo-covers/ket.png',114:'/upload/epgo-covers/ket.png',121:'/upload/epgo-covers/pet.png',122:'/upload/epgo-covers/pet.png',123:'/upload/epgo-covers/pet.png',124:'/upload/epgo-covers/pet.png'}

conn = pymysql.connect(**DB)
cur = conn.cursor()
cur.execute("SELECT class1,COUNT(*) FROM ep_news WHERE recycle=0 AND class1 IN (103,104,105,111,112,113,114,121,122,123,124) GROUP BY class1")
counts = dict(cur.fetchall())
sql = "INSERT INTO ep_news (title,description,content,class1,class2,class3,no_order,wap_ok,img_ok,imgurl,com_ok,issue,hits,updatetime,addtime,lang,recycle,displaytype,publisher) VALUES (%s,%s,%s,%s,0,0,0,1,1,%s,1,%s,%s,%s,%s,%s,0,1,%s)"
inserted = 0
for cid in COLUMN_IDS:
    need = max(0, TARGET - counts.get(cid, 0))
    topics = TOPICS[cid]
    for i in range(need):
        idx = counts.get(cid, 0) + i
        topic = topics[idx % len(topics)]
        title = TITLE_TMPL[cid].format(topic=topic)
        cur.execute("SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND class1=%s AND title=%s", (cid, title))
        if cur.fetchone()[0]:
            title = f"{title}（扩展{i+1}）"
        desc = f'围绕{topic}场景整理高频表达、常见题型和可执行训练方法，帮助学习者在英语应用与考试备考中持续提升。'
        content = f'''<p>{desc}</p><h3>学习重点</h3><ul><li>掌握 {topic} 主题中的核心表达与词汇搭配</li><li>理解该主题在考试和真实交流中的常见出现方式</li><li>结合练习完成输入、整理与输出</li></ul><h3>训练建议</h3><p>建议先阅读理解，再整理表达，最后用自己的话口头复述或写出一段简短总结。</p><p>长期坚持同主题输入，能明显提升阅读、写作和表达稳定性。</p>'''
        dt = (datetime.now() - timedelta(days=random.randint(0, 45), hours=random.randint(0, 23))).strftime('%Y-%m-%d %H:%M:%S')
        vals = (title, desc, content, cid, IMG_MAP[cid], 'admin', random.randint(10, 320), dt, dt, 'cn', 'system')
        cur.execute(sql, vals)
        inserted += 1
conn.commit()
print('inserted', inserted)
cur.execute("SELECT class1,COUNT(*) FROM ep_news WHERE recycle=0 AND class1 IN (103,104,105,111,112,113,114,121,122,123,124) GROUP BY class1 ORDER BY class1")
for row in cur.fetchall():
    print(row)
conn.close()
