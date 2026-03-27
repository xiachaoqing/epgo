# EPGO 开发规范手册

> 在改任何文件前，先把这份文档读完。

---

## 一、项目概述

| 项目 | 内容 |
|------|------|
| 网站 | https://xiachaoqing.com |
| CMS | MetInfo v6（PHP，有专属模板语法） |
| 服务器 | 101.42.21.191，宝塔面板管理 |
| 网站根目录 | `/www/wwwroot/go.xiachaoqing.com/` |
| 模板目录 | `templates/epgo-education/` |
| 数据库 | MySQL，库名 `epgo_db`，表前缀 `ep_` |

---

## 二、MetInfo 模板语法

### 2.1 变量输出

```
{$data.title}           文章/产品标题
{$data.content}         正文HTML
{$data.hits}            阅读量
{$data.addtime}         发布时间
{$data.imgurl}          主图URL
{$data.classname}       所属栏目名
{$data.classurl}        所属栏目URL
{$data.class1}          一级栏目ID（数字）

{$c.index_url}          网站首页URL（含末尾斜杠）
{$c.met_webname}        网站名称
{$c.met_logo}           Logo图片URL
{$c.met_weburl}         网站根域名

{$lang.company_name}    语言包：公司名（在后台语言配置里设置）
{$lang.logo}            语言包：Logo
{$lang.wechat_qrcode}   语言包：微信二维码图片

{$word.home}            多语言词条：首页
{$word.wechat}          多语言词条：公众号

{$g.lang}               当前语言标识（cn/en）
{$g.head}               框架注入的额外 head 内容（SEO用）

{$template_url}         模板目录URL（用于引用CSS/JS）
{$metui_url2}           MetInfo UI 框架 v2 路径
{$metui_url3}           MetInfo UI 框架 v3 路径
```

### 2.2 修饰符（Modifier）

```
{$data.title|truncate:50}              截断50字
{$data.addtime|date_format:'%Y-%m-%d'} 格式化日期
{$v.imgurl|thumb:400,200}              生成缩略图 宽x高

❌ 禁止使用 |default: 修饰符
   {$lang.name|default:'fallback'}  → 会编译出 _default() 函数
   tag 引擎不存在 _default()，运行时报 Call to undefined function
   正确写法：直接用 {$lang.name}，在后台配置好对应值
```

### 2.3 CSS/JS 路径——高频踩坑点

**绝对不能在模板里用的变量（运行时为空）：**

```
❌ {$metui_url2}    仅编译阶段可用，运行时输出空字符串
❌ {$metui_url3}    同上
❌ {$template_url}  根本不存在于框架
```

**正确做法：**

```php
<!-- 1. 框架基础CSS/JS（bootstrap, iconfont等）→ 靠 <met_meta> 自动注入 -->
<!-- head.php 第一行必须有 -->
<met_meta page="$met_page" />

<!-- 2. 模板公共CSS/JS → 写进 config.json，框架合并成 metinfo.css 注入 -->

<!-- 3. 模板自定义CSS → 用 {$url.site} 拼绝对路径 -->
<link rel="stylesheet" href="{$url.site}templates/epgo-education/css/epgo-education.css">

<!-- 4. 可用的路径变量 -->
{$url.site}         网站根URL，如 https://go.xiachaoqing.com/
{$url.public_web}   public/web/ 路径
{$c.index_url}      首页URL
```

### 2.3 条件判断

```php
<if value="$data['imgurl']">
    有图片时显示
</if>

<if value="$data['imgurl']">
    有图
<else/>
    无图
</if>

<if value="$data['classnow'] eq 10001">首页<else/>其他页</if>
<if value="$m['class']">当前激活<else/>未激活</if>
```

### 2.4 循环标签

