# 英语陪跑 GO — 运营手册

> 最后更新：2026-04-25
> 维护：夏超青（夏小石）

---

## 一、关键地址与账号

| 用途 | 地址/值 |
|------|---------|
| 落地页 | https://go.xiachaoqing.com/epgo/ |
| 支付结果页 | https://go.xiachaoqing.com/epgo/result.html |
| 管理后台 | https://go.xiachaoqing.com/epgo/admin.html |
| 后台 Token | `jzt_admin_2026_change_me` ← **建议修改！** |
| API 服务器 | https://wechat.xiachaoqing.com |
| 服务器 IP（API/公众号） | 39.105.154.244 |
| 服务器 IP（前端静态） | 101.42.21.191 |

> ⚠️ Token 是登录管理后台的唯一凭证。建议在服务器 `/etc/systemd/system/wechat-platform.service` 里设置环境变量 `JZT_ADMIN_TOKEN=你的新token`，然后 `systemctl daemon-reload && systemctl restart wechat-platform`。

---

## 二、完整购买流程

```
用户打开落地页
    ↓ 微信内打开，自动 OAuth 授权获取 openid
    ↓ 选择套餐 → 填写手机号（用于关联 App 账号）→ 微信支付
    ↓ 支付成功 → 跳转 result.html
    ↓ 后端 /order/notify 回调（微信支付通知）
    ↓ 查账号池有无可用账号
        ├─ 有账号 → 自动分配 → 推送微信模板消息给用户（含账号信息）
        └─ 无账号 → 创建"待录入"记录 → 发客服消息通知夏小石
    ↓ 夏小石收到微信通知 → 登录管理后台 → 录入账号
    ↓ 录入完成 → 后台自动推送激活通知给用户
```

---

## 三、管理后台功能说明

### 登录
- 地址：`/epgo/admin.html`
- 输入 Token 登录（Token 见上方）

### 数据概览
| 卡片 | 含义 |
|------|------|
| 今日新增 | 当天新付款订单数 |
| 待录入 | 已付款但账号还未录入的订单数（⚠️ 需要处理） |
| 已激活账号 | 当前有效的激活账号数量 |
| 本月收入 | 当月已付款订单合计 |
| 总付款订单 | 历史所有已付款订单 |

下方速览最近 5 条待录入订单，点「录入账号」可直接处理。

### 全部订单 — Tab 分类
- **全部**：所有订单
- **已付款**：已支付但还未激活（有角标提醒数量）
- **已激活**：已分配账号的订单
- **已退款**：退款订单（pay_status=9）
- **待付款**：创建了但还没支付的

### 账号管理
状态说明：
- **已激活**：账号正常，可以登录 App
- **已过期**：账号到期，需续费
- **待录入**：已有购买记录但账号还没填入
- **禁用**：手动禁用

操作：
- **✏️ 编辑**：修改账号、密码、到期日、套餐、备注、状态
- **禁用/启用**：一键切换状态

### 系统设置
- 查看/复制当前 Token（点击显示/隐藏）
- 快速复制各地址

---

## 四、微信菜单「查账号」/「续费」如何关联到用户

**重要机制说明：**

系统通过 **openid 关联**，不是手机号关联。流程如下：

1. 用户在落地页付款时，页面已经做了微信 OAuth 授权，拿到了 `openid`
2. 订单表 `jzt_orders.openid` 记录了购买者的微信 openid
3. 用户在公众号点「查账号」→ 发的是 CLICK 事件，服务器能获取这次请求的 `openid`
4. 后端用这个 `openid` 去 `jzt_orders` 里查有没有对应的已付款订单 → 找到了就返回账号信息

**如果查不到的情况：**
- 用户购买时没有在公众号内打开落地页（比如复制链接在浏览器打开），导致 openid 没有绑定到订单
- 用户换了微信号

**目前没有独立绑定功能**，如果有用户购买后查不到，运营侧手动处理（在 admin 后台找到这条订单，手动录入后用公众号给用户发消息告知账号）。

**是否需要加绑定功能：** 可以加。方案是：用户回复手机号 → 系统查手机号对应的订单 → 将当前 openid 写入订单。但这有安全风险（别人用你手机号可以绑走账号），需要加验证码。暂时不加，运营侧人工处理即可。

---

## 五、购买通知管理员机制

当有用户付款且账号池不足（需要手动录入）时，系统会立即给夏小石（openid: `oShQE6TxKM_xTLpkzvaOBkaW7Rb4`）发一条**微信客服消息**（text 类型，非模板消息），内容如下：

```
🔔 新订单需要录入！

手机号：13161241306
套餐：7天体验卡 ¥9
订单号：JZT2026...

请尽快登录后台录入账号：
https://go.xiachaoqing.com/epgo/admin.html
```

> 注意：客服消息只能在用户48小时内有过互动时才能发送。如果收不到，可以看管理后台的「待录入」提醒。

---

## 六、套餐价格

| 套餐 | 天数 | 价格 |
|------|------|------|
| 7天体验卡 | 7天 | ¥9.9 |
| 月卡 | 30天 | ¥39 |
| 季卡 | 90天 | ¥99 |
| 年卡 | 365天 | ¥399 |

---

## 七、服务器运维

### 常用命令

```bash
# 查看服务状态
systemctl status wechat-platform

# 重启服务
systemctl restart wechat-platform

# 查看日志
tail -f /www/wwwroot/wechat_platform/logs/app.log

# 查看最近错误
grep ERROR /www/wwwroot/wechat_platform/logs/app.log | tail -20
```

### 关键文件路径

| 文件 | 路径 |
|------|------|
| API 服务（Python/FastAPI） | `/www/wwwroot/wechat_platform/` |
| 落地页/管理后台（HTML） | `/www/wwwroot/go.xiachaoqing.com/epgo/` |
| 旧路径（同步保留） | `/www/wwwroot/go.xiachaoqing.com/jiazhangtong/` |
| 游戏页面 | `/www/wwwroot/wechat_reply/games/` |

### Git 维护说明

代码在本地维护，手动 sftp 上传到服务器。建议：
```bash
cd /Users/xiachaoqing/projects/epgo
git add -A
git commit -m "描述本次改动"

cd /Users/xiachaoqing/projects/openclaw_file
git add -A
git commit -m "描述本次改动"
```

---

## 八、密码相关说明

- 初始密码：手机号后6位（系统自动设置）
- 用户可以在 App 内自行修改密码
- 管理后台显示的是**初始密码**，如果用户改过则无法从这里查到
- 密码**不会**通过前端接口返回给普通用户（安全保护）
- 用户忘记密码：公众号回复「查账号」会提示"初始密码为手机号后6位，如已修改请联系客服"

---

## 九、常见问题排查

| 现象 | 排查方向 |
|------|----------|
| 用户支付后没收到通知 | 检查 openid 是否在微信内授权，查日志 `_send_pay_notify` |
| 查账号返回"开通中" | 正常，账号池不足时的临时状态，去后台录入后用户再查就OK |
| 查账号返回"未找到" | 用户购买时没用微信内浏览器，openid没绑定，手动处理 |
| 管理后台列表打不开 | Token 是否正确，查 F12 Network 看接口返回 |
| 分享不生效 | wx.config 签名问题，查 Console 里的微信 JS-SDK 报错 |
| 500 错误 | 查 `tail -20 /www/wwwroot/wechat_platform/logs/app.log` |
