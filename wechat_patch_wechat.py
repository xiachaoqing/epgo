"""
微信接口回调
"""
import hashlib
import time
import xml.etree.ElementTree as ET
from datetime import datetime

import pymysql
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import PlainTextResponse
from loguru import logger
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.database import get_db
from ..models.message import Message
from ..models.reply_rule import ReplyRule
from ..models.user import User
from ..services.reply_engine import ReplyEngine
from ..services.wechat_crypto import WechatCrypto
from ..services.wechat_service import WechatService
from ..services.llm_fallback import generate_fallback_reply

router = APIRouter(tags=["微信接口"])

def _get_crypto() -> WechatCrypto:
    return WechatCrypto(
        settings.WECHAT_TOKEN,
        settings.WECHAT_ENCODING_AES_KEY,
        settings.WECHAT_APP_ID,
    )

# ─── GET：微信服务器验证 ────────────────────────────────────

@router.get("/wechat")
async def wechat_verify(
    signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    echostr: str = Query(...),
):
    crypto = _get_crypto()
    if crypto.verify_signature(signature, timestamp, nonce):
        try:
            plain = crypto.decrypt_echostr(echostr)
            logger.info("✅ 微信验证成功（安全模式）")
            return PlainTextResponse(content=plain)
        except Exception:
            logger.info("✅ 微信验证成功（明文模式）")
            return PlainTextResponse(content=echostr)
    logger.warning(f"❌ 微信验证失败 sig={signature}")
    return PlainTextResponse(content="", status_code=403)

# ─── POST：微信消息接收 ─────────────────────────────────────

@router.post("/wechat")
async def wechat_callback(request: Request, db: Session = Depends(get_db)):
    start_time = time.time()
    body = await request.body()
    xml_str = body.decode("utf-8")

    msg_signature = request.query_params.get("msg_signature", "")
    timestamp = request.query_params.get("timestamp", str(int(time.time())))
    nonce = request.query_params.get("nonce", "")

    if msg_signature:
        try:
            root = ET.fromstring(xml_str)
            encrypt_node = root.find("Encrypt")
            if encrypt_node is None or not encrypt_node.text:
                logger.error("安全模式消息缺少 <Encrypt> 节点")
                return PlainTextResponse(content="")
            encrypt_str = encrypt_node.text
            crypto = _get_crypto()
            if not crypto.verify_msg_signature(msg_signature, timestamp, nonce, encrypt_str):
                logger.warning("❌ 消息签名验证失败")
                return PlainTextResponse(content="", status_code=403)
            xml_str = crypto.decrypt(encrypt_str)
            logger.info(f"安全模式解密成功，消息长度={len(xml_str)}")
        except Exception as e:
            logger.error(f"安全模式解密异常：{e}")
            return PlainTextResponse(content="")

    msg_dict = WechatService.parse_xml(xml_str)
    if not msg_dict:
        return PlainTextResponse(content="")

    msg_type = msg_dict.get("MsgType", "")
    openid   = msg_dict.get("FromUserName", "")
    to_user  = msg_dict.get("ToUserName", "")
    reply_content  = ""
    matched_rule   = None
    matched_keyword = None

    try:
        if msg_type == "event":
            event_type = msg_dict.get("Event", "")
            if event_type == "subscribe":
                # 从DB读取关注欢迎回复
                try:
                    row = db.execute(
                        "SELECT reply_content FROM we_reply_rules WHERE keyword=:k AND is_active=1 AND (is_deleted IS NULL OR is_deleted=0) ORDER BY priority DESC LIMIT 1",
                        {"k": "subscribe"}
                    ).fetchone()
                    reply_content = row[0] if row and row[0] else "欢迎关注「英语陪跑go」！\n回复「资料包」获取全套备考资料 📚"
                except Exception:
                    reply_content = "欢迎关注「英语陪跑go」！\n回复「资料包」获取全套备考资料 📚"
                _sync_user(db, openid, subscribe=True)
            elif event_type == "unsubscribe":
                _sync_user(db, openid, subscribe=False)
                return PlainTextResponse(content="")
            elif event_type == "CLICK":
                reply_content = _handle_menu_click(msg_dict.get("EventKey", ""), db=db)
            else:
                return PlainTextResponse(content="")

        elif msg_type == "text":
            content = msg_dict.get("Content", "").strip()
            logger.info(f"收到文本消息 openid={openid} content={content!r}")

            # ── 英语陪跑GO：查账号 / 续费 特殊处理 ──────────────
            if content in ('查账号', '查询账号', '我的账号', '账号', '续费'):
                reply_content = _query_jzt_account(openid)
                matched_rule = None
                matched_keyword = content
            else:
                reply_content, matched_rule, matched_keyword = ReplyEngine.match_rule(db, content)
            if matched_rule:
                ReplyEngine.update_hit_count(db, matched_rule.id)
            else:
                # 未命中规则，使用 LLM 智能兜底
                logger.info("未命中规则，使用 LLM 生成兜底回复")
                reply_content = generate_fallback_reply(content)
            # 每条消息更新用户互动记录
            _update_user_interaction(db, openid)
        else:
            reply_content = "暂不支持该消息类型"

        response_ms = int((time.time() - start_time) * 1000)
        ReplyEngine.log_message(
            db=db,
            openid=openid,
            msg_type=msg_type,
            content=msg_dict.get("Content", ""),
            reply_content=reply_content,
            matched_rule_id=matched_rule.id if matched_rule else None,
            matched_keyword=matched_keyword,
            response_time=response_ms,
        )

        plain_reply = WechatService.build_reply_xml(
            to_user=openid,
            from_user=to_user,
            content=reply_content,
        )

        if msg_signature:
            crypto = _get_crypto()
            encrypted_reply = crypto.build_encrypted_reply(plain_reply, timestamp, nonce)
            return PlainTextResponse(content=encrypted_reply, media_type="application/xml")

        return PlainTextResponse(content=plain_reply, media_type="application/xml")

    except Exception as e:
        logger.error(f"处理消息异常：{e}")
        return PlainTextResponse(content="")

