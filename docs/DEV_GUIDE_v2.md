# EPGO 开发文档 v2（2026-03-27 更新）

> 接手必读。之前所有踩过的坑都在这里，节省你几天时间。

---

## 一、项目基本信息

| 项目 | 内容 |
|------|------|
| 网站 | https://go.xiachaoqing.com |
| CMS | MetInfo v6（PHP，专属模板语法） |
| 服务器 | 101.42.21.191，宝塔面板 |
| 网站根目录 | `/www/wwwroot/go.xiachaoqing.com/` |
| 模板目录 | `templates/epgo-education/` |
| 数据库 | MySQL，库名`epgo_db`，表前缀`ep_` |
| DB用户 | xiachaoqing / 07090218 |

---

## 二、目录结构

```
templates/epgo-education/
├── head.php              导航栏（深蓝色 #1565C0）
├── foot.php              页脚（深色背景，metv75原版结构）
├── index.php             首页（自定义banner + 内容区）
├── news.php              文章列表页（含自定义epgo-category-header）
├── shownews.php          文章详情页
├── subcolumn_nav.php     子栏目导航条（metv75原版）
├── position.php          面包屑导航（metv75原版）
├── metinfo.inc.php       引擎配置（绝对不能改）
├── config.json           CSS/JS加载列表
├── css/
│   └── epgo-education.css  所有自定义样式（唯一改样式的地方）
└── js/
    └── epgo-education.js   自定义JS
```

---

## 三、MetInfo 模板语法规范

### 3.1 禁止事项（会报错/白屏）

```
❌ {$lang.name|default:'xxx'}   → 编译出_default()函数，报undefined function
❌ <link href="{$metui_url2}xxx">  → 运行时为空字符串，CSS不加载
❌ <link href="{$metui_url3}xxx">  → 同上
❌ <link href="{$template_url}xxx"> → 变量根本不存在
❌ met_meta不在第一行            → 产生双body标签，样式全乱
```

### 3.2 正确的路径写法

```php
<!-- CSS/JS由框架通过config.json自动注入，不需要手写link/script -->
<!-- 如果必须手写，用： -->
<link rel="stylesheet" href="{$url.site}templates/epgo-education/css/epgo-education.css">

<!-- 可用路径变量 -->
{$url.site}      → https://go.xiachaoqing.com/
{$c.index_url}   → 首页URL
```

### 3.3 常用变量

```
{$c.met_webname}      网站名称：英语陪跑GO
{$c.met_logo}         Logo图片URL
{$c.index_url}        首页URL
{$c.met_footright}    页脚版权文字
{$c.met_footother}    页脚备案号
{$c.met_foottext}     页脚其他文字

{$word.home}          多语言词条：首页
{$g.lang}             当前语言标识：cn
{$g.head}             框架注入的head内容

{$data.title}         当前页面标题
{$data.classnow}      当前栏目ID（首页=10001）
{$data.class1}        一级栏目ID

{$lang.footinfo_wx}   公众号二维码图片URL（ep_templates表）
{$lang.footinfo_dsc}  联系电话：17610721765
{$lang.footinfo_tel}  联系标签文字
{$lang.wooktime_text} 工作时间
{$lang.erweima_one}   二维码说明文字
{$lang.aboutus_text}  关注我们标题
{$lang.footlink_title} 友情链接标题
```

### 3.4 导航标签（父子结构）

