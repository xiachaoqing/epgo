# 英语陪跑GO 落地页运维文档

> 最后更新：2026-07-20

---

## 一、架构总览

```
用户访问 https://go.xiachaoqing.com/epgo/
         │
         ▼
    ┌─────────────────────────────────────┐
    │  epgo 服务器 (101.42.21.191)        │
    │  ssh epgo                            │
    │  Nginx + PHP (MetInfo CMS)           │
    │  /www/wwwroot/go.xiachaoqing.com/    │
    │    ├── epgo/          ← 落地页（git管理）│
    │    │   ├── index.html    首页(价格页)  │
    │    │   ├── admin.html    后台管理      │
    │    │   ├── result.html   支付结果页    │
    │    │   ├── query.html    订单查询页    │
    │    │   └── share.jpg     分享封面      │
    │    └── templates/      ← CMS模板      │
    └─────────────────────────────────────┘
         │
         │ 前端调用 API
         ▼
    ┌─────────────────────────────────────┐
    │  openclaw 服务器 (39.105.154.244)    │
    │  ssh openclaw                        │
    │  Python FastAPI (uvicorn :8000)      │
    │  /www/wwwroot/wechat_platform/       │
    │    └── app/api/jiazhangtong.py       │
    │        ├── /api/jzt/order/create     │ ← 微信支付下单
    │        ├── /api/jzt/order/notify     │ ← 微信支付回调
    │        ├── /api/jzt/order/status     │ ← 查询订单状态
    │        ├── /api/jzt/user/follow      │ ← 检测公众号关注
    │        ├── /api/jzt/auth/callback    │ ← OAuth获取openid
    │        └── /api/jzt/wx/jsconfig      │ ← JS-SDK签名
    │                                      │
    │  公众号自动回复 (wechat.py)           │
    │    └── "查账号" → 自动返回账号密码     │
    └─────────────────────────────────────┘
         │
         │ 微信支付 + 模板消息
         ▼
    ┌─────────────────────────────────────┐
    │  微信公众平台                         │
    │  公众号：英语陪跑go                    │
    │  AppID: wx10b4ccec486e7961           │
    │  模板消息：                            │
    │    TMPL_PAY_OK    支付成功通知         │
    │    TMPL_ACTIVATE  账号开通通知         │
    └─────────────────────────────────────┘
```

**域名路由：**
| 域名 | 指向 | 说明 |
|------|------|------|
| go.xiachaoqing.com | epgo服务器 | 落地页 + CMS网站 |
| wechat.xiachaoqing.com | openclaw服务器 | API后端 |
| diary.xiachaoqing.com | epgo服务器 | 成长小日记小程序后端 |

---

## 二、套餐价格

| 套餐 | 价格 | 天数 | 前端key |
|------|------|------|---------|
| 7天体验卡 | ¥9.9 | 7天 | trial |
| 月卡 | ¥39 | 30天 | month |
| 季卡 | ¥99 | 90天 | quarter |
| 年卡 | ¥298（暑假特惠） | 365天 | year |

**改价格需要改两个地方：**

### 1. 前端（epgo服务器）
文件：`epgo/index.html`
- 搜索 `298` 或当前价格，改3处：
  - `price-val` 显示价格
  - `price-ori` 划线原价
  - `PLANS.year.amount` JS配置

### 2. 后端（openclaw服务器）
文件：`/www/wwwroot/wechat_platform/app/api/jiazhangtong.py`
- 第50行：`'price_fen': 29800`（单位：分，298元=29800分）
- 改完重启：`pkill -f uvicorn; cd /www/wwwroot/wechat_platform && nohup venv/bin/python3 venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2 --log-level info > /tmp/uvicorn.log 2>&1 &`

---

## 三、日常维护流程

### 修改落地页（前端）

```bash
# 1. 本地修改
cd ~/projects/epgo
vim epgo/index.html

# 2. 提交推送
git add epgo/
git commit -m "fix: 修改描述"
git push origin main

# 3. 线上拉取（一行搞定）
ssh epgo "cd /www/wwwroot/go.xiachaoqing.com && git fetch origin && git reset --hard origin/main && rm -rf cache/templates/"
```

### 修改后端（API/支付）