# ─── 用户同步工具函数 ───────────────────────────────────────

def _sync_user(db: Session, openid: str, subscribe: bool):
    """关注/取关时同步 we_users 表"""
    try:
        user = db.query(User).filter(User.openid == openid).first()
        now = datetime.now()
        if user:
            user.subscribe_status = 1 if subscribe else 0
            if subscribe:
                user.subscribe_time = now
        else:
            user = User(
                openid=openid,
                subscribe_status=1 if subscribe else 0,
                subscribe_time=now if subscribe else None,
            )
            db.add(user)
        db.commit()
        logger.info(f"用户同步成功 openid={openid} subscribe={subscribe}")
    except Exception as e:
        logger.warning(f"同步用户失败 openid={openid} err={e}")


def _update_user_interaction(db: Session, openid: str):
    """每次收到消息时更新用户互动时间和消息计数"""
    try:
        user = db.query(User).filter(User.openid == openid).first()
        now = datetime.now()
        if user:
            user.last_interaction_at = now
            user.message_count = (user.message_count or 0) + 1
        else:
            # 发消息但没有关注记录（扫码场景）
            user = User(
                openid=openid,
                subscribe_status=1,
                subscribe_time=now,
                last_interaction_at=now,
                message_count=1,
            )
            db.add(user)
        db.commit()
    except Exception as e:
        logger.warning(f"更新用户互动失败 openid={openid} err={e}")

# ─── 菜单点击处理 ───────────────────────────────────────────

