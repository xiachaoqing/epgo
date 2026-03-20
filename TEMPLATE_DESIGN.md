# EPGO 教育类模板设计方案

## 设计理念

EPGO（英语陪跑GO）是面向英语学习者的专业教育平台，核心特点：
- **知识型**: KET/PET考试培训、英文演讲、历史故事等内容
- **专业性**: 清晰的信息架构，易用的学习路径
- **社群性**: 推广公众号，建立学习社群
- **变现性**: Google AdSense广告无缝融合

## 视觉设计规范

### 1. 色彩体系

#### 主色调
```
- 主蓝色: #1E88E5 (专业、信任、教育感)
- 辅助绿色: #43A047 (活力、成长、进步)
- 中性灰: #616161 (文字、辅助)
- 背景白: #FFFFFF
```

#### 使用场景
- 导航、按钮、链接: 主蓝色
- 成就、进度、亮点: 辅助绿色
- 文本、分割线、border: 中性灰
- 背景: 白色 + 浅灰 (#F5F5F5)

### 2. 字体体系

```
标题: "PingFang SC", "Helvetica Neue", sans-serif, bold
正文: "PingFang SC", "Helvetica Neue", sans-serif, regular
字号:
  - H1: 32px (页面标题)
  - H2: 24px (区块标题)
  - H3: 20px (子标题)
  - 正文: 16px (PC) / 14px (Mobile)
  - 小文本: 12px (辅助信息)
```

### 3. 间距规范

```
基础单位: 8px
常用间距: 8px, 16px, 24px, 32px, 48px
区块间距: 60px (视觉呼吸感)
卡片内边距: 24px
```

### 4. 圆角规范

```
小组件: 4px
卡片: 8px
按钮: 4px
大组件: 12px
```

---

## 页面结构设计

### 首页 (index.php)

#### 区块1: Hero Banner (英雄区)
```
高度: 600px
背景: 渐变蓝色 (#1E88E5 -> #1565C0) 或精美教育相关图片
内容:
  - 标题: "英语陪跑GO" (42px, 白色, 加粗)
  - 副标题: "让英语学习不再枯燥，专业KET/PET考试培训" (18px, 白色)
  - CTA按钮: "开始学习" + "关注公众号" (两个按钮)
  - 背景元素: 英文字、书籍、笔等装饰
布局: 居中, flex布局
动画: 从上淡入 (fade-in)
```

#### 区块2: 核心服务卡片 (4列)
```
标题: "快速导航"
4个卡片:
  1. 📘 KET考试教程 → 指向KET栏目
     描述: "KET真题、词汇、听力、写作全套教程"
     图标颜色: #1E88E5

  2. 📕 PET考试教程 → 指向PET栏目
     描述: "PET完整学习路径，助力考试成功"
     图标颜色: #43A047

  3. 📚 学习资源 → 指向资源栏目
     描述: "词汇表、语法、真题、音频全免费下载"
     图标颜色: #FB8C00

  4. 👥 关注公众号 → 弹窗显示二维码
     描述: "每日英语干货，考试技巧分享，免费答疑"
     图标颜色: #E53935

设计:
  - 卡片: 白色背景, border-left: 4px 彩色
  - hover效果: 向上提升 3px, box-shadow增强
  - 图标: 32px, 圆形背景
  - 响应式: PC(4列) → Tablet(2列) → Mobile(1列)
```

#### 区块3: 最新课程内容
```
标题: "最新课程"
显示: 8篇最新文章
布局:
  - 大卡片布局 (左大右3个小)
  - 大卡片: 显示第1篇文章
    * 背景图: 文章配图
    * 标题、描述、发布时间、阅读数
    * hover: 图片缩放
  - 右侧3个卡片: 第2-4篇简化版本
    * 小图 + 标题 + 简要信息
    * 上下排列

设计:
  - 卡片圆角: 8px
  - 图片: object-fit: cover
  - 标题颜色: #1E88E5 (hover变色)
  - 分类标签: 背景 #E3F2FD, 文字 #1E88E5
  - 发布时间: 灰色, 14px
```

#### 区块4: 热门资源下载
```
标题: "热门资源下载"
显示: 6-8个热门资源
布局: 3列网格
单个资源卡片:
  - 图标/缩略图 (顶部)
  - 资源名称 (加粗)
  - 简介 (灰色, 13px)
  - 下载按钮 (蓝色, 圆角4px)
  - 下载数/热度显示

设计:
  - 背景: 白色, border: 1px #EEE
  - hover: 背景变浅灰, box-shadow出现
  - 图标: 32px, 圆形背景
```

#### 区块5: 英文演讲/历史故事
```
标题: "英文演讲 & 历史故事"
描述: "通过名人演讲和历史故事学习英语，增长见闻"

显示: 4个推荐内容 (2x2网格)
单项内容:
  - 视频/图片缩略图
  - 标题 (白色文字, 叠加在图片上)
  - 分类标签: "演讲" / "故事"
  - 播放/阅读按钮 (overlay)

设计:
  - 卡片比例: 16:9
  - hover: 亮度降低, 显示播放按钮
  - 分类标签背景: 半透明黑
```

#### 区块6: 学员成就墙
```
标题: "学员成就"
显示: 数据统计 + 学员案例

数据统计行:
  ✓ 5000+ 学员
  ✓ 87% 考试通过率
  ✓ 4.8 ⭐ 平均评分
  ✓ 1000+ 小时教学

布局: 4列, 大字体数字 + 描述

学员案例:
  显示: 3-4个代表学员
  单项:
    - 学员头像 (圆形, 60px)
    - 名字、考试等级
    - 短评价 ("3个月从零基础到KET通过")
    - 星评分

设计:
  - 案例卡片: 白色背景, 圆角8px
  - 头像: 圆形, border: 3px #43A047
  - 数据字号: 32px, 加粗, 蓝色
```

#### 区块7: 公众号推广区
```
位置: 关键位置 (通常在中部)
背景: 渐变色 (#1E88E5 -> #1565C0) 或英文背景图
内容:
  左侧 (60%):
    - 标题: "关注公众号 英语陪跑GO"
    - 描述: "坚持每日打卡，轻松提升英语水平"
    - 核心福利列表:
      ✓ 每日精选英语单词 (含发音)
      ✓ KET/PET考试技巧分享
      ✓ 学习资料免费领取
      ✓ 专业老师在线答疑
    - 字体: 白色, 18px

  右侧 (40%):
    - 公众号二维码 (200x200px)
    - 二维码下方: "长按扫码关注"

设计:
  - 背景: 深蓝渐变或英文教育背景图
  - 文字: 白色, 高对比度
  - 二维码: 白色背景, 圆角8px, padding: 10px
  - 响应式: Mobile时改为上下布局
```

#### 区块8: Google AdSense 广告位
```
位置: 上区块下方
尺寸: 728x90 (横幅广告)
或: 300x250 (矩形广告, 侧边栏)

设计:
  - 外层容器: padding: 20px 0
  - 背景: #F5F5F5 (浅灰)
  - border-top: 1px #DDD
  - 广告文字标签: "赞助广告" (灰色, 12px)
```

#### 区块9: Footer区域
```
背景: #263238 (深灰蓝)
文字: 白色, 13px

上部:
  - 品牌信息: Logo + "英语陪跑GO - 专业英语教育平台"
  - 3列链接:
    * 快速链接 (首页、KET、PET等)
    * 资源中心 (资料下载、视频教学等)
    * 联系方式 (Email、客服、反馈)

中部:
  - 社交媒体链接: 公众号、微博等

下部:
  - 版权信息: "© 2024 英语陪跑GO. All Rights Reserved."
  - ICP备案号 (如有)
```

---

## 列表页 (news.php / 内容列表)

### 设计

```
上部: 页面标题 + 背景图
  - 标题: 栏目名称 (如"KET考试教程")
  - 背景: 对应栏目的色系渐变
  - 高度: 300px

左侧 (70%): 文章列表
  - 视图模式: 卡片视图
  - 单个卡片:
    * 左: 缩略图 (200x150px)
    * 右: 标题、分类、摘要、发布时间、阅读数
    * hover: 卡片向上提升, shadow增强
  - 分页: 下方分页器
  - 排序: 最新 / 热门 / 评分

右侧 (30%): 侧边栏
  - 搜索框 (顶部)
  - 热门文章列表 (缩略版)
  - 分类云标签
  - Google AdSense 300x600广告
  - 公众号推广小卡片
```

---

## 文章详情页 (shownews.php)

### 设计

```
上部: 面包屑导航
中部:
  - 文章标题 (36px, 加粗)
  - 元信息: 分类、作者、发布时间、阅读数

正文区 (70%):
  - 正文: 16px, 行高 1.8
  - 代码块: 深色背景 (#263238), 可复制
  - 图片: max-width: 100%, 圆角4px
  - 视频: 响应式iframe

右侧边栏 (30%):
  - 目录 (TOC) - 自动生成H2/H3
  - 关键词标签 (可点击)
  - 相关文章推荐 (3篇)
  - Google AdSense 300x250广告

下部:
  - 点赞/分享按钮
  - 作者信息卡片
  - 评论区 (如启用)
  - 相关推荐文章 (3篇)
```

---

## 响应式断点

```
PC (Desktop): 1200px+
  - 导航: 完整显示
  - 布局: 3列 (左导航/中内容/右侧栏)
  - 字号: 16px (正文)

Tablet (平板): 768px - 1199px
  - 导航: 导航栏折叠
  - 布局: 2列或单列
  - 字号: 15px

Mobile (手机): < 768px
  - 导航: 汉堡菜单
  - 布局: 单列
  - 字号: 14px
  - 间距: 减半
  - 卡片: 全宽
```

---

## CSS样式规范

### 变量定义

```css
:root {
  /* 色彩 */
  --color-primary: #1E88E5;    /* 主蓝 */
  --color-success: #43A047;    /* 成功绿 */
  --color-warning: #FB8C00;    /* 警告橙 */
  --color-danger: #E53935;     /* 危险红 */
  --color-text: #616161;       /* 正文灰 */
  --color-border: #EEEEEE;     /* 边框灰 */
  --color-bg: #F5F5F5;         /* 背景浅灰 */

  /* 尺寸 */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* 阴影 */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 8px rgba(0,0,0,0.12);
  --shadow-lg: 0 8px 16px rgba(0,0,0,0.15);

  /* 字体 */
  --font-family: "PingFang SC", "Helvetica Neue", sans-serif;
  --font-size-sm: 12px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
}
```

### 常用组件样式

```css
/* 按钮 */
.btn-primary {
  background: var(--color-primary);
  color: white;
  padding: 10px 24px;
  border-radius: var(--radius-sm);
  border: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #1565C0;
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/* 卡片 */
.card {
  background: white;
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  border: 1px solid var(--color-border);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

/* 标题 */
h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1E1E1E;
  margin-bottom: var(--space-lg);
}

h3 {
  font-size: 20px;
  font-weight: 500;
  color: #1E1E1E;
  margin-bottom: var(--space-md);
}

/* 正文 */
p {
  font-size: var(--font-size-base);
  line-height: 1.8;
  color: var(--color-text);
  margin-bottom: var(--space-md);
}
```

---

## 实现清单

- [ ] 创建新的模板目录: `templates/epgo-education/`
- [ ] 创建样式文件: `epgo-education.css`
- [ ] 修改 `head.php` - 导航栏、颜色、Logo
- [ ] 修改 `index.php` - 首页各区块
- [ ] 修改 `news.php` - 列表页
- [ ] 修改 `shownews.php` - 详情页
- [ ] 修改 `foot.php` - Footer
- [ ] 创建 `config.json` - 模板配置
- [ ] 添加响应式媒体查询
- [ ] Google AdSense代码集成
- [ ] 测试各页面在不同设备上的显示

---

## 下一步

1. 确认设计方向是否符合预期
2. 开始实现HTML/CSS代码
3. 集成MetInfo框架的标签系统
4. 本地测试后推送GitHub
5. 线上拉取并启用新模板
