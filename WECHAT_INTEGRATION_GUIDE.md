# 微信公众号集成指南 - 从 openclaw_file 项目提取

## 📋 关键信息速查

### 【公众号基本信息】
```
公众号名称：英语陪跑 go
类型：已认证服务号（有完整 API 权限）
AppID：wx10b4ccec486e7961
AppSecret：已写入服务器 .env
回调地址：https://wechat.xiachaoqing.com/wechat
管理后台：https://wechat.xiachaoqing.com/admin/
```

---

## 🎛️ 自动回复规则（11条）

已完整部署，规则优先级排序：

| 规则名 | 关键词 | 优先级 | 说明 |
|--------|--------|--------|------|
| PET 资料 | PET 资料 | 10 | 最高 |
| 听力资料 | 听力 | 9 | - |
| 阅读资料 | 阅读 | 9 | - |
| 写作资料 | 写作 | 9 | - |
| 口语资料 | 口语 | 9 | - |
| 词汇资料 | 词汇 | 8 | - |
| 真题资料 | 真题 | 8 | - |
| 备考计划 | 备考计划 | 8 | - |
| 成绩查询 | 成绩 | 7 | - |
| 报名信息 | 报名 | 7 | - |
| 默认回复 | （无匹配时） | 0 | 兜底 |

**回复原理：**
- 精确匹配 / 模糊匹配 / 正则匹配
- 匹配成功后按优先级排序
- 支持文本、图文、图片、语音回复

---

## 📱 菜单配置

### 在微信公众号后台配置自定义菜单

**操作路径：**
微信公众号后台 → 自定义菜单 → 新增菜单

**菜单结构建议：**
```
├─ 首页/推荐（链接到网站）
├─ 免费学习（链接到：https://go.xiachaoqing.com）
├─ 下载 APP（链接到：https://app.lingshi.com/bjxxsy）
└─ 关于我们
```

**菜单项配置：**
- 菜单名称：最多 4 个字
- 菜单类型：页面链接 / 回复消息 / 小程序等
- URL：完整的 http/https 链接
- 优先级：从上到下显示

---

## 📊 文章发布参数

### POST /api/articles/save（发布到草稿箱）

```json
{
  "title": "PET听力5个必考技巧",        // 必填
  "content": "<p>HTML正文...</p>",     // 必填
  "author": "Cathy",                   // 作者，默认 Cathy
  "digest": "摘要...",                 // 摘要，留空自动截取
  "topic_hint": "PET听力技巧",         // 影响封面主题匹配
  "thumb_media_id": "",                // 留空=自动选封面
  "is_original": 1,                    // 1=原创声明
  "xhs_title": "小红书标题",           // 小红书标题（可选）
  "xhs_content": "小红书正文",         // 小红书正文（可选）
  "source": "ai_auto"                  // 来源标记
}
```

### 发布策略（重要！）

**微信限制：每月仅限群发 4 次**

推荐做法：
```
常规发布：POST /api/articles/{id}/publish
结果：无推送通知，节省群发次数
用户可通过搜索找到，产生自然流量

精华内容：POST /api/articles/push-multi + /publish
结果：向粉丝群发通知（每月最多 4 次）
建议：每月选 4 次精华内容群发
```

---

## 🔑 原创声明功能

### 当前支持
- 代码已支持 `is_original=1` 参数
- 默认全部声明原创

### 需要开通
微信公众号后台 → 内容管理 → 原创保护 → 申请开通

### 开通条件
- 已发表至少 3 篇原创文章
- 原创能力未被封禁

### 漫画原创
- 单独申请（需先发 3 篇漫画内容）
- 开通后可声明漫画原创

---

## 💰 流量主与收益

### 当前状态
- ✅ 已开通流量主
- 文章自动展示广告
- 阅读量越高 → 收益越高

### 收益机制
- CPM：每千次展示收益
- 基于：地区、时段、用户质量

---

## 🔧 后端架构

### 技术栈
- 前端：HTML5 + 原生 JS（无框架）
- 后端：FastAPI + Uvicorn
- 数据库：MySQL 8.0
- 进程管理：systemd

### 目录结构
```
/www/wwwroot/
├── wechat_reply/          前端静态文件
│   ├── index.html         首页
│   └── admin/index.html   管理后台
└── wechat_platform/       后端 Python 项目
    ├── app/main.py        FastAPI 入口
    ├── models/            数据模型
    ├── services/          业务逻辑
    └── .env               环境变量
```

### 数据库表
核心表：
- `we_reply_rules` - 回复规则
- `we_messages` - 消息记录
- `we_articles` - 文章记录
- 共 10 张表，统一 `we_` 前缀

---

## 🛠️ 运维命令

```bash
# 重启后端服务
ssh openclaw "systemctl restart wechat-platform"

# 查看服务状态
ssh openclaw "systemctl status wechat-platform"

# 查看日志（最后50行）
ssh openclaw "journalctl -u wechat-platform -n 50 --no-pager"

# 手动补充封面
SCRIPT="/root/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/public/article-writer/scripts/fetch_covers.py"
ssh openclaw "python3 $SCRIPT --auto-daily --count 5"
```

---

## 📝 关键点总结

### ✅ 已实现的功能
- 自动回复规则（11 条）
- 文章群发管理（考虑月度限制）
- 原创声明支持
- 流量主广告
- 后台管理系统

### 💡 推广策略建议
1. **菜单推广**
   - 添加"下载 APP"菜单
   - URL：https://app.lingshi.com/bjxxsy

2. **文章推广**
   - 在每篇文章末尾添加推广链接
   - 利用自动回复规则引导用户

3. **回复规则优化**
   - 可在自动回复中插入 APP 推广
   - 例：回复"学习"时，附带 APP 下载链接

4. **群发策略**
   - 每月 4 次群发机会
   - 建议用于重要推广内容

---

## 🔗 相关链接

- 公众号首页：https://wechat.xiachaoqing.com
- 管理后台：https://wechat.xiachaoqing.com/admin/
- epgo 网站：https://go.xiachaoqing.com
- APP 下载：https://app.lingshi.com/bjxxsy

---

## 📚 相关文档位置

- 完整微信公众号文档：`/Users/xiachaoqing/projects/openclaw_file/docs/06-微信公众号.md`
- 后端架构详解：`/Users/xiachaoqing/projects/openclaw_file/docs/10-公众号后端架构.md`