def _handle_menu_click(event_key: str, db=None) -> str:
    """菜单点击回复：优先从 we_reply_rules 精确匹配 menu_key，兜底用硬编码"""
    base = 'https://doc.xiachaoqing.com'

    # 从数据库查对应回复规则（menu_key = keyword）
    if db:
        try:
            row = db.execute(
                "SELECT reply_content FROM we_reply_rules WHERE keyword=:k AND match_type=1 AND is_active=1 AND is_deleted=0 LIMIT 1",
                {"k": event_key}
            ).fetchone()
            if row and row[0]:
                logger.info(f"菜单点击命中DB规则: {event_key}")
                return row[0]
        except Exception as e:
            logger.warning(f"菜单DB查询失败: {e}")

    # 兜底硬编码回复
    menu_replies = {
        'PET_MATERIALS': (
            '📚 PET 高频短语 100 个合集\n\n'
            '点击链接在线查看：\n'
            + base + '/pet-phrases-100.html\n\n'
            '💡 建议每天复习 10 个，坚持 10 天全部掌握！\n'
            '💪 加油，一次通过 PET！'
        ),
        'KET_MATERIALS': (
            '📚 KET 高频词汇 500 个\n\n'
            '点击链接在线查看：\n'
            + base + '/ket-vocab-500.html\n\n'
            '💡 按主题分类，含例句，适合初学者！'
        ),
        'FCE_MATERIALS': (
            '📚 FCE 进阶词汇\n\n'
            '📖 FCE词汇学习建议：\n'
            '· 重点掌握同义词替换（写作提分关键）\n'
            '· 每天学10个，配合例句记忆\n\n'
            '回复「FCE资料」获取完整资料包'
        ),
        'ALL_PACK': (
            '📦 英语陪跑 go 全套资料\n\n'
            '按级别获取：\n'
            '📗 KET 资料 → 回复「KET资料」\n'
            '📘 PET 资料 → 回复「PET资料」\n'
            '📙 FCE 资料 → 回复「FCE资料」\n\n'
            '🎮 顺手来一局：\n'
            'https://wechat.xiachaoqing.com/games/word-battle/'
        ),
        'LEVEL_GUIDE': (
            '📊 KET / PET / FCE 怎么选？\n\n'
            '🟢 KET（A2级）适合：小学高年级～初一\n'
            '🔵 PET（B1级）适合：初二～初三\n'
            '🟣 FCE（B2级）适合：高中～大学\n\n'
            '不确定？回复「选级别」获取详细测评建议'
        ),
        'LISTENING': (
            '🎧 PET 听力备考资料\n\n'
            '包含：考试结构 / 练习方法 / 高频词汇\n\n'
            '点击查看：\n'
            + base + '/pet-listening.html\n\n'
            '💡 每天精听1篇，坚持1个月听力提升明显！'
        ),
        'READING': (
            '📖 PET 阅读备考资料\n\n'
            '包含：题型解析 / 解题技巧 / 高频词汇\n\n'
            '点击查看：\n'
            + base + '/pet-reading.html\n\n'
            '💡 掌握同义替换技巧，阅读分数大幅提升！'
        ),
        'WRITING': (
            '✏️ PET 写作备考资料\n\n'
            '包含：改写句型技巧 / 书信万能模板 / 高分词组\n\n'
            '点击查看：\n'
            + base + '/pet-writing.html\n\n'
            '💡 背熟模板 + 每周写2篇，写作满分不是梦！'
        ),
        'SPEAKING': (
            '🗣️ PET 口语备考资料\n\n'
            '包含：考试流程 / 自我介绍模板 / 图片描述句型\n\n'
            '点击查看：\n'
            + base + '/pet-speaking.html\n\n'
            '💡 每天跟读15分钟，模拟真实考试场景！'
        ),
        'HISTORY': (
            '📂 查看历史文章\n\n'
            '公众号主页 → 右上角 ··· → 历史消息\n\n'
            '或回复关键词：\n'
            '· 回复「听力」→ 听力资料\n'
            '· 回复「阅读」→ 阅读资料\n'
            '· 回复「写作」→ 写作资料\n'
            '· 回复「口语」→ 口语资料'
        ),
        'ABOUT': (
            '👋 你好，我是 Cathy！\n\n'
            '📖 英语陪跑 go 创始人\n'
            '🎯 专注 KET/PET/FCE 备考教学\n'
            '✅ 已帮助 1000+ 学员通过考试\n\n'
            '💪 一起加油，轻松拿证！'
        ),
        'CONTACT': (
            '📬 联系我们\n\n'
            '💬 微信：chaoqing_pet（备注 PET 咨询）\n'
            '📱 小红书：英语陪跑 go\n\n'
            '🎁 添加微信可领取：\n'
            '· 备考资料包（完整版）\n'
            '· 一次免费学情评估\n\n'
            '⏰ 工作日 9:00-21:00 在线'
        ),
        'SERVICES': (
            '🎯 我们的服务\n\n'
            '1️⃣ 一对一辅导\n'
            '   · 定制专属学习计划\n'
            '   · 考前冲刺精准辅导\n\n'
            '2️⃣ 备考群（免费）\n'
            '   · 每日打卡督促\n'
            '   · 资料免费共享\n\n'
            '💬 回复「联系方式」添加微信了解详情'
        ),
    }
    return menu_replies.get(event_key, (
        '感谢您的点击！\n\n'
        '📚 回复「PET资料」→ 获取备考资料\n'
        '🎮 回复「KET资料」→ 获取KET资料\n'
        '📖 回复「资料包」→ 获取全套资料'
    ))


