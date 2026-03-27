# EPGO网站 - 内容填充与优化完全指南

> 最后更新：2026-03-21
> 目标：打造美观、丰满、功能完善的英语教育平台

---

## 📱 PC端和移动端优化总览

### PC端 (>1200px)

#### 布局特点
- **导航栏**: 完整的横向菜单，蓝色渐变背景
- **首页banner**: 1920×520px轮播
- **文章网格**: 3列布局
- **下一篇/上一篇**: 并排显示
- **视频卡片**: 3列网格显示

#### 优化完成项
✅ Header导航栏蓝色渐变
✅ Footer特色功能4列网格
✅ 课程卡片hover动画
✅ 数据统计卡片渐变效果
✅ 文章卡片3列响应式
✅ 演讲视频3列网格
✅ 详情页侧栏布局

### 移动端 (<768px)

#### 布局特点
- **导航栏**: 竖直堆叠菜单（底部tab或汉堡包菜单）
- **首页banner**: 240px高度
- **文章网格**: 1-2列布局
- **按钮**: 全宽显示
- **间距**: 减少，更紧凑

#### 已优化的CSS
```css
@media (max-width: 768px) {
  .met-footnav .left_lanmu {
    flex-direction: column; /* 特色功能竖排 */
  }

  .epgo-videos-grid {
    grid-template-columns: 1fr; /* 视频单列 */
  }

  .epgo-pagination {
    flex-direction: column; /* 分页竖排 */
  }
}
```

#### 手机菜单（底部导航栏）
位置: `foot.php` 中的 `met-menu-list` 元素

```php
<div class="met-menu-list" m-type="menu">
    <div class="main">
        <tag action="menu.list">
            <div>
                <a href="{$v.url}" class="item">
                    <i class="{$v.icon}"></i>
                    <span>{$v.name}</span>
                </a>
            </div>
        </tag>
    </div>
</div>
```

**手机菜单优化建议**:
1. 每个菜单项应该有清晰的**图标** (icon)
2. 文字简短，1-2个字最佳
3. 可在MetInfo后台配置颜色和图标
4. 建议菜单项数不超过5个

---

## 📝 内容填充指南

### 第1步：栏目规划

**推荐栏目结构（在MetInfo后台创建）**：

```
主栏目
├── KET备考
│   ├── KET真题解析 (10篇)
│   ├── KET词汇速记 (8篇)
│   ├── KET写作指导 (5篇)
│   └── KET听力技巧 (5篇)
│
├── PET备考
│   ├── PET真题解析 (10篇)
│   ├── PET词汇速记 (8篇)
│   ├── PET写作指导 (5篇)
│   └── PET阅读技巧 (5篇)
│
├── 通用英语
│   ├── 英语阅读 (15篇)
│   ├── 演讲训练 (10篇)
│   ├── 每日英语 (20篇)
│   └── 资料下载 (文件)
│
└── 英文演讲
    ├── TED演讲 (10个视频)
    ├── BBC纪录 (8个视频)
    └── 牛津讲座 (5个视频)
```

### 第2步：文章内容规范

#### 文章格式要求

**标题规范**：
- ✅ 20字以内
- ✅ 包含关键词（如"KET", "词汇", "听力"等）
- ✅ 数字或问句形式更吸引人

示例标题：
- "KET词汇速记：如何在30天内掌握2000个高频词"
- "英语听力技巧：5个方法让你听懂BBC新闻"
- "2024年KET真题解析：阅读部分得分秘诀"

**文章结构**（推荐800-2000字）：

```markdown
# 标题
[一句话摘要 - 说明本文要解决什么问题]

## 导言 (200字)
[为什么要学这个? 学了有什么好处?]

## 核心内容 (800字)

### 知识点1
[详细讲解]
- 要点1
- 要点2

### 知识点2
[继续讲解]

### 学习例句
> "例句1" - 翻译与用法解析
> "例句2" - 翻译与用法解析

## 常见问题
- Q: 问题1？
- A: 回答1

## 总结
[重点回顾，3-5个关键点]

## 推荐资源
- 相关视频：[链接]
- 练习题：[链接]
- 延伸阅读：[链接]
```

**示例完整文章**：

