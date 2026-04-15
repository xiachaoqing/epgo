# epgo 模板修改规范

> 适用模板：`templates/epgo-education/`
> 参考模板：`templates/metv75/`（官方标准，不可修改）
> 服务器路径：`/www/wwwroot/go.xiachaoqing.com/`
> 数据库：`epgo_db`，表前缀：`ep_`，用户：`xiachaoqing`

---

## 核心原则

**epgo-education 是 metv75 的样式改造版，模板标签语法和 PHP 结构不变，只改 HTML/CSS。**

修改时必须对照 `metv75/` 同名文件，确保：
1. MetInfo 模板标签（`<tag>`, `<if>`, `<list>`, `{$var}`）保持不变
2. `m-id`, `m-type` 属性保持不变（后台编辑依赖）
3. `<pagination/>`, `<pager/>` 等特殊标签不删除

---

## 文件结构

```
templates/epgo-education/
├── head.php          # 导航栏、全局 CSS/JS 引入
├── foot.php          # 页脚、二维码、版权
├── index.php         # 首页
├── news.php          # 文章列表页
├── shownews.php      # 文章详情页
├── ajax/
│   └── news.php      # 文章列表卡片（列表页核心）
├── static/
│   ├── metinfo.css   # 模板主 CSS（可改）
│   └── metinfo.js    # 模板主 JS（可改）
└── cache/            # 框架自动生成，不可手动编辑
    ├── metinfo.css   # 编译后 CSS
    └── metinfo.js    # 编译后 JS
```

---

## CSS 修改规则

### 文件位置
- 只改 `static/metinfo.css`，**不改 `cache/` 目录**
- cache 目录由框架自动合并，改了也会被覆盖

### 颜色变量（CSS 中用 `$varname$` 形式）
| 变量 | 说明 |
|------|------|
| `$first_color$` | 主色（链接色） |
| `$thirdcolor$` | 按钮/强调色 |
| `$titlecolor$` | 标题颜色 |
| `$hovercolor$` | hover 颜色 |

在后台「网站配置 > 颜色设置」中统一修改，不要在 CSS 里写死颜色。

### 响应式断点
| 断点 | 范围 | 用途 |
|------|------|------|
| `@media (max-width: 768px)` | 手机 | 手机端专属样式 |
| `@media (max-width: 992px)` | 平板 | 平板专属样式 |
| `@media (min-width: 768px)` | ≥平板 | 桌面端样式 |

---

## JS 修改规则

### 框架说明
- Bootstrap 版本：**Bootstrap 3 风格**（`basic.css` 用 `.open` 类展开 dropdown）
- jQuery 由 `basic.js` 加载，`metinfo.js` 在其后执行
- 设备判断：`M.device_type` → `'d'`=PC, `'t'`=平板, `'m'`=手机

### 已知问题修复记录
| 问题 | 原因 | 修复方式 |
|------|------|---------|
| PC端导航不展开 | Bootstrap4 `.show` 类无效 | 改用 Bootstrap3 `.open` 类 |

---

## 数据库 / 定时脚本

### 数据库信息
```
Host:   127.0.0.1
DB:     epgo_db
User:   xiachaoqing
Pass:   07090218
表前缀: ep_
```

### 文章表关键字段
```sql
ep_news: id, title, description, content, imgurl, img_ok,
         class1, class2, lang, add_time, hits, display
```

### 定时脚本
- 位置：`/www/wwwroot/go.xiachaoqing.com/scripts/daily_generate_articles.sh`
- crontab：`0 8 * * *`（每天8点）
- 日志：`/var/log/epgo_article_gen.log`
- 每次写入文章时字段 `img_ok=0`（无封面图），列表页有占位图兜底

---

## 部署流程

```bash
# 本地修改后
git add -A
git commit -m "描述"
git push origin main

# 服务器拉取
ssh epgo "cd /www/wwwroot/go.xiachaoqing.com && git pull origin main"

# 清除模板缓存（CSS/JS 有改动时执行）
ssh epgo "rm -f /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/cache/metinfo.{css,js}"
# 访问一次首页，框架自动重建 cache
```

---

## 常见修改示例

### 修改导航栏背景色
```css
/* static/metinfo.css 里搜索 met-nav，修改背景 */
/* head.php 里导航的 style="background:#1565C0" 也要同步修改 */
```

### 修改文章卡片样式
编辑 `ajax/news.php`，对照 `metv75/ajax/news.php` 确保模板标签不变

### 修改页脚
编辑 `foot.php`，注意不删除 `m-id`, `m-type` 属性

---

## 不允许的操作

- ❌ 直接修改 `cache/` 目录下的文件
- ❌ 删除任何 `m-id="..."` 或 `m-type="..."` 属性
- ❌ 删除 `<pagination/>`, `<pager/>`, `<met_foot />` 等框架标签
- ❌ 修改 `metv75/` 目录（仅作参考，不是线上模板）
- ❌ 在 CSS 里硬编码颜色值（用变量）
