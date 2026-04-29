# 英语陪跑GO — 项目交接文档

> 最后更新：2026-04-23
> 交接给下一个AI处理，请从头读完再动手。

---

## 一、项目概览

**业务模式**：代理销售"英语陪跑GO"APP账号激活服务
- APP本体下载**完全免费**，地址：https://app.lingshi.com/bjxxsy
- 用户下载后需要**激活账号**才能使用全部功能
- 激活账号由站长（夏朝庆）向供应商购买，成本 **¥7/账号/月**
- 站长定价销售给用户，赚取差价

**售价体系**：
| 套餐 | 售价 | 成本 | 有效期 |
|------|------|------|--------|
| 7天体验卡 | ¥4.9 | ≈¥1.6 | 7天 |
| 月卡 | ¥29 | ¥7 | 30天 |
| 季卡 | ¥79 | ¥21 | 90天 |
| 年卡 | ¥299 | ¥84 | 365天 |

---

## 二、服务器与域名

| 用途 | 域名 | IP | 备注 |
|------|------|-----|------|
| 英语陪跑GO落地页 | go.xiachaoqing.com | 101.42.21.191 | MetInfo PHP框架 |
| 微信后端API | wechat.xiachaoqing.com | 39.105.154.244 | FastAPI Python |
| 数据库 | localhost on 39.105.154.244 | — | MySQL, db: wechat_platform |

**SSH登录**：
```bash
# epgo服务器
ssh -i ~/.ssh/id_rsa root@101.42.21.191
# 后端服务器
ssh -i ~/.ssh/id_rsa_openclaw root@39.105.154.244
```

---

## 三、落地页

**本地路径**：`/Users/xiachaoqing/projects/epgo/jiazhangtong/`
**线上地址**：https://go.xiachaoqing.com/jiazhangtong/
**支付结果页**：https://go.xiachaoqing.com/jiazhangtong/result.html

**文件清单**：
- `index.html` — 主落地页（英语陪跑GO介绍 + 定价 + 下载 + 支付弹窗）
- `result.html` — 支付完成后跳转，轮询账号状态并展示

**页面功能**：
1. 介绍APP功能（用COS素材）
2. 展示两个视频（产品介绍 + 快速上手）
3. 定价区（4个套餐，点击弹出支付弹窗）
4. 填手机号 → 微信H5支付 → 跳转result.html
5. result.html轮询 `/api/jzt/order/status` 展示账号

**上传到服务器命令**：
```bash
scp -i ~/.ssh/id_rsa /Users/xiachaoqing/projects/epgo/jiazhangtong/index.html \
  /Users/xiachaoqing/projects/epgo/jiazhangtong/result.html \
  root@101.42.21.191:/www/wwwroot/go.xiachaoqing.com/jiazhangtong/
chmod 755 /www/wwwroot/go.xiachaoqing.com/jiazhangtong
chmod 644 /www/wwwroot/go.xiachaoqing.com/jiazhangtong/*.html
```

---

## 四、COS素材

**Bucket**：`art-nine-1252921383`
**Region**：`ap-beijing`
**基础URL**：`https://art-nine-1252921383.cos.ap-beijing.myqcloud.com/`
**密钥**：（已移除，请从服务器 `.env` 或腾讯云控制台获取）
```
SecretId:  [已脱敏，见服务器 /www/wwwroot/.env 或腾讯云控制台]
SecretKey: [已脱敏，见服务器 /www/wwwroot/.env 或腾讯云控制台]
```

**yingyupeipao/ 目录素材清单**：
| 文件名 | 用途 | 落地页使用位置 |
|--------|------|--------------|
| `APP重磅上线.png` | Hero主图 | Hero区右侧 |
| `C端APP宣传海报.png` | 宣传海报 | 橙色宣传区 |
| `ai对话.png` | AI功能截图 | 功能区第1卡 |
| `阅读功能.png` | 阅读功能截图 | 功能区第2卡 |
| `单词闯关.png` | 词汇功能截图 | 功能区第3卡 |
| `同步天天练.png` | 同步教材截图 | 功能区第4卡 |
| `阅读区.png` | 阅读区界面 | 官方图区右下 |
| `下载方式.png` | 下载说明图 | 下载区左下 |
| `英语陪跑go.mp4` | 产品介绍视频 | 视频区tab1 |
| `英语陪跑go快速上手使用指南.mp4` | 教程视频 | 视频区tab2 |

