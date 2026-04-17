# Google AdSense 修复 - 快速参考卡片

## 🎯 项目一句话总结

用3个脚本将436篇低质量文章中的343篇改写为高质量，成本¥0.9，耗时2-3小时，目标Google AdSense通过。

---

## 📊 现状 vs 目标

```
当前状态:
  ❌ AdSense: 低价值内容警告
  ❌ 高质量文章: 仅16.5%
  ❌ 重复内容: 120篇 (27.5%)
  ❌ 模板化: 111篇 (25.5%)
  ❌ 过短: 112篇 (25.7%)

改写后:
  ✅ AdSense: 预期通过审核
  ✅ 高质量文章: 95%+
  ✅ 重复内容: 0篇
  ✅ 模板化: 0篇
  ✅ 过短: 0篇
```

---

## 🚀 立即行动（3步）

### Step 1: 测试脚本 (5分钟)
```bash
ssh root@101.42.21.191
cd /www/wwwroot/go.xiachaoqing.com

# 不改DB，只看看会改写什么
python3 scripts/rewrite_batch_articles.py --round=1 --batch-size=10 --dry-run
```

### Step 2: 执行改写 (2-3小时)
```bash
# 快速版：3轮并行运行，总耗时2小时
python3 scripts/rewrite_batch_articles.py --round=1 --parallel=4 &
sleep 60
python3 scripts/rewrite_batch_articles.py --round=2 --parallel=4 &
sleep 60
python3 scripts/rewrite_batch_articles.py --round=3 --parallel=4 &
```

### Step 3: 验证和提交 (1小时)
```bash
# 查看改写统计
mysql -uxiachaoqing -p'Xia@07090218' epgo_db -e "
SELECT issue, COUNT(*) FROM ep_news WHERE recycle=0 GROUP BY issue;
"

# 生成质量报告
python3 scripts/quality_monitor.py

# 提交到Git
git add . && git commit -m "refactor: AdSense compliance - 343 articles rewritten"
```

---

## 📁 关键文件

| 文件 | 用途 | 执行方式 |
|------|------|---------|
| `EXECUTION_GUIDE.md` | 📖 详细执行手册（中文） | 📖 阅读 |
| `ADSENSE_FIX_PLAN.md` | 🔍 技术细节和方案 | 🔍 参考 |
| `rewrite_batch_articles.py` | ⚙️ 改写脚本（一次性） | ⚡ 执行 |
| `quality_monitor.py` | 📊 质量监测（周期） | 📊 执行 |
| `PROJECT_SUMMARY.md` | 📋 完整项目总结 | 📋 存档 |

---

## ⏱️ 时间表

```
第1天 (1小时):   前端优化 + 测试脚本
第2天 (2小时):   改写第1轮（重复）
第2天 (2小时):   改写第2轮（模板）
第2天 (2小时):   改写第3轮（过短）- 可并行
第3天 (1小时):   验证和提交到Google
第4天-第17天:    等待Google审核（7-14天）
第18天 ✓:       AdSense批准 🎉
```

**加速方案**: 用`--parallel=4`可将第2天耗时从6小时压到2小时

---

## 💰 成本

```
LLM API调用（3轮，343篇文章）: ¥0.9
总成本: ¥0.9 ✓ 超便宜
```

---

## 🔧 常见命令

### 改写脚本
```bash
# 串行版（安全但慢）
python3 rewrite_batch_articles.py --round=1

# 并行版（快速）
python3 rewrite_batch_articles.py --round=1 --parallel=4

# 测试模式（不改DB）
python3 rewrite_batch_articles.py --round=1 --dry-run

# 断点续传（从ID 250继续）
python3 rewrite_batch_articles.py --round=2 --resume-from-id=250
```

### 监测
```bash
# 查看改写进度
tail -50 /logs/rewrite_batch_*.log

# 查看改写统计
mysql -uxiachaoqing -p'Xia@07090218' epgo_db -B -N -e "
SELECT issue, COUNT(*) as cnt FROM ep_news WHERE recycle=0 GROUP BY issue;
"

# 生成质量报告
python3 scripts/quality_monitor.py
cat /docs/quality_reports/quality_report_*.md
```

---

## ⚠️ 重点提醒

1. ✅ **保留URL和标题** - SEO不受影响
2. ✅ **标记为rewrite-v1** - 便于追踪
3. ✅ **详细日志记录** - 便于审查和回滚
4. ✅ **支持并行加速** - 快速完成改写
5. ✅ **自动质量检验** - 不会入库垃圾内容

---

## 🆘 出问题了？

| 症状 | 原因 | 解决 |
|------|------|------|
| `invalid_api_key` | API Key错误 | 检查 sk-63851... |
| `Timeout` | 网络太慢 | 重试或减少batch_size |
| 内容质量差 | LLM生成不好 | 提升quality_threshold或回滚 |
| DB未更新 | 脚本失败 | 查看日志，从断点续传 |

详见 `EXECUTION_GUIDE.md` 的"常见问题"部分

---

## 📞 完整文档导航

```
快速开始:
  └─ 本文件 (30秒快速理解)

详细执行:
  └─ EXECUTION_GUIDE.md (中文，分步操作)

技术深入:
  └─ ADSENSE_FIX_PLAN.md (英文，方案和原理)

项目档案:
  └─ PROJECT_SUMMARY.md (完整总结)
```

---

## ✨ 预期成果

```
✓ 第1周:  前端符合AdSense政策
✓ 第2周:  343篇文章改写完成
✓ 第1月:  Google AdSense批准 🎉
✓ 第2月:  低价值警告消失
✓ 第3月+: 开始投放广告，产生收入
```

---

**版本**: 1.0
**创建日期**: 2026-04-16
**最后更新**: 2026-04-16
**状态**: ✅ 准备好了，可以开始执行