```bash
# 1. SSH到openclaw服务器
ssh openclaw

# 2. 编辑后端代码
vim /www/wwwroot/wechat_platform/app/api/jiazhangtong.py

# 3. 重启服务
pkill -f uvicorn
cd /www/wwwroot/wechat_platform
nohup venv/bin/python3 venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2 --log-level info > /tmp/uvicorn.log 2>&1 &

# 4. 验证
curl -s https://wechat.xiachaoqing.com/api/jzt/order/status?order_no=test
```

### 修改Nginx配置

```bash
ssh epgo
vim /www/server/panel/vhost/nginx/go.xiachaoqing.com.conf
nginx -t && nginx -s reload
```

---

## 四、支付全流程

```
1. 用户在微信打开 https://go.xiachaoqing.com/epgo/
2. 前端获取openid（OAuth静默授权）
3. 用户点击"购买年卡" → 弹窗输入手机号
4. 前端调用 POST /api/jzt/order/create
   → 后端创建订单，调微信统一下单API
   → 返回JSAPI支付参数
5. 前端调WeixinJSBridge调起微信支付
6. 用户支付成功
7. 微信服务器回调 POST /api/jzt/order/notify
   → 后端验证签名
   → 更新订单状态为已支付
   → 发送模板消息「支付成功通知」到用户公众号
   → 通知管理员（新订单提醒）
8. 管理员在 admin.html 录入账号密码
   → 后端发送模板消息「账号开通通知」到用户公众号
9. 用户在公众号收到账号密码
   → 也可在公众号回复"查账号"自动获取
```

---

## 五、后台管理

访问 `https://go.xiachaoqing.com/epgo/admin.html`
- 需要管理员Token（环境变量 `JZT_ADMIN_TOKEN`）
- 功能：
  - 查看所有订单
  - 录入/开通账号
  - 群发消息
  - 查看收入统计

---

## 六、备案信息

- ICP备案号：京ICP备2020039465号-1
- 备案链接：https://beian.miit.gov.cn/
- 显示位置：index.html / query.html / result.html 页面底部

---

## 七、关键文件清单

### epgo服务器 (101.42.21.191)
| 文件 | 说明 |
|------|------|
| `/www/wwwroot/go.xiachaoqing.com/epgo/index.html` | 落地页首页 |
| `/www/wwwroot/go.xiachaoqing.com/epgo/admin.html` | 后台管理 |
| `/www/wwwroot/go.xiachaoqing.com/epgo/query.html` | 订单查询 |
| `/www/wwwroot/go.xiachaoqing.com/epgo/result.html` | 支付结果 |
| `/www/server/panel/vhost/nginx/go.xiachaoqing.com.conf` | Nginx配置 |

### openclaw服务器 (39.105.154.244)
| 文件 | 说明 |
|------|------|
| `/www/wwwroot/wechat_platform/app/api/jiazhangtong.py` | 支付API后端 |
| `/www/wwwroot/wechat_platform/app/api/wechat.py` | 公众号消息处理 |
| `/www/wwwroot/wechat_platform/.env` | 环境变量（密钥等） |

### 本地
| 文件 | 说明 |
|------|------|
| `~/projects/epgo/epgo/` | 前端代码（git管理） |
| `~/projects/epgo/docs/英语陪跑GO运营手册.md` | 运营手册 |
| `~/projects/epgo/docs/EPGO_LANDING_PAGE_OPS.md` | 本文档 |

---

## 八、常见问题

### Q: 改了价格但页面没变？
A: 清缓存 `ssh epgo "rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/"`

### Q: 改了后端代码但API没变？
A: 重启uvicorn `ssh openclaw "pkill -f uvicorn; cd /www/wwwroot/wechat_platform && nohup venv/bin/python3 venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2 > /tmp/uvicorn.log 2>&1 &"`

### Q: git pull报冲突？
A: 强制以远程为准 `ssh epgo "cd /www/wwwroot/go.xiachaoqing.com && git fetch origin && git reset --hard origin/main"`

### Q: 旧链接 /jiazhangtong/ 还能用吗？
A: 能，Nginx配置了301跳转到 /epgo/

### Q: 微信支付不成功？
A: 检查三件事：
1. 后端uvicorn是否运行：`ssh openclaw "ps aux | grep uvicorn"`
2. API是否正常：`curl -s https://wechat.xiachaoqing.com/api/jzt/order/status?order_no=test`
3. 微信支付回调URL是否通：`curl -s https://wechat.xiachaoqing.com/api/jzt/order/notify`
