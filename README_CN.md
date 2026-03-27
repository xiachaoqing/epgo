# 🚀 EPGO项目 - 快速开始指南

> 最后更新：2026-03-21
> 适合：项目维护者、开发者、内容编辑

---

## 📌 项目三大核心

| 方面 | 现状 | 下一步 |
|------|------|--------|
| **代码部署** | ✅ Git仓库配置完成 | 学习[GIT_WORKFLOW.md](./GIT_WORKFLOW.md) |
| **网站样式** | ✅ PC/移动端优化完成 | 根据[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)部署 |
| **内容填充** | 🔄 待填充 | 按[CONTENT_FILLING_GUIDE.md](./CONTENT_FILLING_GUIDE.md)操作 |

---

## 🎯 今天完成的优化

### 1. 新增功能
- ✅ **英文演讲播放页面** (`speech.php`)
  - 支持 YouTube、优酷、Vimeo 视频
  - 视频分类筛选功能
  - 精美的演讲卡片布局

### 2. 首页优化
- ✅ 文章列表增加至 **12 篇**（原来 6 篇）
- ✅ 新增 **英文演讲推荐** 区块
- ✅ 数据统计卡片优化（渐变颜色、hover效果）
- ✅ 课程卡片 hover 动画

### 3. 样式增强
- ✅ Footer 特色功能对齐修复
- ✅ 下一篇/上一篇导航重新实现
- ✅ 移动端全面适配
- ✅ 响应式网格布局