```
# KET词汇速记：15个最高频不规则动词

你是否还在为记忆英文不规则动词而烦恼？在KET考试中，
掌握100个高频不规则动词就能覆盖95%的词汇考点。
本文为你精选15个最常考的动词，并提供记忆技巧。

## 导言
不规则动词是KET考试的难点。与规则动词不同，
它们的过去式和过去分词需要单独记忆。
但不用担心，我们已经为你筛选出最重要的15个。
只要一周，你就能完全掌握它们！

## 核心内容

### 第一类：be型 (是)
- **be** → was/were → been
  - I **was** tired yesterday.（我昨天很累）
  - We **have been** friends for 5 years.（我们已经是5年的朋友了）

- **become** → became → become
  - She **became** a teacher.（她成了一名教师）

### 第二类：ow-ew-own型
- **know** → knew → known
  - I **didn't know** the answer.（我不知道答案）
  - Have you **known** him long?（你认识他很久吗？）

- **grow** → grew → grown
  - He **grew** up in Beijing.（他在北京长大）

## 常见问题
Q: 如何快速记住这些动词？
A: 将同类动词分组，利用谐音或故事法。
例如：know-knew-known → "挪(knew)知识到房间(known)"

Q: 需要全部背诵吗？
A: 不需要。专注于频率TOP 100即可。

## 总结
- 15个高频动词掌握后，建议再扩展到50个
- 使用"间隔重复法"(Spaced Repetition)
- 每个动词至少造3个例句加深印象

## 推荐资源
- 📺 视频：《KET不规则动词完全攻略》
- 📝 练习：《50题不规则动词强化训练》
- 🔗 工具：Anki词卡 KET高频动词包
```

### 第3步：文章配图

#### 图片要求
- **格式**: JPG(照片)、PNG(图表)、WebP(优化)
- **大小**: 单张 < 500KB（总内容 < 3MB）
- **尺寸**:
  - 封面缩略图: 400×300px
  - 文章内图: 800×600px
  - Banner: 1920×540px

#### 获取高质量图片的方式

