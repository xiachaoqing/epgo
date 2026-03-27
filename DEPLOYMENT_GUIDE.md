# EPGO英语教育网站 - 部署与开发指南

> 最后更新：2026-03-21

## 📋 目录

1. [项目概述](#项目概述)
2. [部署流程](#部署流程)
3. [开发工作流](#开发工作流)
4. [文件结构](#文件结构)
5. [图片管理](#图片管理)
6. [内容填充](#内容填充)
7. [样式优化](#样式优化)

---

## 项目概述

**项目名称**: EPGO - 英语陪跑GO（KET/PET备考平台）
**技术框架**: MetInfo CMS v7.5+
**模板名称**: epgo-education
**主要功能**:
- 英语考试备考课程（KET、PET）
- 文章发布与管理
- 课程推荐与学员评价
- 微信公众号集成
- 响应式设计（PC/移动端）

**域名**: www.mairunkeji.com（需在MetInfo后台配置）

---

## 部署流程

### 1. 本地开发流程

```bash
# 1. 克隆仓库（如果是第一次）
git clone git@github.com:xiachaoqing/epgo.git
cd epgo

# 2. 修改文件
# - 编辑 templates/epgo-education/ 下的 PHP 文件
# - 修改 CSS/JS 文件

# 3. 验证修改
# - 在本地浏览器测试（如已安装MetInfo本地环境）
# - 或使用 Git diff 检查变化
git diff templates/epgo-education/

# 4. 提交更改
git add templates/epgo-education/
git commit -m "feat: 优化首页布局和文章显示"

# 5. 推送到GitHub
git push origin main
```

### 2. 服务器部署流程

```bash
# 1. 服务器拉取最新代码
ssh 服务器地址
cd /www/wwwroot/epgo  # 或实际部署路径
git pull origin main

# 2. 清除MetInfo缓存
# - 登录MetInfo后台 (http://域名/admin/)
# - 系统设置 → 缓存管理 → 清空所有缓存

# 3. 验证修改
# - 访问网站前端检查效果
# - 检查开发者工具中是否有错误

# 4. 备份数据库
mysqldump -u user -p database_name > backup_$(date +%Y%m%d).sql
```

### 3. Git 配置说明

**远程仓库**: GitHub (git@github.com:xiachaoqing/epgo.git)

```bash
# 查看当前配置
git remote -v

# 查看状态
git status

# 查看提交历史
git log --oneline -10
```

---

## 开发工作流

### 快速开始

```bash
# 1. 查看有哪些未提交的改动
git status

# 2. 查看具体改动内容
git diff templates/epgo-education/foot.php

# 3. 暂存特定文件
git add templates/epgo-education/index.php

# 4. 提交
git commit -m "优化: 首页文章列表增加到9篇"

# 5. 推送
git push origin main
```

### 标准的 Commit 信息格式

```
feat: 添加新功能 (特性)
fix: 修复bug
style: 样式优化 (不影响代码逻辑)
refactor: 代码重构
docs: 文档更新
perf: 性能优化
chore: 构建或依赖调整
```

示例：
```
git commit -m "feat: 添加英文演讲视频播放功能"
git commit -m "fix: 修复移动端菜单对齐问题"
git commit -m "style: 优化footer特色功能样式"
```

---

## 文件结构

### 重要文件清单

```
templates/epgo-education/
├── head.php              ← 页头(导航、样式导入)
├── foot.php              ← 页脚(菜单、联系方式)
├── index.php             ← 首页
├── shownews.php          ← 文章详情页
├── news.php              ← 文章列表页
├── show.php              ← 通用详情页
├── css/
│   ├── epgo-education.css  ← 主样式文件
│   └── 其他框架样式
├── js/
│   ├── epgo-education.js   ← 主脚本文件
│   └── 其他框架脚本
└── metinfo.inc.php       ← MetInfo集成配置
```

### 关键变量

在MetInfo模板中使用的常用变量：

```php
{$c.index_url}        // 首页URL
{$c.met_webname}      // 网站名称
{$c.met_weixin_appid} // 微信AppID
{$lang.xxx}           // 语言文本
{$data.title}         // 文章标题
{$v.url}              // 循环变量的URL
```

---

## 图片管理

### 图片存储位置

MetInfo CMS 的图片存储方式：

```
/img/                    ← 所有上传的图片目录
  ├── news/              ← 新闻/文章图片
  ├── product/           ├ 产品图片
  ├── banner/            ← banner图片
  └── other/             ← 其他图片
```

### 添加文章图片的步骤

1. **登录MetInfo后台**
   访问: http://您的域名/admin/

2. **选择「文章管理」**
   找到要编辑的文章

3. **上传图片**
   - 点击图片上传按钮
   - 选择本地图片文件
   - 系统会自动存储到 `/img/news/` 目录
   - 获得图片URL（如 `/img/news/2026/03/abc.jpg`）

4. **在文章内容中使用**
   编辑器会自动插入 `<img>` 标签

### 批量导入图片的方式

如果需要批量导入，可以：

1. **FTP上传方式** (如果有FTP权限)
   - 连接到服务器FTP
   - 上传到 `/img/news/` 文件夹
   - 在MetInfo后台引用这些图片

2. **直接数据库插入** (开发者方式)
   ```sql
   -- 图片在数据库中的记录
   UPDATE met_news SET imgurl='/img/news/2026/03/filename.jpg'
   WHERE id=123;
   ```

### 图片优化建议

- **格式**: JPG (照片)、PNG (图表)、WebP (新格式)
- **大小**: 建议 < 500KB
- **尺寸**:
  - Banner: 1920×540px
  - 缩略图: 400×300px
  - 内容图: 800×600px
- **压缩工具**: TinyPNG、ImageOptim 等

---

## 内容填充

### 1. 首页内容更新

**修改文件**: `templates/epgo-education/index.php`

**可编辑部分**:
- 轮播Banner (从数据库查询)
- 数据统计数字
- 课程卡片描述
- 最新文章列表 (从 `num='9'` 改为显示更多)
- 学员评价卡片
- 常见问题

**示例修改**:
```php
// 修改课程卡片数据
<h3 style="font-size:24px; font-weight:700; margin:20px 0; color:#111827;">KET备考</h3>
<p style="color:#6B7280; line-height:1.8; margin-bottom:25px; font-size:15px;">
    剑桥英语初级认证<br>
    适合初中到高中学生<br>
    全面覆盖听说读写<br>
    从零基础到高分
</p>
```

### 2. 文章内容规范

**推荐的文章结构**:

```markdown
# 标题（H1）
一句话摘要

## 导言（H2）
简述文章主要内容

## 核心内容（多个H2）
### 子标题（H3）
具体内容...

- 列表项1
- 列表项2

> 重要提示或引用

### 另一个子标题
继续内容...

## 总结
重点回顾

## 学习建议
后续建议
```

**文章格式要求**:
- ✅ 标题清晰有吸引力
- ✅ 首段100字以内，说明内容主题
- ✅ 使用H2、H3分层次
- ✅ 每个段落 3-5 句话
- ✅ 配置相关图片（封面+内文）
- ✅ 添加标签（2-3个）
- ✅ 文章长度: 800-2000字为佳

### 3. 栏目填充

**建议栏目结构**:

```
KET备考
├── KET真题解析 (5-10篇)
├── KET词汇速记 (5-8篇)
├── KET写作指导 (3-5篇)
└── KET听力技巧 (3-5篇)

PET备考
├── PET真题解析 (5-10篇)
├── PET词汇速记 (5-8篇)
├── PET写作指导 (3-5篇)
└── PET阅读技巧 (3-5篇)

通用英语
├── 英语阅读 (10+篇)
├── 演讲训练 (8+篇)
└── 每日英语 (持续更新)
```

---

## 样式优化

### PC端优化 (> 1200px)

**已优化的部分**:
- ✅ Header导航栏 (蓝色渐变背景)
- ✅ Footer特色功能 (4列网格布局)
- ✅ 首页文章卡片 (3列网格)
- ✅ 详情页下一篇/上一篇 (并排按钮)

**文件**: `css/epgo-education.css`

### 移动端优化 (< 768px)

**关键修改**:

```css
@media (max-width: 768px) {
  /* 菜单改为竖直排列 */
  .met-footnav .left_lanmu {
    flex-direction: column;
  }

  /* 文章卡片改为单列 */
  .epgo-related-grid {
    grid-template-columns: 1fr;
  }

  /* 分页按钮改为竖直排列 */
  .epgo-pagination {
    flex-direction: column;
  }
}
```

### 暗色/亮色主题（可选）

如需支持暗色模式，在 CSS 中添加：

```css
@media (prefers-color-scheme: dark) {
  body {
    background: #1a1a1a;
    color: #e0e0e0;
  }
  .epgo-article-card {
    background: #2a2a2a;
    border-color: #444;
  }
}
```

---

## 常见问题

### Q1: 修改后不见效果
A: 需要清除MetInfo缓存
- 登录后台 → 系统设置 → 缓存管理 → 清空所有缓存
- 或者在URL末尾添加 `?nocache=1` 强制刷新

### Q2: 如何添加新栏目
A: 在MetInfo后台操作
- 登录后台 → 栏目管理 → 添加新栏目
- 模板会自动读取并显示

### Q3: 图片为什么显示不了
A: 检查以下几点
- 图片路径是否正确
- 图片文件是否已上传到服务器
- 检查文件权限 (644)

### Q4: 如何统计访问量
A: 使用MetInfo内置的统计功能
- 后台 → 网站统计 → 查看访问数据
- 或集成Google Analytics

---

## 联系方式

如有问题，请联系：
- **域名**: www.mairunkeji.com
- **备案**: [根据实际填写]
- **维护者**: [项目维护人员]

---

**提示**: 定期更新内容，保持网站新鲜度，有利于搜索引擎排名！