```php
<!-- 文章列表 -->
<tag action='list' type='news' cid="$data['class1']" num="6" orderby="addtime DESC">
    <a href="{$v.url}">{$v.title}</a>
    <span>{$v.hits}</span>
</tag>

<!-- 栏目导航（一级） -->
<tag action='category' type='head'>
    <a href="{$m.url}">{$m._name}</a>
</tag>

<!-- 子栏目 -->
<tag action='category' cid="$m['id']" type='son'>
    <a href="{$m.url}">{$m.name}</a>
</tag>

<!-- 文章标签 -->
<tag action='tags' id="$data['id']" type='news'>
    <a href="{$m.url}">{$m.name}</a>
</tag>
```

### 2.5 必须存在的框架标签

```php
<!-- head.php 开头必须有 -->
<met_meta page="$met_page" />

<!-- foot.php 末尾必须有 -->
<met_foot />

<!-- 分页（列表页） -->
<pagination/>

<!-- 引入子模板 -->
<include file="head.php" />
<include file="foot.php" />
```

### 2.6 m-id 属性（框架识别用，不能乱删）

| m-id 值 | 作用 |
|---------|------|
| `noset` | 主内容区域，框架注入文章数据 |
| `news_bar` | 侧栏 |
| `met_head` | 导航区域 |

---

## 三、metinfo.inc.php — 必须正确配置

**这个文件控制模板引擎类型，配错会导致整站白屏。**

```php
<?php
global $metinfover;
$metinfover    = "v2";      // ← 必须是 v2，不能删不能改
$template_type = "tag";     // ← 必须是 tag，不能删不能改

$metadmin['categorynamemark']  = 1;
$metadmin['categoryimage']     = 1;
$metadmin['categorymarkimage'] = 0;
$metadmin['system_flash_option_ok'] = array(
    'all' => 1, 'img_des' => 1,
    'img_title_color' => 1, 'img_des_color' => 1,
    'img_text_position' => 1
);
```

**排错：出现 "error templates file is not found"**

原因链路：
1. `$template_type` 未定义或不是 `"tag"`
2. 系统认为是 `parse` 引擎 → 找 `parse.class.php`
3. 该文件不存在 → 报错

修复：检查 `metinfo.inc.php` 里两行是否存在。

---

## 四、数据库表结构

### 4.1 ep_news（文章表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| title | varchar(200) | 标题 |
| content | longtext | 正文HTML |
| class1 | int | 一级栏目ID（对应 ep_column.id） |
| class2 | int | 二级栏目ID（0=无） |
| class3 | int | 三级栏目ID（0=无） |
| imgurl | varchar(255) | 封面图路径（相对路径，拼接域名使用） |
| hits | int | 阅读量 |
| addtime | datetime | 发布时间 |
| updatetime | datetime | 更新时间 |
| displaytype | int | 1=正常显示 0=隐藏 |
| recycle | int | 1=已删除（回收站） |
| lang | varchar(50) | 语言 cn/en |
| tag | mediumtext | 标签（逗号分隔） |
| top_ok | int | 1=置顶 |
| keywords | varchar(200) | SEO关键词 |
| description | mediumtext | SEO描述 |

**常用查询：**

```sql
-- 某栏目最新文章
SELECT id, title, hits, addtime, imgurl
FROM ep_news
WHERE class1 = 101 AND displaytype = 1 AND recycle = 0 AND lang = 'cn'
ORDER BY addtime DESC LIMIT 10;

-- 上一篇（同栏目）
SELECT id, title FROM ep_news
WHERE class1 = ? AND id < ? AND displaytype = 1 AND recycle = 0
ORDER BY id DESC LIMIT 1;

-- 下一篇（同栏目）
SELECT id, title FROM ep_news
WHERE class1 = ? AND id > ? AND displaytype = 1 AND recycle = 0
ORDER BY id ASC LIMIT 1;

-- 热门文章
SELECT id, title, hits FROM ep_news
WHERE displaytype = 1 AND recycle = 0 AND lang = 'cn'
ORDER BY hits DESC LIMIT 5;
```

