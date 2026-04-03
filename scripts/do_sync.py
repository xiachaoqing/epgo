# -*- coding: utf-8 -*-
import pymysql, json, re
from datetime import datetime

dst = pymysql.connect(host="localhost", port=3306, user="xiachaoqing",
    password="***REMOVED***", db="epgo_db", charset="utf8")
cur = dst.cursor()
cur.execute("SET NAMES utf8")

def gc(t):
    if "KET" in t:
        if u"\u771f\u9898" in t: return 140
        if u"\u8bcd\u6c47" in t or u"\u77ed\u8bed" in t: return 141
        if u"\u5199\u4f5c" in t or u"\u53e5\u578b" in t: return 142
        return 128
    if "PET" in t: return 127
    if u"\u5199\u4f5c" in t or u"\u8fde\u63a5\u8bcd" in t: return 142
    if u"\u77ed\u8bed" in t or u"\u7528\u6cd5" in t: return 141
    return 126

CTA = (u'<hr style="border:none;border-top:2px dashed #e0e0e0;margin:30px 0 20px;">'
       u'<div style="background:#e8f4fd;border-left:4px solid #1E88E5;padding:16px 20px;border-radius:0 8px 8px 0;">'
       u'<p style="margin:0 0 6px;font-weight:700;color:#1565C0;">\u5173\u6ce8\u516c\u4f17\u53f7\u300c\u82f1\u8bed\u966a\u8dd1GO\u300d</p>'
       u'<p style="margin:0;font-size:14px;color:#555;">\u6bcf\u5929KET/PET\u5907\u8003\u5e72\u8d27\uff0c\u8bcd\u6c47\u771f\u9898\u5199\u4f5c\u6a21\u677f\uff0c\u514d\u8d39\u9886\u53d6\uff01</p>'
       u'</div>')

def remove_emoji(text):
    # 去掉4字节emoji（MySQL utf8不支持）
    return re.sub(u"[\U00010000-\U0010ffff]", u"", text, flags=re.UNICODE)

def ch(html):
    if not html: return u""
    html = re.sub(r"font-family:[^;}\x27\"]+;?", u"", html)
    html = remove_emoji(html)
    return html.strip() + CTA

def dd(html, n=150):
    t = re.sub(r"<[^>]+>", u" ", html)
    t = re.sub(r"\s+", u" ", t).strip()
    return t[:n] + (u"..." if len(t) > n else u"")

with open("/tmp/_wechat_data.json", "r") as f:
    arts = json.load(f)

count = skip = 0
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
lang_cn = "cn"
kw = u"KET,PET,\u82f1\u8bed\u966a\u8dd1GO,\u5251\u6865\u82f1\u8bed"

for a in arts:
    title = remove_emoji((a.get("title") or u"").strip())
    if not title:
        continue
    cur.execute("SELECT id FROM ep_news WHERE title=%s LIMIT 1", (title,))
    if cur.fetchone():
        skip += 1
        continue
    content = ch(a.get("content", u""))
    d = dd(a.get("digest", u"") or content)[:200]
    col = gc(title)
    img = a.get("thumb_url", u"")
    pt = a.get("pub_time", u"") or now
    try:
        sql = ("INSERT INTO ep_news "
               "(title,ctitle,keywords,description,content,class1,"
               "imgurl,img_ok,addtime,updatetime,lang,recycle,hits) "
               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0,0)")
        cur.execute(sql, (title, title, kw, d, content, col,
                          img, 1 if img else 0, pt, pt, lang_cn))
        dst.commit()
        count += 1
        print(u"[{}] col:{} {}".format(count, col, title[:38]))
    except Exception as e:
        print(u"ERR:{} - {}".format(title[:20], str(e)[:60]))

dst.close()
print(u"\n写入:{} 跳过:{}".format(count, skip))
