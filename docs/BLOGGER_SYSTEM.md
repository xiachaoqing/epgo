# Blogger 自动发布系统 - 业务说明

**网址:** https://xiachaoqing.blogspot.com
**发布频率:** 每天 2 篇（9:00 + 15:00）
**状态:** 由另一个AI在管理（不改动）

---

## 业务流程

### 1. 文章生成阶段
**脚本:** `/Users/xiachaoqing/projects/epgo/scripts/gen_blogger_english_articles.py`

**内容方向:** KET/PET 英语备考类英文文章

**文章类型示例:**
- KET阅读技巧
- KET听力真题解析
- PET写作指导
- 英语学习方法

**输出:** HTML格式文章，包含：
- 标题 + 标签
- 图片（Unsplash免费图库）
- 内容段落
- 内部链接

---

### 2. 文章存储阶段
**目录:** `/root/.openclaw/workspace/blogger-articles-en/`

**文件格式:** `.html`（预编译的HTML，可直接发布）

**文件命名:** `{topic-name}.html`
示例: `ket-reading-tips.html`

---

### 3. 自动发布阶段
**脚本:** `/root/.openclaw/workspace/blogger-publisher/auto-publish.py`

**发布时间:**
```
第1篇：每天 09:00
第2篇：每天 15:00
```

**发布方式:**
- 使用 Google Blogger API
- OAuth2 认证（token.pickle）
- 代理: packetstream.io（已配置）

**发布流程:**
1. 读取预生成的HTML文件
2. 解析标题、内容、标签
3. 通过Google API发送到Blogger
4. 文章上线显示 LIVE 状态

---

## 关键配置

**代理设置（无需改动）:**
```
http://berlio:4tEUkj5lGBRR9wxR@proxy.packetstream.io:31112
```

**Google OAuth Token:**
```
/root/.openclaw/workspace/blogger-publisher/token.pickle
```

**Blog ID:**
```
自动从 https://xiachaoqing.blogspot.com 获取
```

---

## 发布计划示例

| 时间 | 标题 | 标签 |
|------|------|------|
| 09:00 | Free vs Paid AI Tools | AI tools, productivity |
| 15:00 | How to Automate Your Job with AI | AI, automation |

---

## 内容特点

✅ **完全英文** - 面向国际英语学习者
✅ **SEO优化** - 含关键词和标签
✅ **配图** - Unsplash高质量图片
✅ **实用价值** - KET/PET备考内容
✅ **长期价值** - 适合AdSense变现

---

## 注意事项

- ⚠️ **不做改动** - 已由AI自动化管理
- ⚠️ **不调整时间** - 9:00和15:00固定
- ⚠️ **不改代理** - packetstream已稳定配置
- ✓ **可监控** - 定期检查Blogger后台发布状态

---

*此系统独立运行，与 xiachaoqing.com 网站内容生成分离*
