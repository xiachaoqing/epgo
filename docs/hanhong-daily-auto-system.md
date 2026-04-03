# hanhong 网站 - 每日自动文章生成系统配置说明

## 🎯 系统概述

一个**完全自动化的文章生成系统**，每天早上 8 点自动生成 3-5 篇高质量原创文章，无需人工干预。

## ✅ 已完成的配置

### 1. 脚本位置
- **本地项目**: `/Users/xiachaoqing/projects/epgo/scripts/daily_generate_articles.sh`
- **服务器**: `/usr/local/bin/daily_generate_articles.sh`
- **状态**: ✅ 已上传并设置为可执行

### 2. 定时任务配置
```bash
# 每天早上 8:00 执行
0 8 * * * /usr/local/bin/daily_generate_articles.sh >> /var/log/hanhong_article_gen.log 2>&1
```

### 3. 日志文件
- **位置**: `/var/log/hanhong_article_gen.log`
- **用途**: 记录每次执行的详细信息
- **查看**: `ssh root@101.42.21.191 "tail -100 /var/log/hanhong_article_gen.log"`

---

## 📊 工作原理

### 每日生成策略
系统根据**当前日期**自动选择文章主题组合，循环生成不同类型内容：

| 日期尾号 | 文章主题 | 数量 |
|----------|--------|------|
| 0 | 产品系列（MR-707/807/808） | 3篇 |
| 1 | 行业应用（石油、纺织、食品） | 3篇 |
| 2 | 技术知识（绝缘、谐波、三相） | 3篇 |
| 3 | FAQ和常见问题 | 3篇 |
| 4 | 成本和ROI分析 | 3篇 |
| 5 | 数字化和智能化 | 3篇 |
| 6 | 用户成功故事 | 3篇 |
| 7 | 产品对比 | 3篇 |
| 8 | 维护和最佳实践 | 3篇 |
| 9 | 教育和培训 | 3篇 |

**结果**: 每10天完整循环一遍所有主题，确保内容多样性

### 生成流程
```
每天 8:00 触发
    ↓
根据日期计算文章主题组合
    ↓
逐篇插入数据库
    ↓
生成日志记录
    ↓
完成
```

---

## 🚀 快速操作指南

### 查看今天的文章生成情况
```bash
ssh root@101.42.21.191 "tail -20 /var/log/hanhong_article_gen.log"
```

### 手动执行一次脚本
```bash
ssh root@101.42.21.191 "/usr/local/bin/daily_generate_articles.sh"
```

### 查看最新生成的文章
```bash
ssh root@101.42.21.191 "mysql -uhanhong -p07090218 hanhong -e \
  \"SELECT id, title, DATE(addtime) FROM hh_news WHERE lang='cn' ORDER BY id DESC LIMIT 10;\" 2>/dev/null"
```

### 查看文章统计
```bash
ssh root@101.42.21.191 "mysql -uhanhong -p07090218 hanhong -e \
  \"SELECT COUNT(*) as 总数 FROM hh_news WHERE lang='cn';
   SELECT COUNT(*) as 今日新增 FROM hh_news WHERE lang='cn' AND DATE(addtime)=CURDATE();\" 2>/dev/null"
```

### 查看定时任务状态
```bash
ssh root@101.42.21.191 "crontab -l"
```

---

## 📈 预期效果

### 数据增长趋势
| 时间 | 文章数 | 增长 |
|------|-------|------|
| 初始 | 12篇 | - |
| 第1天 | 45篇 | +33篇 |
| 第10天 | 75篇 | +30篇 |
| 第30天 | 135篇 | +90篇 |
| 第90天 | 315篇 | +180篇 |
| 第180天 | 585篇 | +270篇 |

### 对Google AdSense的长期影响

**第1-2周**:
- Google爬虫发现新文章
- 索引速度加快
- 网站权重提升

**第2-4周**:
- 新文章收录完成
- 流量开始增加
- AdSense批准概率提升

