# epgo 日常维护脚本使用指南

## 📋 概况

原有两个日常脚本已整合为一个统一的维护脚本：

| 旧脚本 | 运行时间 | 功能 |
|-------|--------|------|
| daily_generate_articles_epgo.sh | 08:00 | 插入文章 |
| daily_update_epgo.py | 03:15 | 插入文章 |

**新脚本：`daily_maintain_epgo.py`**
- 运行时间：每天 02:00（建议）
- 功能：整合所有日常维护任务
- 优势：
  - ✅ 避免重复插入
  - ✅ 随机化时间戳（更真实）
  - ✅ 自动清理缓存
  - ✅ 支持所有栏目（包括106、107）
  - ✅ 数据去重检查
  - ✅ 详细的日志记录

---

## 🚀 快速开始

### 1. 部署新脚本

```bash
# 复制到服务器
scp scripts/daily_maintain_epgo.py epgo:/www/wwwroot/go.xiachaoqing.com/scripts/

# 或 rsync
rsync -av scripts/daily_maintain_epgo.py epgo:/www/wwwroot/go.xiachaoqing.com/scripts/

# 给予执行权限
ssh epgo 'chmod +x /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py'
```

### 2. 配置 cron（二选一）

**选项A：替换现有两个 cron 任务（推荐）**

```bash
# 登录服务器
ssh epgo

# 编辑 crontab
crontab -e

# 删除这两行：
# 0 8 * * * /usr/local/bin/daily_generate_articles_epgo.sh >> /var/log/epgo_article_gen.log 2>&1
# 15 3 * * * /usr/bin/python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_update_epgo.py >> ...

# 添加这一行：
0 2 * * * /usr/bin/python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py >> /www/wwwroot/go.xiachaoqing.com/logs/daily_maintain.log 2>&1
```

**选项B：保留现有任务，额外添加新脚本**

```bash
# 同时保留两个旧脚本，但调整新脚本到不同时间
0 2 * * * /usr/bin/python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py
```

### 3. 创建日志目录

```bash
ssh epgo 'mkdir -p /www/wwwroot/go.xiachaoqing.com/logs && chmod 777 /www/wwwroot/go.xiachaoqing.com/logs'
```

### 4. 测试运行

```bash
# 本地测试
python3 scripts/daily_maintain_epgo.py

# 或在服务器上测试
ssh epgo 'python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py'
```

---

## 📊 脚本功能详解

### 每天做什么？

1. **为每个栏目插入一篇新文章**
   - 根据日期轮转主题（循环利用话题库）
   - 避免插入重复文章（title + class1/class2 去重）
   - 随机化时间戳（7-30天前）
   - 随机化阅读数（10000-50000）

2. **支持的栏目**
   - 103 英语阅读 ✓
   - 104 英语演讲 ✓
   - 105 每日英语 ✓
   - 106 资料下载 ✓（新增支持）
   - 107 关于我们 ✓（新增支持）
   - 111-114 KET 各类 ✓
   - 121-124 PET 各类 ✓

3. **自动清理缓存**
   - 清理 MetInfo 编译缓存
   - 清理模板缓存
   - 使新文章立即生效

4. **生成详细日志**
   - 成功/失败记录
   - 插入数量统计
   - 错误诊断信息

### 话题库

每个栏目有 2-3 个轮转话题，按日期循环：

```
Day 1 -> Topic 1
Day 2 -> Topic 2
Day 3 -> Topic 3
Day 4 -> Topic 1 (repeat)
...
```

这确保每月内容多样，且不会重复太快。

---

## 📝 日志查看

```bash
# 实时查看日志
ssh epgo 'tail -f /www/wwwroot/go.xiachaoqing.com/logs/daily_maintain.log'

# 查看最近10条记录
ssh epgo 'tail -n 10 /www/wwwroot/go.xiachaoqing.com/logs/daily_maintain.log'

# 按日期搜索
ssh epgo 'grep "2026-03-28" /www/wwwroot/go.xiachaoqing.com/logs/daily_maintain.log'
```

