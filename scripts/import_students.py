#!/usr/bin/env python3
"""导入老学员到 jzt_accounts 表"""
import pymysql

DB = dict(host='localhost', port=3306, user='root',
          passwd='t96wKmf1fMyp2GYz', db='wechat_platform',
          charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

STUDENTS = [
    ("李子涵",   "15321103160", "15321103160", None),
    ("马子钊",   "13811615057", "13811615057", None),
    ("Gdmdy126607","13810071599","13810071599",None),
    ("Anne",     "13121099221", "13121099221", None),
    ("佳潼",     "13716407951", "13716407951", None),
    ("笑笑",     "13811722799", "13811722799", None),
    ("淼淼",     "13693598167", "13693598167", None),
    ("Yoyo",     "19520062351", "19520062351", None),
    ("高子茗",   "18510488721", "18510488721", None),
    ("Elsa",     "13601168170", "13601168170", None),
    ("Eric",     "13810564102", "13810564102", None),
    ("Yoyo2",    "13621141164", "13621141164", None),
    ("max",      "13439191143", "13439191143", None),
    ("Anne2",    "18611003065", "18611003065", None),
    ("王彦洲",   "15801239224", "15801239224", "2026-12-01"),
    ("MIA.",     "13811983236", "13811983236", "2026-11-01"),
    ("李亮",     "18612600500", "18612600500", "2026-11-01"),
    ("Delia",    "13810533262", "13810533262", "2026-11-01"),
    ("冬青",     "A18612597785","",            "2026-11-01"),
    ("亿",       "18612420886", "18612420886", "2026-11-01"),
    ("Amber",    "13520574790", "13520574790", "2026-11-01"),
    ("Becky",    "18511898423", "18511898423", "2026-11-01"),
    ("王梓迪",   "13426496662", "13426496662", "2026-11-01"),
    ("杨茗雨",   "15201302951", "15201302951", "2026-11-01"),
    ("Alice",    "13911292265", "13911292265", "2026-11-01"),
    ("金淼",     "13070110958", "13070110958", "2026-11-01"),
    ("贾柯然",   "13901079279", "13901079279", "2026-11-01"),
    ("李子涵2",  "15321860800", "15321860800", "2026-11-01"),
    ("Ivy",      "18618233731", "18618233731", "2026-11-01"),
]
DEFAULT_EXPIRE = "2026-12-31"

def main():
    db = pymysql.connect(**DB)
    inserted = skipped = 0
    try:
        with db.cursor() as cur:
            for name, account, phone, expire_str in STUDENTS:
                expire    = expire_str or DEFAULT_EXPIRE
                ref_phone = phone if (phone and phone.isdigit() and len(phone)==11) else account
                pwd       = (phone or account)[-6:] if (phone or account) else "123456"
                cur.execute('SELECT id FROM jzt_accounts WHERE jzt_account=%s OR (phone=%s AND phone!="") LIMIT 1',
                            (account, ref_phone))
                if cur.fetchone():
                    print(f"  跳过: {name}/{account}")
                    skipped += 1; continue
                cur.execute(
                    'INSERT INTO jzt_accounts(phone,jzt_account,jzt_password,expire_at,status,plan_name,remark,created_at,updated_at)'
                    ' VALUES(%s,%s,%s,%s,1,"老学员",%s,NOW(),NOW())',
                    (ref_phone, account, pwd, expire, f"老学员-{name}")
                )
                print(f"  导入: {name}/{account}/到期{expire}")
                inserted += 1
        db.commit()
    finally:
        db.close()
    print(f"\n完成: 导入{inserted}条, 跳过{skipped}条")

if __name__ == '__main__':
    main()