```php
<!-- 头部导航，正确写法 -->
<tag action='category' type='head' class='active'>
<if value="$m['sub']">
<!-- 有子栏目：显示下拉 -->
<li class="nav-item dropdown">
    <a href="{$m.url}" class="nav-link dropdown-toggle {$m.class}"
       data-toggle="dropdown" data-hover="dropdown">{$m._name}</a>
    <div class="dropdown-menu">
        <tag action='category' cid="$m['id']" type='son' class='active'>
            <a href="{$m.url}" class='dropdown-item {$m.class}'>{$m._name}</a>
        </tag>
    </div>
</li>
<else/>
<!-- 无子栏目：普通链接 -->
<li class='nav-item'>
    <a href="{$m.url}" class="nav-link {$m.class}">{$m._name}</a>
</li>
</if>
</tag>

<!-- 重要：type='head'只显示nav=1的栏目（见数据库说明） -->
<!-- 子栏目通过cid="$m['id']" type='son'查询，不依赖navbarok配置 -->
```

### 3.5 必须存在的框架标签

```php
<!-- head.php 第一行必须是 -->
<met_meta page="$met_page" />

<!-- foot.php 末尾必须有 -->
<met_foot />
```

---

## 四、数据库关键字段说明

### 4.1 ep_column（栏目表）关键字段

| 字段 | 含义 | 正确值 |
|------|------|--------|
| classtype | 栏目层级 | 1=一级 2=二级 3=三级 |
| nav | 是否在头部导航显示 | 1=显示 0=不显示 |
| bigclass | 父级栏目ID | 0=顶级栏目 |
| isshow | 是否对外显示 | 1=显示 |

**当前栏目结构：**
```
KET备考(101)  classtype=1 nav=1
  KET真题解析(111) classtype=2 nav=0
  KET词汇速记(112) classtype=2 nav=0
  KET写作指导(113) classtype=2 nav=0
  KET听力技巧(114) classtype=2 nav=0
PET备考(102)  classtype=1 nav=1
  PET真题解析(121) classtype=2 nav=0
  PET词汇速记(122) classtype=2 nav=0
  PET写作指导(123) classtype=2 nav=0
  PET阅读技巧(124) classtype=2 nav=0
英语阅读(103)  classtype=1 nav=1
英语演讲(104)  classtype=1 nav=1
每日英语(105)  classtype=1 nav=1
资料下载(106)  classtype=1 nav=1
关于我们(107)  classtype=1 nav=1
```

> ⚠️ **子栏目nav必须是0**，否则会平铺在一级导航里

### 4.2 缓存文件说明

修改数据库后必须删这两个缓存，否则不生效：

```bash
# 模板缓存（改模板文件后删）
rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/
rm -rf /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/cache/

# 栏目缓存（改ep_column后删）
rm -f /www/wwwroot/go.xiachaoqing.com/cache/column_cn.php

# 重建目录并赋权
mkdir -p /www/wwwroot/go.xiachaoqing.com/cache/templates
chown www:www /www/wwwroot/go.xiachaoqing.com/cache/templates
```

### 4.3 ep_flash（Banner表）关键字段

```
module = '10001'   → 在首页显示
module = ''        → 不显示（bug！会产生灰色占位空间）
```

---

## 五、CSS 开发规范

**只改 `css/epgo-education.css`，加载顺序：**
1. `public/web/css/basic.css` — 框架基础样式
2. `templates/epgo-education/cache/metinfo.css` — 框架模板样式（由config.json合并）
3. `templates/epgo-education/css/epgo-education.css` — 自定义样式（后加载，权重高）

**当metinfo.css里有`display:none`覆盖时，在epgo-education.css里用`!important`：**
```css
/* 例：metinfo.css把pclogo设为none，需要覆盖 */
.met-nav .met-logo .pclogo { display: block !important; }
```

**已有的关键CSS覆盖：**
```css
/* 导航深蓝色主题 */
.met-nav.navbar { background: #1565C0; }
.met-nav .nav-link { color: #fff !important; }
.met-nav .nav-link.active { border-bottom: 3px solid #FFB81C; }

/* Logo强制显示 */
.met-nav .met-logo .pclogo { display: block !important; }

/* 隐藏框架空banner（index.php有自定义banner） */
.met-banner { display: none !important; }
.met-banner-ny { display: none !important; }

/* 子栏目导航条 */
.met-column-nav { background: #fff; border-bottom: 1px solid #e8edf2; }
.met-column-nav .met-column-nav-ul > li a.active.link { color: #1565C0; }

/* 弹窗默认隐藏 */
#epgo-qr-modal { display: none; }
```

