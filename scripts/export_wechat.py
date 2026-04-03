#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地运行：通过SSH连接openclaw导出文章，然后导入epgo数据库
"""
from __future__ import print_function
import subprocess
import json
import sys
import re
from datetime import datetime
import pymysql

DRY_RUN = '--dry' in sys.argv

DST = dict(
    host='101.42.21.191',
    port=3306,
    user='xiachaoqing',
    password='07090218',
    db='epgo_db',
    charset='utf8mb4',
    connect_timeout=10,
)

COLUMNS = {
    'ket_exam':  140,
    'ket_word':  141,
    'ket_write': 142,
    'ket':       128,
    'pet':       127,
    'english':   126,
}


def guess_column(title):
    t = title
    if 'KET' in t or 'KET' in t.upper():
        if '真题' in t: return COLUMNS['ket_exam']
        if '词汇' in t or '单词' in t or '短语' in t: return COLUMNS['ket_word']
        if '写作' in t or '作文' in t or '句型' in t: return COLUMNS['ket_write']
        return COLUMNS['ket']
    if 'PET' in t:
        return COLUMNS['pet']
    if '写作' in t or '作文' in t or '句型' in t or '连接词' in t:
        return COLUMNS['ket_write']
    if '词汇' in t or '单词' in t or '短语' in t or '用法' in t:
        return COLUMNS['ket_word']
    return COLUMNS['english']


def clean_content(html):
    if not html:
        return ''
    html = re.sub(r'\s*data-[a-z_-]+=(?:"[^"]*"|\'[^\']*\')', '', html)
    html = re.sub(r'font-family:[^;"\'}]+;?', '', html)
    # 图片适配
    html = re.sub(r'(<img)([^>]*)(>)',
        lambda m: m.group(1)
            + re.sub(r'style="[^"]*"', '', m.group(2))
            + ' style="max-width:100%;height:auto;border-radius:6px;margin:8px 0;"'
            + m.group(3), html)
    # 去掉公众号顶部版权行
    html = re.sub(r'<p[^>]*>\s*✨[^<]*</p>', '', html)
    html = re.sub(r'<section[^>]*>\s*</section>', '', html, flags=re.DOTALL)
    # 末尾CTA
    html += u"""
<hr style="border:none;border-top:2px dashed #e0e0e0;margin:30px 0 20px;">
<div style="background:#e8f4fd;border-left:4px solid #1E88E5;padding:16px 20px;border-radius:0 8px 8px 0;">
  <p style="margin:0 0 6px;font-weight:700;color:#1565C0;">关注公众号「英语陪跑GO」</p>
  <p style="margin:0;font-size:14px;color:#555;">每天5分钟，KET/PET备考干货·词汇速记·写作模板·真题解析，免费领取！</p>
</div>"""
    return html.strip()


def make_desc(html, length=150):
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^[✨\s]+', '', text)
    return text[:length] + ('...' if len(text) > length else '')


def make_keywords(title):
    kws = [u'英语陪跑GO', u'剑桥英语']
    for w in ['KET', 'PET', u'写作', u'词汇', u'真题', u'语法']:
        if w in title:
            kws.insert(0, w)
    return ','.join(kws[:5])


def fetch_articles_via_ssh():
    """通过SSH在openclaw服务器执行Python读取数据库，JSON输出"""
    script = """
import pymysql, json, sys
conn = pymysql.connect(host='localhost',user='root',password='t96wKmf1fMyp2GYz',
    db='wechat_platform',charset='utf8mb4')
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute("SELECT id,title,digest,content,thumb_url,publish_time FROM we_articles WHERE publish_status=1 AND title!='' ORDER BY id")
rows = []
for r in cur.fetchall():
    rows.append({
        'id': r['id'],
        'title': r['title'] or '',
        'digest': r['digest'] or '',
        'content': r['content'] or '',
        'thumb_url': r['thumb_url'] or '',
        'publish_time': str(r['publish_time']) if r['publish_time'] else '',
    })
conn.close()
print(json.dumps(rows, ensure_ascii=False))
"""
    result = subprocess.check_output(
        ['ssh', 'openclaw', 'python3 -c "{}"'.format(script.replace('"', '\\"'))],
        stderr=subprocess.DEVNULL
    )
    return json.loads(result.decode('utf-8'))


def fetch_articles_via_ssh_file():
    """把脚本写成文件传过去执行，避免引号问题"""
    with open('/tmp/_fetch_articles.py', 'w') as f:
        f.write("""# -*- coding: utf-8 -*-
import pymysql, json
conn = pymysql.connect(host='localhost',user='root',password='t96wKmf1fMyp2GYz',
    db='wechat_platform',charset='utf8mb4')
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute("SELECT id,title,digest,content,thumb_url,publish_time FROM we_articles WHERE publish_status=1 AND title!='' ORDER BY id")
rows = []
for r in cur.fetchall():
    rows.append({
        'id': r['id'],
        'title': r['title'] or '',
        'digest': r['digest'] or '',
        'content': r['content'] or '',
        'thumb_url': r['thumb_url'] or '',
        'pub_time': str(r['publish_time']) if r['publish_time'] else '',
    })
conn.close()
print(json.dumps(rows, ensure_ascii=False))
""")
    # 传脚本
    subprocess.call(['scp', '-q', '/tmp/_fetch_articles.py', 'openclaw:/tmp/_fa.py'])
    # 执行并获取结果
    result = subprocess.check_output(
        ['ssh', 'openclaw', 'python3 /tmp/_fa.py'],
        stderr=subprocess.PIPE
    )
    return json.loads(result.decode('utf-8'))


def main():
    print('[{}] 开始同步公众号文章'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    # 获取文章
    print('从 openclaw 读取文章...')
    try:
        articles = fetch_articles_via_ssh_file()
        print('读取到 {} 篇'.format(len(articles)))
    except Exception as e:
        print('读取失败: {}'.format(e))
        sys.exit(1)

    if DRY_RUN:
        print('\n** DRY RUN 预览 **')
        for a in articles:
            col = guess_column(a['title'])
            print('  [{}] col:{} - {}'.format(a['id'], col, a['title'][:40]))
        return

    # 连接epgo数据库
    try:
        dst = pymysql.connect(**DST)
        print('epgo 连接成功')
    except Exception as e:
        print('epgo 连接失败: {}'.format(e))
        sys.exit(1)

    cur = dst.cursor()
    count = skip = 0

    for art in articles:
        title = art['title'].strip()
        if not title:
            continue

        cur.execute("SELECT id FROM ep_news WHERE title=%s LIMIT 1", (title,))
        if cur.fetchone():
            skip += 1
            continue

        content = clean_content(art['content'])
        digest = art['digest'] or ''
        desc = make_desc(digest or content)
        col_id = guess_column(title)
        keywords = make_keywords(title)
        imgurl = art['thumb_url'] or ''
        pub_time = art['pub_time'] or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cur.execute("""INSERT INTO ep_news
            (title, ctitle, keywords, description, content,
             bigclass, imgurl, img_ok, inputtime, updatetime,
             lang, isshow, issys, hits)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'cn',1,0,0)
        """, (title, title, keywords, desc, content,
              col_id, imgurl, 1 if imgurl else 0,
              pub_time, pub_time))
        dst.commit()
        count += 1
        print('  [{}] {} -> col:{}'.format(count, title[:30], col_id))

    dst.close()
    print('\n完成！写入:{} 跳过:{}'.format(count, skip))


if __name__ == '__main__':
    main()
