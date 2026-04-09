# 📱 【功能文档】微信公众号系统

> 最后更新：2026-04-09 | 维护者：AI Assistant | 状态：生产环境

---

## 📋 概述

英语陪跑GO微信公众号是核心营销和用户互动平台，集文章推送、自动回复、菜单导航、APP推广等功能于一体。

---

## 🎛️ 菜单系统

### 菜单结构（21项）

#### 一级菜单（4个）

| 菜单名 | 优先级 | 功能 | 子菜单数 |
|--------|--------|------|---------|
| 备考资料 | 1 | 学习资源分类 | 5 个 |
| 学习中心 | 2 | 技能训练 | 5 个 |
| 下载APP | 2 | APP推广 | - |
| 关于我们 | 3 | 品牌信息 | 4 个 |

#### 二级菜单详情

**备考资料（5个）**
- PET资料（menu_key: PET_MATERIALS）
- KET资料（menu_key: KET_MATERIALS）
- FCE资料（menu_key: FCE_MATERIALS）
- 全套资料包（menu_key: ALL_PACK）
- 选级别指南（menu_key: LEVEL_GUIDE）

**学习中心（5个）**
- 听力（menu_key: LISTENING）
- 阅读（menu_key: READING）
- 写作（menu_key: WRITING）
- 口语（menu_key: SPEAKING）
- 单词大乱斗（view: 游戏链接）

**关于我们（4个）**
- 作者介绍（menu_key: ABOUT）
- 联系方式（menu_key: CONTACT）
- 我们的服务（menu_key: SERVICES）
- 历史文章（menu_key: HISTORY）

---

## 💬 自动回复规则系统

### 规则统计（44条）

| 优先级 | 数量 | 说明 |
|--------|------|------|
| 100 | 1 | 订阅欢迎 |
| 10 | 18 | 高优规则（PET、KET、FCE各类资料） |
| 9 | 5 | 基础资料+APP推广 ✅ |
| 8 | 2 | 备考技巧、真题解析 |
| 7 | 4 | 历史、作者、服务等 |
| 0 | 14 | 其他专题资料 |

### 规则类型

**学习资料类（优先级10-9）**
```
关键词：PET资料、听力、阅读、写作、口语、词汇、真题等
回复：详细的学习资料 + 下载链接

示例（PET资料 - 优先级10）：
"? 你好！
回复以下关键词获取对应资料：
? 词汇类：回复「PET短语」→ 高频短语100个
? 听力类：回复「PET听力」→ 听力备考资料
..."
```

**APP推广规则（优先级9）✅ 新增**
```
关键词：APP、下载、应用
匹配方式：模糊匹配
优先级：9
回复内容：完整的APP介绍 + 下载链接

示例：
"英语陪跑GO APP
核心特性：系统课程、真人讲解、在线练习、学习追踪、随时随地
立即下载：https://app.lingshi.com/bjxxsy
支持iOS和Android"
```

**其他规则（优先级0-8）**
```
- 备考技巧：学习方法、高分秘诀
- 真题解析：过去的真题讲解
- 历史消息：查看往期文章
- 作者介绍：品牌信息
- 联系方式：获取联系渠道
- 服务介绍：课程和服务信息
```

### 规则匹配机制

```
用户消息 → 规则引擎
  ↓
按优先级排序（最高100 → 最低0）
  ↓
依次尝试匹配：
  - 精确匹配
  - 模糊匹配
  - 正则匹配
  ↓
首个匹配成功 → 返回回复内容
  ↓
无匹配 → 返回默认回复
```

---

## 📊 功能数据

### 菜单数据库结构（we_menus表）

```sql
id              - 菜单ID
parent_id       - 父菜单ID（0=一级菜单）
menu_name       - 菜单名称
menu_type       - 菜单类型（click=点击 / view=链接）
menu_key        - 菜单标识键
menu_url        - 链接URL（view类型时使用）
sort_order      - 排序顺序
is_active       - 是否启用（1=启用 / 0=禁用）
```

### 回复规则数据库结构（we_reply_rules表）

```sql
id              - 规则ID
rule_name       - 规则名称
keyword         - 触发关键词
reply_content   - 回复内容
reply_type      - 回复类型（1=文本 / 2=图文 / 3=图片 / 4=语音）
match_type      - 匹配类型（1=精确 / 2=模糊 / 3=正则）
priority        - 优先级（0-100，越大越先匹配）
is_active       - 是否启用
hit_count       - 累计命中次数
last_hit_at     - 最后命中时间
```

---

## 📱 APP推广集成（2026-04-09新增）

### 推广入口

#### 1️⃣ 菜单入口
- **位置**：一级菜单第3个
- **显示**：用户打开公众号即可看到
- **链接**：https://app.lingshi.com/bjxxsy

#### 2️⃣ 搜索入口
- **触发词**：APP、下载、应用
- **优先级**：9（仅次于最高优先级10）
- **回复**：完整APP介绍 + 下载链接

#### 3️⃣ 资料推广（待优化）
- **计划**：在18条高优规则末尾追加APP推广
- **目标**：用户获取任何资料时同时看到APP推广

---

## 🔧 技术信息

### 后端架构

```
微信服务器
    ↓ (消息推送/回调)
Nginx (wechat.xiachaoqing.com)
    ↓ (路由分流)
    ├─ /admin/*       → 静态后台
    ├─ /api/*         → FastAPI
    └─ /wechat        → FastAPI回调处理
        ↓
    FastAPI (127.0.0.1:8000)
        ├─ 消息解析 (AES解密)
        ├─ 规则匹配
        └─ 数据库查询 (MySQL)
            ↓
        wechat_platform (MySQL数据库)
            ├─ we_menus         (菜单表)
            ├─ we_reply_rules   (规则表)
            ├─ we_messages      (消息记录表)
            └─ 其他7张表
```

### 服务管理

```bash
# 重启服务
ssh openclaw "systemctl restart wechat-platform"

# 查看服务状态
ssh openclaw "systemctl status wechat-platform"

# 查看日志
ssh openclaw "journalctl -u wechat-platform -n 50 --no-pager"
```

---

## 📝 维护清单

### 日常检查

- [ ] 菜单是否正常显示
- [ ] 回复规则是否有效
- [ ] 后端服务是否运行
- [ ] 数据库连接是否正常

### 定期维护

- [ ] 检查规则命中率（hit_count）
- [ ] 清理过期消息记录
- [ ] 更新规则回复内容
- [ ] 备份数据库

### 故障排查

```bash
# 1. 检查菜单是否已发布
ssh openclaw "mysql ... SELECT * FROM we_menus WHERE is_active=1"

# 2. 检查回复规则是否启用
ssh openclaw "mysql ... SELECT * FROM we_reply_rules WHERE is_active=1"

# 3. 查看服务日志
ssh openclaw "journalctl -u wechat-platform -n 100 --no-pager"

# 4. 测试消息回复
# 在微信公众号发送测试消息，检查是否收到回复
```

---

## 📅 更新历史

| 日期 | 内容 | 项目ID |
|------|------|--------|
| 2026-04-09 | 添加APP推广菜单和规则 | 20260409-wechat-promotion |
| - | 基础菜单和规则系统 | - |

---

## 🔗 相关资源

- **项目文档**：docs/projects/20260409-wechat-promotion.md
- **配置文件**：.env（已配置AppID/AppSecret）
- **后端代码**：/www/wwwroot/wechat_platform/app/
- **前端后台**：/www/wwwroot/wechat_reply/admin/