---

## 六、页面结构说明

### 6.1 首页（index.php）

```
head.php
  → 导航栏（深蓝色，父子下拉菜单）
  → 框架banner容器（CSS隐藏）
index.php
  → 自定义banner（epgo-banner-wrap，PHP直接查ep_flash，自动轮播）
  → 统计数据区
  → 栏目卡片
  → 最新文章列表
  → ... 其他内容区
  → 二维码弹窗（#epgo-qr-modal，默认隐藏）
foot.php
```

### 6.2 文章列表页（news.php）

```
head.php
  → 框架met-banner-ny（CSS隐藏）
  → subcolumn_nav.php（子栏目导航条：全部/子栏目1/子栏目2...）
news.php
  → epgo-category-header（自定义栏目标题蓝色背景区）← 不要重复写
  → 文章列表
  → 右侧边栏（栏目导航/推荐文章）
  → 分页
foot.php
```

> ⚠️ `news.php`里已经有`epgo-category-header`作为栏目标题，不要在其他地方再写栏目名称标题，否则会重复显示。

### 6.3 文章详情页（shownews.php）

```
head.php
  → 面包屑（position.php）
shownews.php
  → 文章标题/正文
  → 上下篇导航
  → 评论区（如果有）
foot.php
```

---

## 七、部署流程

```bash
# 1. 本地改完
cd /Users/xiachaoqing/projects/epgo

# 2. 推git
git add templates/epgo-education/
git commit -m "说明改了什么"
git push origin main

# 3. 直接scp到服务器（比git pull快）
scp templates/epgo-education/head.php root@101.42.21.191:/www/wwwroot/go.xiachaoqing.com/templates/epgo-education/

# 4. 清缓存（必须）
ssh root@101.42.21.191 "
rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/
mkdir -p /www/wwwroot/go.xiachaoqing.com/cache/templates
chown www:www /www/wwwroot/go.xiachaoqing.com/cache/templates
"

# 5. 验证
curl -sk --resolve go.xiachaoqing.com:443:101.42.21.191 https://go.xiachaoqing.com/ | grep '<title>'
```

---

## 八、常见问题排查

| 症状 | 原因 | 解决 |
|------|------|------|
| 整站白屏 | `metinfo.inc.php`里`$template_type`被删或不是`"tag"` | 恢复该文件 |
| 样式全乱/列表bullet点 | CSS没加载，可能用了`$metui_url2`变量 | 删掉那些link标签 |
| 子栏目平铺在导航 | `ep_column.nav=1`（子栏目应该是0）| 修数据库 |
| 导航下拉菜单空 | `ep_column.classtype`值错误或`column_cn.php`缓存未删 | 修classtype(1级=1,2级=2)，删缓存 |
| 首页灰色大空白 | `ep_flash.module`为空 | 改为`module='10001'` |
| Logo不显示 | `metinfo.css`里`.pclogo{display:none}`覆盖了 | `epgo-education.css`里加`!important` |
| 底部弹窗直接展开 | CSS里没有`#epgo-qr-modal{display:none}` | 补CSS |
| 修数据库后没生效 | 框架有`cache/column_cn.php`缓存 | `rm -f cache/column_cn.php` |

---

## 九、不能动的文件

| 文件 | 原因 |
|------|------|
| `metinfo.inc.php` | 改了`$template_type`整站白屏 |
| `config/config_db.php` | 数据库密码，不提交git |
| `app/` 目录 | MetInfo框架核心 |
| `cache/` 目录下的文件 | 自动生成，手改没用 |
| `public/` 目录 | 框架公共资源 |

---

*最后更新：2026-03-27*
