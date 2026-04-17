# Google AdSense 低价值内容修复完整方案

**文档日期**: 2026-04-16
**状态**: 执行中
**目标**: 从"低价值内容"警告 → Google AdSense 批准并优化收益

---

## 一、问题诊断

### 当前状态

| 项目 | 数据 | 严重性 |
|------|------|--------|
| 总文章数 | 436篇 | - |
| 高质量(>4000字) | 72篇 (16.5%) | ✓ 优秀 |
| 模板水文 | 111篇 (25.5%) | 🔴 致命 |
| 内容过短(<2000字) | 112篇 (25.7%) | 🔴 致命 |
| 内容重复 | 120篇 (27.5%) | 🔴 最严重 |
| 需要改写 | ~300篇 | - |

### Google判定低价值的根本原因

1. **内容重复** (27.5%) - Google最痛恨，会大幅降权
2. **模板化** (25.5%) - 无实际价值，用户停留时间短
3. **太短** (25.7%) - 没有足够信息量，不满足E-E-A-T标准
4. **综合质量低** - 高质量内容只占16.5%

---

## 二、改写方案（一次性 + 持续维护脚本）

### 2.1 脚本分类

| 脚本 | 类型 | 频率 | 用途 |
|------|------|------|------|
| `rewrite_batch_articles.py` | **一次性** | 运行一次 | 改写现有300篇低质量文章 |
| `daily_maintain_epgo.py` | **长期** | 每天凌晨2点 | 生成新文章（已优化） |
| `quality_monitor.py` | **监测** | 每周运行 | 监测文章质量，预警低质量 |

### 2.2 一次性改写脚本工作流

```
rewrite_batch_articles.py
├─ 识别低质量文章（复制+过短+模板）
├─ 按优先级排序（重复>模板>过短）
├─ 分批处理（每批20篇，间隔30秒）
├─ 调用通义千问API改写
├─ 保留原标题/URL/ID
├─ 替换content和description
├─ 验证格式（HTML标签）
├─ 记录日志（便于审查和回滚）
├─ 数据库更新
├─ Git提交变更日志
└─ 成本监控
```

### 2.3 改写策略

**保留内容**:
- `id` - URL不变
- `title` - SEO排名不受影响
- `class1/class2` - 栏目分类
- `hits` - 阅读数（保真）
- `addtime` - 发布时间（保真）

**改写内容**:
- `content` - 替换成高质量1500-2000字内容
- `description` - 替换成独立50-80字摘要
- `issue` - 标记为 `rewrite-v1`

**质量标准**:
- ✅ 每篇 1500-2500 字节（改写后）
- ✅ 包含具体例句和代码/步骤
- ✅ 结构清晰（h2小标题+p段落）
- ✅ 有实际教学价值
- ✅ description ≠ title

---

## 三、前端模板优化（Google AdSense要求）

### 3.1 当前问题

| 问题 | 位置 | AdSense影响 |
|------|------|-----------|
| 缺少隐私政策链接 | footer | 🔴 必需 |
| 缺少条款页面 | footer | 🔴 必需 |
| 缺少关于页面 | header | 🟡 推荐 |
| 广告配置缺失 | head | 🔴 必需 |
| 页面速度未优化 | - | 🟡 推荐 |

### 3.2 必需页面

```
/privacy/           (隐私政策)
/terms/            (服务条款)
/about/            (关于我们) - 已有
/contact/          (联系我们) - 已有
```

### 3.3 AdSense必需的HTML标签

```html
<!-- 在 head.php 中添加 -->
<meta name="google-site-verification" content="your_code_here" />
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_CODE"></script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="页面描述">
```

### 3.4 Footer优化

需要在footer中添加：
```
隐私政策 | 服务条款 | 联系我们 | 关于我们 | 广告合作
```

---

## 四、执行流程（分阶段）

### 阶段1：前端准备（今天）
- [ ] 创建/优化隐私政策页面
- [ ] 创建/优化服务条款页面
- [ ] 更新footer导航链接
- [ ] 添加AdSense验证代码
- [ ] 提交到git

**预计时间**: 1小时
**涉及文件**:
- `templates/epgo-education/privacy.php` (新建)
- `templates/epgo-education/terms.php` (新建)
- `templates/epgo-education/foot.php` (修改)
- `templates/epgo-education/head.php` (修改)

### 阶段2：文章改写（最关键，需要几轮）