### 4.2 ep_column（栏目表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | varchar(100) | 栏目名称 |
| bigclass | int | 父级栏目ID（0=顶级） |
| module | int | 类型：1=单页 2=文章列表 4=下载 |
| foldername | varchar(50) | URL路径名 |
| isshow | int | 1=显示 0=隐藏 |
| no_order | int | 排序权重 |

**当前栏目树：**

```
101  KET备考       (module=2, /ket/)
  111  KET真题解析  (/ket-exam/)
  112  KET词汇速记  (/ket-word/)
  113  KET写作指导  (/ket-write/)
  114  KET听力技巧  (/ket-listen/)
102  PET备考       (module=2, /pet/)
  121  PET真题解析  (/pet-exam/)
  122  PET词汇速记  (/pet-word/)
  123  PET写作指导  (/pet-write/)
  124  PET阅读技巧  (/pet-read/)
103  英语阅读       (module=2, /reading/)
104  英语演讲       (module=2, /speech/)
105  每日英语       (module=2, /daily/)
106  资料下载       (module=4, /download/)
107  关于我们       (module=1, /about/)
```

### 4.3 ep_config（系统配置表）

| 字段 | 说明 |
|------|------|
| name | 配置项名称 |
| value | PC端配置值 |
| mobile_value | 移动端配置值 |
| lang | 所属语言（cn/en） |

**关键配置项：**

```sql
SELECT name, value FROM ep_config WHERE lang='cn' AND name IN (
  'met_skin_user',   -- 当前模板名（必须等于 epgo-education）
  'met_webname',     -- 网站名称：英语陪跑GO
  'met_logo',        -- Logo图片路径
  'met_keywords',    -- 全站默认SEO关键词
  'met_description'  -- 全站默认SEO描述
);
```

### 4.4 ep_lang（多语言配置表）

后台"模板配置"里设置的值存这里，模板里用 `{$lang.xxx}` 读取。

```sql
-- 查看所有模板配置
SELECT name, value FROM ep_lang WHERE lang='cn';
-- 关键字段：company_name, logo, wechat_qrcode, favicon
```

### 4.5 ep_flash（轮播图表）

| 字段 | 说明 |
|------|------|
| id | 主键 |
| title | 图片标题 |
| imgurl | 图片路径 |
| url | 点击跳转链接 |
| columnid | 所属栏目（0=全局） |
| no_order | 排序 |

---

## 五、模板文件说明

```
templates/epgo-education/
├── metinfo.inc.php      ← 引擎配置（绝对不要删 $template_type）
├── config.json          ← 模板CSS/JS加载列表
├── head.php             ← 导航 + CSS + 弹窗
├── foot.php             ← 页脚 + JS + met_foot
├── index.php            ← 首页
├── news.php             ← 文章列表页
├── shownews.php         ← 文章详情页
├── show.php             ← 单页（关于我们等）
├── showdownload.php     ← 下载详情页
├── download.php         ← 下载列表页
├── search.php           ← 搜索结果页
├── sitemap.php          ← 网站地图
├── ajax/
│   └── news.php         ← 列表页AJAX片段
├── css/
│   └── epgo-education.css  ← 所有自定义样式
└── js/
    └── epgo-education.js   ← 自定义JS
```

---

## 六、CSS 开发规范

**只改 `css/epgo-education.css`，不要内联写 style 属性。**

```css
/* 主色调（改颜色只改这里） */
:root {
  --epgo-blue: #2563EB;
  --epgo-blue-dark: #1D4ED8;
}

/* 命名规范：所有自定义 class 加 epgo- 前缀 */
.epgo-card { }
.epgo-hero { }

/* 禁止覆盖框架class */
/* ❌ .met-head { } */
/* ❌ .navbar { }  */
/* ✅ .epgo-nav-custom { } */
```