**待上传素材**（用户需补充）：
| 文件名 | 内容 |
|--------|------|
| `yingyupeipao/qr_download.png` | APP下载二维码（指向 https://app.lingshi.com/bjxxsy） |
| `yingyupeipao/qr_service.png` | 客服微信二维码 |

---

## 五、后端API

**服务路径**：`/www/wwwroot/wechat_platform/app/api/jiazhangtong.py`
**路由前缀**：`/api/jzt`
**服务管理**：`systemctl restart wechat-platform.service`

### API列表

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/jzt/order/create` | POST | 创建订单，返回微信H5支付链接 |
| `/api/jzt/order/notify` | POST | 微信支付回调（自动分配账号） |
| `/api/jzt/order/status?order_no=xxx` | GET | 查询支付+账号状态 |
| `/api/jzt/admin/pending` | GET | 查看待处理订单（需Header: X-Admin-Token） |
| `/api/jzt/admin/fill_account` | POST | 手动录入账号 |
| `/api/jzt/admin/add_stock` | POST | 批量预存账号库存 |
| `/api/jzt/admin/orders` | GET | 查看所有订单 |

**管理Token**：`jzt_admin_2026_change_me`（生产环境请修改）

### 数据库表

```sql
-- 订单表
jzt_orders (id, order_no, phone, grade, plan_id, plan_name, price_fen, days,
            openid, pay_status, wx_trans_id, account_id, created_at, paid_at)

-- 账号表
jzt_accounts (id, phone, jzt_account, jzt_password, expire_at,
              status, order_no, remark, created_at, updated_at)
-- status: 0=待处理, 1=已激活分配, 2=库存待分配
```

### 账号分配逻辑

```
用户支付成功 → 微信回调触发
  ↓
查 jzt_accounts 有无 status=2 的库存账号
  ↓ 有库存                      ↓ 无库存
自动分配给用户                  插入status=0的待处理记录
status改为1                     → 管理员收到通知
result.html显示账号密码          → 手动调用 fill_account 接口录入
```

### 手动录入账号示例

```bash
curl -X POST https://wechat.xiachaoqing.com/api/jzt/admin/fill_account \
  -H 'Content-Type: application/json' \
  -H 'X-Admin-Token: jzt_admin_2026_change_me' \
  -d '{"order_no":"JZT20260423...", "jzt_account":"13800138000", "jzt_password":"abc123"}'
```

### 批量预存账号

```bash
curl -X POST https://wechat.xiachaoqing.com/api/jzt/admin/add_stock \
  -H 'Content-Type: application/json' \
  -H 'X-Admin-Token: jzt_admin_2026_change_me' \
  -d '[{"jzt_account":"账号1","jzt_password":"密码1"},{"jzt_account":"账号2","jzt_password":"密码2"}]'
```

---

## 六、微信支付配置

复用现有 `wechat_platform` 的支付配置：

```python
APPID      = 'wx10b4ccec486e7961'
MCH_ID     = '1631517893'
API_KEY    = 'A7kP9xM2Qd4Zt8Bv1Ny6Hr3Ls5Wc0JuE'
NOTIFY_URL = 'https://wechat.xiachaoqing.com/api/jzt/order/notify'
```

---

## 七、Nginx配置关键段

**文件**：`/www/server/panel/vhost/nginx/go.xiachaoqing.com.conf`

```nginx
# 家长通/英语陪跑GO落地页 - 静态HTML
location ^~ /jiazhangtong {
    index index.html;
    try_files $uri $uri/index.html =404;
}
```

---

## 八、待完成事项

- [ ] 上传 `qr_download.png`（APP下载二维码）到COS
- [ ] 上传 `qr_service.png`（客服微信二维码）到COS
- [ ] 修改管理员Token（`JZT_ADMIN_TOKEN` 环境变量）
- [ ] 预存账号到库存（向供应商购买账号后调用 add_stock）
- [ ] 测试完整购买流程（小额测试）
- [ ] 在 go.xiachaoqing.com 首页加落地页入口Banner
- [ ] C端宣传海报底部填写机构名称和二维码（供线下推广）

---

## 九、相关文档

- `epgo/docs/DEV_GUIDE_v2.md` — epgo开发指南
- `openclaw_file/docs/10-公众号后端架构.md` — 微信后端架构
- `openclaw_file/wechat_platform_patch/app/api/jiazhangtong.py` — 后端API源码