**第一轮**: 改写120篇重复内容
```
- 预计时间: 2-3小时
- 文件: scripts/rewrite_batch_articles_round1.py
- API调用: 120次
- 成本: ~0.3元
```

**第二轮**: 改写111篇模板化文章
```
- 预计时间: 2-3小时
- 文件: scripts/rewrite_batch_articles_round2.py
- API调用: 111次
- 成本: ~0.3元
```

**第三轮**: 改写112篇过短文章
```
- 预计时间: 2-3小时
- 文件: scripts/rewrite_batch_articles_round3.py
- API调用: 112次
- 成本: ~0.3元
```

**总耗时**: ~6-9小时（可并行多进程加速）
**总成本**: ~0.9元
**并行化**: 可用多进程将耗时降低到 2-3小时

### 阶段3：验证和微调（1小时）
- [ ] 随机抽查50篇改写文章
- [ ] 检查HTML格式
- [ ] 检查内容是否重复（新的）
- [ ] 检查description是否和title重复
- [ ] 检查字数是否符合标准

### 阶段4：提交到Google
- [ ] 验证所有必需页面（隐私政策等）
- [ ] robots.txt配置检查
- [ ] sitemap提交
- [ ] Google Search Console验证
- [ ] 重新提交AdSense审核

---

## 五、脚本清单

### 脚本1: `rewrite_batch_articles.py` （一次性）

**功能**:
- 查询所有低质量文章
- 优先级排序
- 分批调用LLM改写
- 格式验证
- DB更新
- 日志记录

**参数**:
```python
BATCH_SIZE = 20          # 每批改写数量
BATCH_INTERVAL = 30      # 批次间隔(秒)
MIN_CONTENT_LEN = 4000   # 改写后最小字节数
QUALITY_THRESHOLD = 6    # 质量评分阈值(1-10)
```

**运行命令**:
```bash
python3 /www/wwwroot/go.xiachaoqing.com/scripts/rewrite_batch_articles.py --round=1 --api-key=sk-xxx
```

**输出**:
- 改写成功: ✓ 20篇
- 改写失败: ✗ 1篇（含原因）
- 验证不通过: ⚠ 2篇（未入库）
- 总耗时: 3分45秒
- API成本: ¥0.05

### 脚本2: `quality_monitor.py` （长期，周运行）

**功能**:
- 每周扫描新生成的文章
- 检测字数/重复/模板
- 自动标记低质量
- 生成质量报告
- Slack/邮件通知

**运行**:
```bash
0 0 * * 0 python3 /www/wwwroot/go.xiachaoqing.com/scripts/quality_monitor.py
```

---

## 六、文档和Git同步

### 6.1 文档更新

所有改动同步到git：

```
docs/
├── ADSENSE_FIX_PLAN.md          ← 此文档
├── REWRITE_LOG_ROUND1.md        ← 第一轮改写日志
├── REWRITE_LOG_ROUND2.md        ← 第二轮改写日志
├── REWRITE_LOG_ROUND3.md        ← 第三轮改写日志
└── QUALITY_AUDIT_REPORT.md      ← 最终审计报告
```

### 6.2 Git提交规范

**一次性改写阶段**:
```
commit: "fix: rewrite 120 duplicate articles for AdSense (round 1)"
- 替换120篇重复内容文章
- 保留标题和URL
- 标记为 issue='rewrite-v1'
- 所有文章已通过质量检查

commit: "fix: rewrite 111 template articles for AdSense (round 2)"
...

commit: "docs: update REWRITE_LOG_ROUND*.md with results"
- Round 1: 120/120 成功，0 失败
- Round 2: 111/111 成功，0 失败
- Round 3: 112/112 成功，0 失败
- 总计: 343/343 成功
```

**前端优化阶段**:
```
commit: "feat: add privacy and terms pages for AdSense compliance"
- 新增 /privacy/ 页面
- 新增 /terms/ 页面
- 更新 footer 导航链接
- 符合 Google AdSense 政策

commit: "feat: add AdSense verification meta tags"
- 添加 Google Site Verification
- 添加 AdSense script 标签
```

---

## 七、改写文章格式规范

### 7.1 HTML结构（必须严格遵守）

```html
<h2>小标题1</h2>
<p>段落内容（150-300字）。包含具体例句或方法。</p>
<ul>
  <li>要点1</li>
  <li>要点2</li>
</ul>

<h2>小标题2</h2>
<p>段落内容。可包含<strong>加粗</strong>或<em>斜体</em>。</p>

<blockquote>
<p>引用内容（来自权威来源）</p>
</blockquote>
```