**改完CSS后需要在 MetInfo 后台清除缓存：**
后台 → 系统设置 → 清除缓存，或执行：
```bash
ssh root@101.42.21.191 "rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/"
```

---

## 七、部署流程

### 修改模板文件后

```bash
# 1. 在本地改好文件

# 2. 推送到 git
cd /Users/xiachaoqing/projects/epgo
git add templates/epgo-education/
git commit -m "fix: 说明改了什么"
git push origin main

# 3. 在服务器拉取
ssh root@101.42.21.191 "cd /www/wwwroot/go.xiachaoqing.com && git pull origin main"

# 4. 清除模板缓存（必须做）
ssh root@101.42.21.191 "rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/"

# 5. 验证
curl -sk --resolve go.xiachaoqing.com:443:101.42.21.191 https://go.xiachaoqing.com/ | grep '<title>'
```

### 服务器文件权限规范

```bash
# 部署后若出现权限问题，一键修复：
ssh root@101.42.21.191 "
  chown -R www:www /www/wwwroot/go.xiachaoqing.com/templates/
  chmod -R 755 /www/wwwroot/go.xiachaoqing.com/templates/
  rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/
"
# 文件所有者必须是 www:www，权限必须是 755
# git pull 后文件可能变成 root:root，导致 "file is not found" 错误
```

---

## 八、常见错误排查

### error templates file is not found

原因1：`metinfo.inc.php` 缺少 `$template_type = "tag"`
→ 修复：补上这两行，清除缓存

原因2：模板里用了 `|default:` 修饰符
→ 症状：`Call to undefined function _default()`
→ 修复：删掉所有 `|default:xxx`，直接用变量

```bash
# 快速检查是否有 |default: 残留
grep -r '|default:' templates/epgo-education/*.php
```

### 页面内容不显示（文章详情页）

检查 `shownews.php` 主内容区是否有 `m-id="noset"`：

```php
<div class="col-md-9" m-id="noset">   ← 不能少
    {$data.content}
</div>
```

### 样式改了不生效

1. 清除 MetInfo 模板缓存（见上）
2. 强制刷新浏览器 `Cmd+Shift+R`

### git pull 报冲突

```bash
ssh root@101.42.21.191 "
  cd /www/wwwroot/go.xiachaoqing.com
  git stash           # 把服务器上的修改暂存
  git pull origin main
"
# 不要用 git reset --hard，会导致文件权限混乱
```

---

## 九、不要动的内容

| 内容 | 原因 |
|------|------|
| `metinfo.inc.php` 的 `$template_type` | 改了整站白屏 |
| `cache/` 目录下的文件 | 自动生成，改了没用会被覆盖 |
| `config/config_db.php` | 数据库密码，不要提交到 git |
| `app/` 目录下所有文件 | MetInfo 框架核心，不属于此项目 |
| Nginx 伪静态配置 | `/www/server/panel/vhost/rewrite/go.xiachaoqing.com.conf` |
| `.user.ini` | 宝塔安全配置，权限锁定 |

---

## 十、接口与数据

### MetInfo 没有对外 REST API

MetInfo 是传统 PHP 渲染，所有数据在服务端通过模板标签注入，**没有 JSON 接口**。

如需前端异步获取数据，有两种方式：

**方式1：MetInfo AJAX 接口（框架自带）**

```javascript
// 获取文章列表（框架内置，仅用于模板内）
// 参数参考 app/system/news/ 目录下的控制器
POST /index.php?m=news&f=index&v=list
参数: classid=101&page=1&num=10
```

**方式2：直接查数据库（脚本用）**

```python
# scripts/ 目录下的脚本连接方式
import pymysql
db = pymysql.connect(
    host='127.0.0.1', port=3306,
    user='xiachaoqing', password='07090218',
    database='epgo_db', charset='utf8mb4'
)
```

### 后台管理入口

```
https://xiachaoqing.com/admin/
账号密码在服务器本地，不入库
```

---

*最后更新：2026-03-27*