### 日志示例

```
[2026-03-28 02:00:01] INFO: ============================================================
[2026-03-28 02:00:01] INFO: 开始 epgo 日常维护
[2026-03-28 02:00:01] INFO: ============================================================
[2026-03-28 02:00:02] INFO: ✓ 插入 [103] 英语阅读技巧：校园生活主题短文精读
[2026-03-28 02:00:02] INFO: ✓ 插入 [104] 英语演讲表达：校园话题开场白训练
[2026-03-28 02:00:02] INFO: ⊘ 跳过 [105] 每日英语 | 今日表达：描述计划与安排（已存在）
[2026-03-28 02:00:03] INFO: ✓ 插入 [106] KET/PET历年真题集合下载指南
[2026-03-28 02:00:03] INFO: ✓ 插入 [107] 英语陪跑GO平台简介与使用指南
[2026-03-28 02:00:04] INFO: 缓存已清理
[2026-03-28 02:00:04] INFO: ============================================================
[2026-03-28 02:00:04] INFO: 新增: 8 篇 | 跳过: 2 篇 | 总计: 371 篇 | 今日: 2 篇
[2026-03-28 02:00:04] INFO: ============================================================
```

---

## ⚙️ 配置调整

### 改变运行时间

在 crontab 中修改时间字段：

```bash
# 改为每天 23:00 运行
0 23 * * * /usr/bin/python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py
```

### 修改话题库

编辑 `daily_maintain_epgo.py` 中的 `ARTICLE_TOPICS` 字典，添加新话题：

```python
103: [  # 英语阅读
    ("新话题标题", "新话题描述"),
    ("另一个话题", "描述信息"),
],
```

### 调整时间戳范围

改变 `get_random_timestamp()` 函数中的 `days_back` 范围：

```python
# 当前：7-30天前
days_back = random.randint(7, 30)

# 改为 30-90 天前
days_back = random.randint(30, 90)
```

---

## 🔧 故障排查

### 问题1：脚本不执行

```bash
# 检查 crontab 是否正确配置
crontab -l | grep daily_maintain

# 检查 Python 路径
which python3

# 测试手动执行
python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py
```

### 问题2：文章未插入

```bash
# 查看日志中的错误信息
tail -f /www/wwwroot/go.xiachaoqing.com/logs/daily_maintain.log

# 检查数据库连接
mysql -h 127.0.0.1 -u xiachaoqing -p***REMOVED*** epgo_db -e "SELECT COUNT(*) FROM ep_news;"
```

### 问题3：重复数据

```bash
# 查看重复文章
mysql -h 127.0.0.1 -u xiachaoqing -p***REMOVED*** epgo_db -e "
SELECT title, COUNT(*) cnt FROM ep_news GROUP BY title HAVING cnt > 1;
"

# 删除重复数据（保留最新）
mysql -h 127.0.0.1 -u xiachaoqing -p***REMOVED*** epgo_db -e "
DELETE FROM ep_news
WHERE id NOT IN (
  SELECT MAX(id) FROM ep_news GROUP BY title, class1, class2
);
"
```

---

## 📈 性能指标

运行时间：< 5 秒
数据库连接：1
缓存清理：< 2 秒
日志大小：~ 500 bytes/day

---

## 🗑️ 清理旧脚本（可选）

如果完全迁移到新脚本，可以删除旧脚本：

```bash
# 在服务器上
rm /usr/local/bin/daily_generate_articles_epgo.sh
rm /www/wwwroot/go.xiachaoqing.com/scripts/daily_update_epgo.py

# 删除旧日志
rm /var/log/epgo_article_gen.log
```

---

## 💾 备份

建议定期备份脚本文件和数据库：

```bash
# 备份脚本
cp daily_maintain_epgo.py daily_maintain_epgo_backup_$(date +%Y%m%d).py

# 备份数据库
mysqldump -h 127.0.0.1 -u xiachaoqing -p***REMOVED*** epgo_db > epgo_db_backup_$(date +%Y%m%d).sql
```