**1. 免费素材网站**
- Unsplash (https://unsplash.com) - 高清照片
- Pexels (https://pexels.com) - 生活场景
- Pixabay (https://pixabay.com) - 各类素材
- Canva (https://canva.com) - 设计海报

**2. 自制图表**
- 在Canva中设计考试技巧海报
- 用PowerPoint制作学习流程图
- 用Excel制作成绩对比表

**3. 教科书截图** (确保版权允许)
- KET官方真题集页面
- 词汇对比表格
- 发音指导图

**4. 批量处理图片脚本**

```bash
# 使用ImageMagick批量压缩
for file in *.jpg; do
  convert "$file" -resize 800x600 -quality 80 "optimized_$file"
done

# 使用TinyPNG API批量优化 (需要API key)
# 参考: https://tinypng.com/developers
```

### 第4步：MetInfo后台操作流程

#### 添加文章步骤

1. **登录MetInfo后台**
   - 地址: `http://www.mairunkeji.com/admin/`
   - 用户名和密码：[根据实际填写]

2. **进入内容管理**
   - 左侧菜单 → 栏目管理 → 文章管理

3. **新增文章**
   - 点击"添加"按钮
   - 填写基本信息：
     - **标题**: 文章名称
     - **栏目**: 选择对应栏目 (如 KET词汇)
     - **描述**: 100字以内摘要
     - **关键词**: 3-5个SEO关键词
     - **作者**: 留空或输入名字
     - **内容**: 粘贴文章正文

4. **上传封面图**
   - 点击"上传图片"
   - 选择 400×300px 的图片

5. **编辑文章内容**
   - 使用所见即所得编辑器
   - 使用工具栏的图片/视频/表格功能
   - 粘贴图片时自动上传到服务器

6. **设置发布参数**
   - **发布时间**: 设置发布日期
   - **推荐**: 勾选"首页推荐" (可选)
   - **是否发布**: 勾选"立即发布"或保存为草稿

7. **提交**
   - 点击"保存"或"发布"

#### 批量导入文章

如果需要一次导入大量文章，可以：

**方法1: SQL直接导入**（需要数据库权限）

```sql
INSERT INTO met_news
(title, description, content, keyword, issue_id, pic,
 updatetime, author, hits, is_show)
VALUES
('文章标题', '摘要', '完整内容', 'KET,词汇,高频', 12,
 '/img/news/2026/03/abc.jpg', NOW(), '编者', 0, 1);
```

**方法2: 编写Excel导入脚本**

```python
import pandas as pd
import requests

# 读取Excel
df = pd.read_excel('articles.xlsx')

for _, row in df.iterrows():
    # 调用MetInfo API或脚本批量导入
    data = {
        'title': row['标题'],
        'content': row['内容'],
        'category_id': row['栏目ID'],
        ...
    }
    requests.post('http://www.mairunkeji.com/admin/api/article/add', data)
```

---

## 🎬 英文演讲视频集成

### 支持的视频源

#### 1. YouTube视频
```html
<iframe src="https://www.youtube.com/embed/VIDEO_ID"
        width="100%" height="600"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen></iframe>
```

**获取视频ID**:
- 视频链接: `https://www.youtube.com/watch?v=**dQw4w9WgXcQ**`
- 视频ID: `dQw4w9WgXcQ`

#### 2. 优酷视频
```html
<iframe src="https://player.youku.com/embed/VIDEO_ID"
        width="100%" height="600" frameborder="0" allowfullscreen></iframe>
```

#### 3. Vimeo视频
```html
<iframe src="https://player.vimeo.com/video/VIDEO_ID"
        width="100%" height="600" frameborder="0"
        allow="autoplay; encrypted-media" allowfullscreen></iframe>
```

#### 4. 本地视频
```html
<video width="100%" height="600" controls style="border-radius:8px;">
  <source src="/video/speech-001.mp4" type="video/mp4">
  您的浏览器不支持HTML5视频
</video>
```

### 演讲内容建议

#### TED演讲精选

| 编号 | 标题 | 时长 | 难度 | 要点 |
|------|------|------|------|------|
| TED-001 | "The Power of Vulnerable" | 20min | ⭐⭐ | 情感表达、故事讲述 |
| TED-002 | "Do Schools Kill Creativity" | 19min | ⭐⭐ | 论述逻辑、节奏感 |
| TED-003 | "The Surprising Science of Happiness" | 23min | ⭐⭐⭐ | 学术语言、数据支撑 |

#### BBC纪录片推荐

| 编号 | 系列 | 类型 | 字幕难度 |
|------|------|------|---------|
| BBC-001 | David Attenborough | 自然纪录 | 标准英音 |
| BBC-002 | The Office UK | 英式喜剧 | 俚语+口音 |
| BBC-003 | Planet Earth | 科教纪录 | 标准用语 |

#### 牛津讲座推荐

| 编号 | 主题 | 讲师 | 语言水平 |
|------|------|------|---------|
| OXF-001 | Philosophy | Prof. A | 高阶 |
| OXF-002 | History | Prof. B | 中阶 |
| OXF-003 | English Literature | Prof. C | 中阶 |

### 在文章中嵌入视频

在MetInfo编辑器中插入视频的两种方式：

**方式1: 使用编辑器的视频按钮**
- 点击工具栏中的"视频"图标
- 输入视频URL (YouTube/Vimeo)
- 系统自动转换为嵌入代码

**方式2: 手动插入HTML**
```html
<p style="text-align:center; margin:20px 0;">
  <iframe style="width:100%; max-width:800px; height:450px;"
          src="https://www.youtube.com/embed/VIDEO_ID"
          frameborder="0" allowfullscreen></iframe>
</p>
```

---

## 🚀 内容填充完整计划

### 第1周：基础建设
- [ ] 在MetInfo后台创建所有栏目
- [ ] 编写8-10篇核心文章 (不同栏目)
- [ ] 准备20张配图素材

### 第2周：内容扩充
- [ ] 再增加20篇文章
- [ ] 上传10个演讲视频
- [ ] 优化现有文章的SEO

### 第3周：样式调整
- [ ] 测试PC端显示效果
- [ ] 测试移动端显示效果
- [ ] 根据反馈调整CSS

### 第4周+：持续运营
- [ ] 每周更新3-5篇文章
- [ ] 每月添加2-3个新视频
- [ ] 定期清理过期内容

---

## 📊 SEO优化建议

### 关键词策略
```
主关键词: KET备考、PET备考、英语学习
长尾关键词: "如何高效备考KET"、"KET词汇速记方法"
地域词: "北京KET培训"、"在线英语学习"
```

### 文章SEO清单
- [ ] 标题包含主关键词 (1-2次)
- [ ] 首段100字内总结要点
- [ ] H2标题合理使用 (2-3个)
- [ ] 配图添加ALT文字
- [ ] 内链指向相关文章
- [ ] 末尾鼓励评论和分享

### 示例优化文章

```html
<h1>KET词汇速记：30天掌握2000高频词</h1>

<p><!-- SEO优化的开头段落 -->
  KET备考最大的挑战是词汇量。本文为你提供一套
  <strong>科学的词汇学习方法</strong>，
  让你在30天内快速掌握KET高频词汇，
  提高单词考试成绩。
</p>

<h2>为什么KET词汇这么难记？</h2>
<p>...</p>

<h2>5步高效记忆法</h2>
<h3>第1步：分类</h3>
<p>...</p>

<!-- 图片 -->
<img src="/img/xxx.jpg" alt="KET词汇分类表"
     style="max-width:100%; border-radius:8px;">

<!-- 内链 -->
<p>
  相关文章推荐：
  <a href="/ket-listen/">KET听力技巧</a>、
  <a href="/ket-write/">KET写作指导</a>
</p>
```

---

## 💡 常见问题

**Q: 文章不显示怎么办？**
A:
1. 检查是否勾选了"发布"
2. 清除MetInfo缓存 (后台 → 缓存管理)
3. 检查栏目是否正确关联

**Q: 图片显示不了？**
A:
1. 检查图片文件是否真的上传到服务器
2. 检查图片路径是否正确
3. 尝试重新上传

**Q: 移动端菜单混乱？**
A:
1. 在MetInfo后台配置菜单的图标和颜色
2. 清除浏览器缓存
3. 检查screen size是否正确

**Q: 如何统计文章浏览数？**
A:
- MetInfo后台自动记录每篇文章的浏览量
- 后台 → 网站统计 可查看详细数据

---

## 📞 技术支持

- **问题反馈**: 提出具体现象和截图
- **Git提交**: 遇到代码问题立即提交到GitHub
- **缓存清除**: 任何显示问题都先试试清除缓存

---

**祝您网站运营顺利！** 🎉