### 7.2 禁止事项

❌ 不要用 `<h1>` （页面标题已是h1）
❌ 不要使用 `<table>` （除非必要，可用列表替代）
❌ 不要使用 Markdown（必须是HTML）
❌ 不要使用外部iframe
❌ 不要有大段空白或重复段落

### 7.3 必需元素

✅ 至少3个 `<h2>` 小标题
✅ 每个小标题下至少2-3个段落
✅ 包含至少2个具体例句或代码示例
✅ 结尾段要有总结
✅ 总字数 1500-2500 字节

---

## 八、质量检查清单（改写后需验证）

### 每篇文章改写后必须检查：

- [ ] 标题和URL保持不变
- [ ] Content字节数 ≥ 4000 （HTML）
- [ ] Description长度 50-80字，不等于标题
- [ ] 无HTML格式错误（用BeautifulSoup验证）
- [ ] 无明显重复内容（MD5哈希检查）
- [ ] 包含至少2个 `<h2>` 标题
- [ ] 无外链或不当链接
- [ ] 格式符合规范（无Markdown残留）

---

## 九、成本估算和时间表

| 阶段 | 任务 | 时间 | 成本 | 优先级 |
|------|------|------|------|--------|
| 1 | 前端优化（隐私政策等） | 1小时 | 0元 | 🔴 必需 |
| 2 | 改写120篇重复内容 | 2-3小时 | ¥0.3 | 🔴 最严重 |
| 3 | 改写111篇模板文章 | 2-3小时 | ¥0.3 | 🔴 严重 |
| 4 | 改写112篇过短文章 | 2-3小时 | ¥0.3 | 🟡 严重 |
| 5 | 验证和微调 | 1小时 | 0元 | ✓ 必需 |
| 6 | 文档和Git提交 | 30分钟 | 0元 | ✓ 必需 |
| **总计** | - | **8.5-10小时** | **¥0.9** | - |

**使用并行化后**: 耗时可降低到 3-4小时

---

## 十、AdSense审核通过后的持续维护

### 每日维护（已由脚本自动执行）
```
- daily_maintain_epgo.py: 生成12篇高质量文章
- 每篇 1500-2000 字，quality_score ≥ 8/10
```

### 每周监测（新增脚本）
```
- quality_monitor.py: 扫描所有文章，预警低质量
- 自动生成质量报告
```

### 每月审计
```
- 与Google AdSense数据对比
- 检查低价值内容警告是否减少
- 优化广告位置和格式
```

---

## 十一、风险和应急方案

### 风险1: API限流或超时
**症状**: 某轮改写中途失败
**应急方案**:
- 脚本内置断点续传（记录最后成功ID）
- 可从任意轮次重新开始
- 示例: `python3 rewrite_batch.py --round=2 --resume-from-id=150`

### 风险2: 改写内容质量不满足要求
**症状**: 随机抽查发现内容过短或重复
**应急方案**:
- 触发自动回滚：`git revert <commit-hash>`
- 调整LLM prompt并重新运行
- 提升 `QUALITY_THRESHOLD` 参数

### 风险3: 改写后仍被标记为低价值
**症状**: 提交给Google后仍收到警告
**应急方案**:
- 检查是否有新的低质量文章生成
- 增加高质量文章的发布频率
- 审查Google的具体反馈并微调

---

## 十二、成功标志

✅ **第1周**: 前端符合AdSense政策，隐私政策/条款页面完成
✅ **第2周**: 300篇文章改写完成，所有格式验证通过
✅ **第1个月**: Google AdSense 批准，收到审核通过通知
✅ **第2个月**: 低价值内容警告消失，可投放广告

---

## 附录：脚本命令参考

```bash
# 改写第一轮（重复内容）
python3 scripts/rewrite_batch_articles.py \
  --round=1 \
  --batch-size=20 \
  --api-key=sk-63851b428d4b43cb939ab1334a8d8ed8

# 改写第二轮（模板化）
python3 scripts/rewrite_batch_articles.py \
  --round=2 \
  --batch-size=25 \
  --parallel=4

# 改写第三轮（过短）
python3 scripts/rewrite_batch_articles.py \
  --round=3 \
  --batch-size=30 \
  --quality-threshold=7

# 质量检查
python3 scripts/quality_audit.py --check-all

# 生成报告
python3 scripts/quality_report.py --output=html > report.html
```

---

**下一步**: 开始阶段1（前端优化）和阶段2（并行改写）
