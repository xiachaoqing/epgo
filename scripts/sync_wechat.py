#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章 -> epgo官网数据库同步脚本
在 epgo 服务器上执行（可直连两端数据库）

用法：
  python3 sync_wechat.py       # 正式同步
  python3 sync_wechat.py --dry # 预览不写入
"""
from __future__ import print_function
import sys
import re
from datetime import datetime
import pymysql

DRY_RUN = '--dry' in sys.argv

# 源库：openclaw 微信公众号
SRC = dict(
    host='39.105.154.244',
    port=3306,
    user='root',
    password='t96wKmf1fMyp2GYz',
    db='wechat_platform',
    charset='utf8mb4',
    connect_timeout=10,
)

# 目标库：epgo 官网
DST = dict(
    host='localhost',
    port=3306,
    user='xiachaoqing',
    password='07090218',
    db='epgo_db',
    charset='utf8mb4',
)

# 栏目映射
COLUMNS = {
    'ket_exam': 140,   # KET真题解析
    'ket_word': 141,   # KET词汇速记
    'ket_write': 142,  # KET写作指导
    'ket': 128,        # KET备考（通用）
    'pet': 127,        # PET备考
    'english': 126,    # 英语学习（通用）
}


def guess_column(title):
    t = title
    if 'KET' in t or 'ket' in t.lower():
        if '真题' in t: return COLUMNS['ket_exam']
        if '词汇' in t or '单词' in t or '短语' in t: return COLUMNS['ket_word']
        if '写作' in t or '作文' in t or '句型' in t: return COLUMNS['ket_write']
        return COLUMNS['ket']
    if 'PET' in t or 'pet' in t.lower():
        return COLUMNS['pet']
    if '写作' in t or '作文' in t or '句型' in t or '连接词' in t:
        return COLUMNS['ket_write']
    if '词汇' in t or '单词' in t or '短语' in t or '用法' in t:
        return COLUMNS['ket_word']
    return COLUMNS['english']


def clean_content(html):
    """清理微信HTML，适配网站展示"""
    if not html:
        return ''
    # 去掉微信私有属性
    html = re.sub(r'\s*data-[a-z_-]+=(?:"[^"]*"|\'[^\']*\')', '', html)
    # 图片适配
    html = re.sub(
        r'(<img)([^>]*?)(>)',
        lambda m: m.group(1) + re.sub(r'style="[^"]*"', '', m.group(2))
                + ' style="max-width:100%;height:auto;border-radius:6px;margin:10px 0;"'
                + m.group(3),
        html
    )
    # 去掉空section
    html = re.sub(r'<section[^>]*>\s*</section>', '', html, flags=re.DOTALL)
    # 统一字体
    html = re.sub(r'font-family:[^;"\']*(;|(?=["\']))', '', html)
    # 去掉顶部版权行（公众号特有）
    html = re.sub(
        r'<p[^>]*>\s*✨[^<]*阅读[^<]*</p>', '', html)
    # 尾部加CTA
    html += """
<hr style="border:none;border-top:2px dashed #e0e0e0;margin:30px 0 20px;">
<div style="background:#e8f4fd;border-left:4px solid #1E88E5;padding:16px 20px;
     border-radius:0 8px 8px 0;margin-bottom:20px;">
  <p style="margin:0 0 6px;font-weight:700;color:#1565C0;font-size:15px;">
    关注公众号「英语陪跑GO」</p>
  <p style="margin:0;font-size:14px;color:#555;line-height:1.7;">
    每天5分钟，KET/PET备考干货持续更新。词汇速记·真题解析·写作模板，免费领取！</p>
</div>"""
    return html.strip()


def make_desc(html, length=120):
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^[✨\s]+', '', text)
    return text[:length] + ('...' if len(text) > length else '')


def make_keywords(title):
    kws = ['英语陪跑GO', '剑桥英语备考']
    for w in ['KET', 'PET', 'FCE', '写作', '词汇', '真题', '语法', '听力']:
        if w in title:
            kws.insert(0, w)
    return ','.join(kws[:5])


def main():
    print('[{}] 微信文章同步开始'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    if DRY_RUN:
        print('** DRY RUN **')

    # 连接源库
    try:
        src = pymysql.connect(**SRC)
        print('openclaw 连接成功')
    except Exception as e:
        print('openclaw 连接失败: {}'.format(e))
        print('提示：请在 epgo 服务器上执行此脚本，或确认防火墙允许3306端口')
        sys.exit(1)

    # 连接目标库
    try:
        dst = pymysql.connect(**DST)
        print('epgo 连接成功')
    except Exception as e:
        print('epgo 连接失败: {}'.format(e))
        src.close()
        sys.exit(1)

    src_cur = src.cursor(pymysql.cursors.DictCursor)
    dst_cur = dst.cursor()

    # 读取公众号文章（只取已发布的）
    src_cur.execute("""
        SELECT id, title, digest, content, thumb_url, publish_time, created_at
        FROM we_articles
        WHERE publish_status=1 AND title != ''
        ORDER BY id ASC
    """)
    articles = src_cur.fetchall()
    print('读取到 {} 篇已发布文章'.format(len(articles)))

    count = 0
    skip = 0

    for art in articles:
        title = (art['title'] or '').strip()
        if not title:
            continue

        # 去重检查
        dst_cur.execute(
            "SELECT id FROM ep_news WHERE title=%s LIMIT 1", (title,))
        if dst_cur.fetchone():
            skip += 1
            continue

        content = clean_content(art['content'] or '')
        digest = art['digest'] or make_desc(content)
        desc = digest[:200] if digest else make_desc(content)
        col_id = guess_column(title)
        keywords = make_keywords(title)
        imgurl = art['thumb_url'] or ''
        pub_time = art['publish_time'] or art['created_at'] or datetime.now()
        if hasattr(pub_time, 'strftime'):
            pub_time = pub_time.strftime('%Y-%m-%d %H:%M:%S')

        print('  [{}] {} -> col:{}'.format(
            'DRY' if DRY_RUN else '写入',
            title[:28],
            col_id))

        if not DRY_RUN:
            dst_cur.execute("""
                INSERT INTO ep_news
                (title, ctitle, keywords, description, content,
                 bigclass, imgurl, img_ok,
                 inputtime, updatetime,
                 lang, isshow, issys, hits)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'cn',1,0,0)
            """, (
                title, title, keywords, desc, content,
                col_id, imgurl, 1 if imgurl else 0,
                pub_time, pub_time
            ))
            dst.commit()
            count += 1

    src.close()
    dst.close()
    print('\n完成！写入 {} 篇，跳过(已存在) {} 篇'.format(count, skip))


if __name__ == '__main__':
    main()
