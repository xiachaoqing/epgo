# EPGO 教育类模板

专为英语教育类网站设计的现代化MetInfo模板，完美适配EPGO（英语陪跑GO）项目。

## 🎨 核心特性

### 设计理念
- **教育专业** - 清晰的信息架构，易用的学习路径
- **现代美观** - 蓝+绿色系，专业的UI设计
- **移动友好** - 完整的响应式设计支持
- **广告友好** - Google AdSense无缝融合

### 页面组成

#### 1. 首页 (index.php)
- ✅ Hero Banner - 英雄区域，吸引用户注意
- ✅ 核心服务卡片 (4列) - KET、PET、资源、公众号
- ✅ 最新课程内容 - 动态显示最新文章
- ✅ 英文演讲&历史故事 - 特色内容展示
- ✅ 学员成就墙 - 数据统计 + 案例展示
- ✅ Google AdSense广告位
- ✅ 公众号推广区 - 二维码 + 推广文案
- ✅ Footer - 完整的页脚导航和联系方式

#### 2. 列表页 (news.php)
- ✅ 页面标题区 - 漂亮的标题背景
- ✅ 面包屑导航
- ✅ 左侧文章列表 - 卡片式布局
- ✅ 右侧侧边栏
  - 搜索框
  - 热门文章
  - 分类标签
  - Google AdSense广告

#### 3. 详情页 (shownews.php)
- ✅ 文章标题区 - 专业的标题呈现
- ✅ 文章元信息 - 分类、时间、阅读数
- ✅ 文章正文 - 响应式内容展示
- ✅ 文章标签 - 标签云展示
- ✅ 点赞和分享按钮
- ✅ 相关推荐文章
- ✅ 作者信息卡片
- ✅ 侧边栏
  - 热门文章
  - Google AdSense广告
  - 公众号推广卡片

## 🎯 色彩体系

```
主蓝色:   #1E88E5  (导航、按钮、链接)
辅助绿色: #43A047  (成就、进度、亮点)
警告橙色: #FB8C00  (特色内容)
危险红色: #E53935  (推广区块)
中性灰色: #616161  (文本)
背景色:   #F5F5F5  (分隔区块)
```

## 📱 响应式设计

- **PC (1200px+)**: 3列布局（导航 + 内容 + 侧栏）
- **Tablet (768-1199px)**: 2列或单列布局
- **Mobile (<768px)**: 单列布局，优化触摸交互

## 🔧 技术特性

### MetInfo框架标签集成
- `<tag action='category' type='head'>` - 栏目导航
- `<tag action='list'>` - 文章列表
- `<tag action='tags'>` - 标签系统
- 完整的MetInfo模板变量支持

### JavaScript功能
- 服务卡片交互效果
- 内容项目悬停效果
- 滚动动画（Intersection Observer）
- 二维码弹窗功能
- 平滑滚动

### CSS特性
- CSS变量系统 - 易于定制
- 流动布局 - 使用Grid和Flexbox
- 平滑动画 - 所有交互都有过渡效果
- 阴影系统 - 多层次的视觉深度
- 工具类 - 常用Utility Classes

## 📦 文件结构

```
templates/epgo-education/
├── config.json              # 模板配置文件
├── metinfo.inc.php          # MetInfo标记文件
├── head.php                 # 导航头部
├── foot.php                 # 页脚
├── index.php                # 首页
├── news.php                 # 列表页
├── shownews.php             # 详情页
├── css/
│   └── epgo-education.css   # 核心样式
├── js/
│   └── epgo-education.js    # 功能脚本
└── README.md                # 本文件
```

## 🚀 使用方式

### 1. 上传模板到服务器
将整个 `epgo-education` 目录上传到 `/templates/` 目录

### 2. 在宝塔后台启用模板
- 登录宝塔面板
- 进入网站管理 → 模板管理
- 找到"EPGO教育模板"并启用

### 3. 配置后台参数
在MetInfo后台配置以下参数：
- 公众号二维码 (`lang.wechat_qrcode`)
- 公司信息 (`lang.company_name`, `lang.company_phone` 等)
- 网站Logo (`lang.logo`)

## ⚙️ 自定义配置

### 修改色彩
编辑 `css/epgo-education.css` 中的CSS变量：

```css
:root {
  --color-primary: #1E88E5;      /* 改为其他颜色 */
  --color-success: #43A047;      /* 改为其他颜色 */
  /* ... 其他变量 */
}
```

### 修改字体
编辑 `css/epgo-education.css` 中的字体定义：

```css
--font-family: "PingFang SC", "Helvetica Neue", Arial, sans-serif;
```

### 修改间距和圆角
编辑 `css/epgo-education.css` 中的相关变量：

```css
--space-lg: 24px;      /* 改为其他值 */
--radius-md: 8px;      /* 改为其他值 */
```

## 📊 Google AdSense集成

模板已预设以下广告位：

1. **首页全宽广告** - 728x90 (section中部)
2. **列表页侧栏广告** - 300x250 (右侧栏)
3. **详情页侧栏广告** - 300x250 (右侧栏)

广告代码配置：
```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-2043497135383313"
     data-ad-slot="2043497135383313"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
```

> **注意**: 需要替换 `data-ad-slot` 为你的实际广告位ID

## 🔍 SEO优化建议

1. **页面标题** - 使用高质量关键词
2. **Meta描述** - 准确简洁的描述
3. **H标签** - 合理的层级结构
4. **内部链接** - 指向相关内容
5. **图片ALT** - 每张图片都有描述

## 🐛 常见问题

### Q: 如何隐藏Google AdSense广告？
A: 注释掉 `.adsense-container` 相关代码

### Q: 如何修改Hero Banner背景？
A: 编辑 `index.php` 中的 `hero-banner` 样式

### Q: 如何添加新的服务卡片？
A: 在 `index.php` 的 `service-cards-grid` 中复制一个卡片并修改内容

## 📝 更新日志

### v1.0.0 (2024-03-20)
- 首次发布
- 包含首页、列表页、详情页
- 完整的响应式设计
- Google AdSense集成
- 公众号推广功能

## 📄 许可证

版权所有 © 2024 EPGO