**第1-3个月**:
- 自然搜索流量明显增加
- AdSense广告收入稳定增长
- 网站权威性建立

---

## 🔧 维护和调整

### 如果需要修改生成计划

1. **编辑脚本**:
   ```bash
   nano /usr/local/bin/daily_generate_articles.sh
   ```

2. **修改生成时间**:
   改变 `generate_daily_articles()` 中的 `case` 条件

3. **修改执行时间**:
   ```bash
   # 例：改为每天晚上 18:00 执行
   0 18 * * * /usr/local/bin/daily_generate_articles.sh >> /var/log/hanhong_article_gen.log 2>&1
   ```

4. **更新 crontab**:
   ```bash
   ssh root@101.42.21.191 "echo '0 18 * * * /usr/local/bin/daily_generate_articles.sh >> /var/log/hanhong_article_gen.log 2>&1' | crontab -"
   ```

### 故障排查

**问题**: 脚本没有执行
- 检查: `ssh root@101.42.21.191 "crontab -l"`
- 检查: `ssh root@101.42.21.191 "ls -la /usr/local/bin/daily_generate_articles.sh"`

**问题**: 数据库连接失败
- 检查MySQL服务: `ssh root@101.42.21.191 "systemctl status mysql"`
- 检查凭证: 用户名/密码/主机是否正确

**问题**: 脚本执行但没有生成文章
- 检查日志: `tail -50 /var/log/hanhong_article_gen.log`
- 检查SQL语句是否有错误

---

## 📝 脚本特性

### ✅ 自动化功能
- ✓ 每天自动执行，无需人工干预
- ✓ 智能选择文章主题，确保多样性
- ✓ 自动记录执行日志
- ✓ 完整的错误处理

### ✅ 可靠性
- ✓ 与 MySQL 的持久连接
- ✓ 执行失败自动记录
- ✓ 彩色日志输出便于分析
- ✓ 完整的统计信息

### ✅ 易于维护
- ✓ 清晰的代码结构
- ✓ 易于扩展新的文章主题
- ✓ 简单的参数配置
- ✓ 完整的日志记录

---

## 💡 高级技巧

### 临时禁用自动生成
```bash
# 注释掉 crontab 任务
ssh root@101.42.21.191 "crontab -l | sed 's/^0 8 /#0 8 /' | crontab -"
```

### 恢复自动生成
```bash
ssh root@101.42.21.191 "crontab -l | sed 's/^#0 8 /0 8 /' | crontab -"
```

### 改为每 6 小时执行一次
```bash
ssh root@101.42.21.191 "echo '0 */6 * * * /usr/local/bin/daily_generate_articles.sh >> /var/log/hanhong_article_gen.log 2>&1' | crontab -"
```

### 改为每周一、三、五执行
```bash
# 周一=1, 周三=3, 周五=5
ssh root@101.42.21.191 "echo '0 8 * * 1,3,5 /usr/local/bin/daily_generate_articles.sh >> /var/log/hanhong_article_gen.log 2>&1' | crontab -"
```

---

## 📊 当前状态

### 系统配置
- ✅ 脚本已部署
- ✅ Crontab 已配置
- ✅ 日志系统就绪
- ✅ 测试执行成功

### 文章统计
- ✅ 初始: 12 篇
- ✅ 目前: 45 篇
- ✅ 日增长: 3-5 篇
- ✅ 年预计: 500+ 篇

### 预期下次执行
- ⏰ **时间**: 明天 2026-03-28 08:00
- 📊 **预计新增**: 3-5 篇

---

## 🎯 完全零维护

这个系统设计为**完全自动化**，一旦部署就无需任何人工干预。每天早上会自动生成新文章，让Google看到网站的持续更新活力。

**状态**: ✅ **已就绪，自动运行中！**

---

**创建时间**: 2026-03-27 18:30
**系统状态**: 🟢 正常运行
**下次执行**: 2026-03-28 08:00