def _query_jzt_account(openid: str) -> str:
    """用openid查询英语陪跑GO账号信息，用于公众号关键词回复"""
    import os
    try:
        db = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'root'),
            passwd=os.getenv('DB_PASSWORD', 't96wKmf1fMyp2GYz'),
            db=os.getenv('DB_NAME', 'wechat_platform'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
        with db.cursor() as cur:
            # 通过openid查账号
            cur.execute(
                'SELECT a.jzt_account, a.jzt_password, a.expire_at, a.plan_name, a.status '
                'FROM jzt_accounts a '
                'WHERE a.openid=%s AND a.status=1 '
                'ORDER BY a.expire_at DESC LIMIT 1',
                (openid,)
            )
            acc = cur.fetchone()
            if not acc:
                # 尝试通过orders的openid找
                cur.execute(
                    'SELECT a.jzt_account, a.jzt_password, a.expire_at, a.plan_name, a.status '
                    'FROM jzt_orders o '
                    'JOIN jzt_accounts a ON o.account_id = a.id '
                    'WHERE o.openid=%s AND o.pay_status=1 '
                    'ORDER BY a.expire_at DESC LIMIT 1',
                    (openid,)
                )
                acc = cur.fetchone()
        db.close()

        if not acc:
            return (
                '未查到您的英语陪跑GO账号 🔍\n\n'
                '如已购买请确认：\n'
                '1. 使用本微信号授权购买\n'
                '2. 账号开通约10分钟\n\n'
                '👉 点此购买激活账号：\nhttps://go.xiachaoqing.com/jiazhangtong/\n\n'
                '有问题请联系客服'
            )

        from datetime import datetime as dt
        expire = acc['expire_at']
        is_expired = expire and expire < dt.now()
        status_str = '⚠️ 已过期' if is_expired else '✅ 有效'
        expire_str = str(expire)[:10] if expire else '-'

        reply = (
            f'🎯 您的英语陪跑GO账号信息：\n\n'
            f'账号：{acc["jzt_account"]}\n'
            f'密码：{acc["jzt_password"]}\n'
            f'套餐：{acc.get("plan_name", "-")}\n'
            f'到期：{expire_str} {status_str}\n\n'
        )
        if is_expired:
            reply += '账号已到期，点此续费：\nhttps://go.xiachaoqing.com/jiazhangtong/'
        else:
            reply += '下载APP：https://app.lingshi.com/bjxxsy'
        return reply

    except Exception as e:
        logger.warning(f'查询jzt账号失败: {e}')
        return '查询失败，请稍后重试或联系客服'