### 4. 文档完善
- ✅ [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - 部署指南
- ✅ [CONTENT_FILLING_GUIDE.md](./CONTENT_FILLING_GUIDE.md) - 内容填充指南
- ✅ [GIT_WORKFLOW.md](./GIT_WORKFLOW.md) - Git工作流指南

---

## 🔄 部署流程（分为3个阶段）

### 阶段1：本地验证 (已完成 ✅)
```bash
cd /Users/xiachaoqing/projects/epgo

# 查看改动
git log --oneline -5

# 查看改动内容
git show HEAD:templates/epgo-education/index.php | head -50
```

### 阶段2：推送到GitHub (已完成 ✅)
```bash
# 所有改动已推送
git push origin main
```

### 阶段3：服务器部署 (待执行)
```bash
# SSH到服务器
ssh root@39.105.154.244

# 进入项目目录
cd /www/wwwroot/epgo

# 拉取最新代码
git pull origin main

# 清除MetInfo缓存 (登录后台或使用API)
# http://www.mairunkeji.com/admin/ → 系统设置 → 缓存管理 → 清空

# 验证部署
curl -s http://www.mairunkeji.com/ | grep -i "英文演讲"
```

---

## 📝 内容填充快速开始

### 第1步：准备工作 (5分钟)

1. **登录MetInfo后台**
   - 地址: `http://www.mairunkeji.com/admin/`
   - 用户: [根据实际]
   - 密码: [根据实际]

2. **查看现有栏目**
   - 左侧菜单 → 栏目管理
   - 记下栏目ID（用于后续操作）

### 第2步：创建栏目 (10分钟)

如果栏目不足，新增栏目：

```
建议新增栏目：
- KET真题解析 (parent: KET备考)
- KET词汇速记 (parent: KET备考)
- PET真题解析 (parent: PET备考)
- 英文演讲 (顶级栏目)
```

**操作步骤**:
1. 栏目管理 → 添加
2. 填写栏目名称
3. 设置父栏目
4. 点击保存

### 第3步：编写文章 (30分钟/篇)

**快速文章模板**:

```
标题：KET词汇速记：30天掌握2000高频词

摘要：
掌握100个高频不规则动词就能覆盖95%的KET词汇考点。
本文提供科学的学习方法，让你一周内完全掌握。

关键词：KET, 词汇, 记忆方法

内容：
[按照CONTENT_FILLING_GUIDE.md中的文章模板编写]
- 导言段落
- 3-5个核心知识点
- 学习例句
- 总结回顾
- 推荐资源

配图：
- 封面图 (400×300)
- 内文图 (800×600)
```

### 第4步：上传视频 (快速)

英文演讲视频可以直接使用公开视频：

**推荐视频源**:
1. **YouTube** - 最多的内容
   - TED-Ed: https://www.youtube.com/user/TED-Ed
   - Kurzgesagt: 科学知识讲解

2. **优酷** - 中文字幕
   - BBC纪录片合集
   - 英文演讲合集

3. **Vimeo** - 高质量原创
   - 设计和艺术类演讲

**操作步骤**:
1. 在 `speech.php` 中找到视频URL
2. 在MetInfo后台添加产品（用于视频）
3. 输入视频标题和描述
4. 粘贴视频链接

---

## 📱 测试清单

### PC端测试 (Chrome浏览器)

- [ ] 首页banner轮播正常
- [ ] 数据统计卡片显示正确
- [ ] 课程卡片hover有动画
- [ ] 文章列表3列显示
- [ ] 英文演讲推荐显示
- [ ] 下一篇/上一篇导航在文章详情页工作
- [ ] 分享按钮工作正常
- [ ] Footer菜单对齐

### 移动端测试 (Chrome DevTools)

设置 `375×667` (iPhone SE):

- [ ] Header菜单竖直排列
- [ ] Banner高度合理 (240px)
- [ ] 文章卡片1-2列显示
- [ ] 视频卡片单列显示
- [ ] 按钮大小适中（不小于44px）
- [ ] 底部menu正常显示

### 不同尺寸测试

```
iPad (768×1024) - 平板
  - 课程卡片2列
  - 文章卡片2列
  - 侧栏应显示

iPad Pro (1024×1366) - 大平板
  - 应该接近PC端布局
```

---

## 🔧 常见问题速查

### Q1: 新增的演讲页面无法访问
**A**: 需要在MetInfo后台配置菜单
1. 后台 → 菜单管理
2. 添加新菜单项指向 `{$c.index_url}speech/`
3. 清除缓存

### Q2: 首页看不到新增的内容
**A**:
1. 清除浏览器缓存 (Ctrl+Shift+Delete)
2. 清除MetInfo缓存
3. 检查浏览器控制台是否有错误

### Q3: 文章发布后看不到
**A**:
1. 检查"发布"复选框是否勾选
2. 检查栏目是否在前台显示
3. 清除缓存并刷新

### Q4: 图片显示不了
**A**:
1. 确认图片已上传到服务器
2. 在图片管理中检查路径
3. 确保文件权限是644

### Q5: 移动端菜单显示不全
**A**:
1. 检查MetInfo配置中菜单项数量
2. 确保每个菜单项有图标和文字
3. 在 `foot.php` 中调整CSS

---

## 📊 关键文件一览表

| 文件 | 用途 | 优先级 |
|------|------|--------|
| `templates/epgo-education/index.php` | 首页 | 🔴 高 |
| `templates/epgo-education/shownews.php` | 文章详情 | 🔴 高 |
| `templates/epgo-education/speech.php` | 演讲播放 | 🟠 中 |
| `templates/epgo-education/css/epgo-education.css` | 主样式 | 🔴 高 |
| `templates/epgo-education/foot.php` | 页脚菜单 | 🟡 低 |
| `DEPLOYMENT_GUIDE.md` | 部署指南 | 📚 参考 |
| `CONTENT_FILLING_GUIDE.md` | 内容指南 | 📚 参考 |
| `GIT_WORKFLOW.md` | Git指南 | 📚 参考 |

---

## 🚀 下周计划建议

### 内容团队
- [ ] 编写 20 篇高质量文章
- [ ] 收集 10 个优质演讲视频
- [ ] 设计 3-5 个宣传海报（配图）

### 开发团队
- [ ] 部署到生产环境
- [ ] 配置 Google Analytics（SEO追踪）
- [ ] 优化页面加载速度
- [ ] 添加评论功能（可选）

### 运营团队
- [ ] 准备首页文案
- [ ] 制定内容更新计划
- [ ] 建立微信公众号自动推送
- [ ] 准备社交媒体链接

---

## 💬 获取帮助

### 遇到问题？

**1. 先查文档**
- 部署问题 → 查 `DEPLOYMENT_GUIDE.md`
- 内容问题 → 查 `CONTENT_FILLING_GUIDE.md`
- Git问题 → 查 `GIT_WORKFLOW.md`

**2. 查看项目日志**
```bash
git log --oneline -20
git log --grep="关键词" --oneline
```

**3. 检查代码差异**
```bash
git diff HEAD~1 templates/epgo-education/index.php
```

**4. 反馈问题**
- 描述具体现象和截图
- 提交到GitHub Issues
- 或发邮件给维护者

---

## 🎓 学习资源

- [MetInfo CMS官方](https://www.metinfo.cn/)
- [Git基础教程](https://git-scm.com/book/en/v2)
- [HTML/CSS参考](https://developer.mozilla.org/)
- [响应式设计](https://www.w3schools.com/css/css_rwd_intro.asp)

---

## ✅ 完成清单

- ✅ 功能开发完成
- ✅ 样式优化完成
- ✅ 文档编写完成
- ✅ Git提交完成
- 🔄 **下一步：内容填充** ← 你在这里
- 🔄 最后：生产部署

---

**快速导航**:
- 📖 [完整部署指南](./DEPLOYMENT_GUIDE.md)
- 📝 [内容填充指南](./CONTENT_FILLING_GUIDE.md)
- 🔧 [Git工作流](./GIT_WORKFLOW.md)
- 💾 [GitHub仓库](https://github.com/xiachaoqing/epgo)

**祝您网站运营成功！** 🎉
