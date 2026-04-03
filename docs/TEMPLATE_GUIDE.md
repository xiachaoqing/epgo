# epgo-education 模板开发指南

> 适用站点：go.xiachaoqing.com / xiachaoqing.com
> 模板路径：`/www/wwwroot/go.xiachaoqing.com/templates/epgo-education/`
> 本地路径：`/Users/xiachaoqing/projects/epgo/templates/epgo-education/`
> 框架：MetInfo 7.x
> 最后更新：2026-04-03

---

## 目录结构

```
epgo-education/
├── head.php              # 顶部导航 + Banner（所有页面包含）
├── foot.php              # 页脚（所有页面包含）
├── index.php             # 首页
├── news.php              # 文章列表页（子栏目）
├── shownews.php          # 文章详情页
├── show.php              # 单页（关于我们等）
├── product.php           # 产品列表
├── showproduct.php       # 产品详情
├── subcolumn_nav.php     # 子栏目横向导航条
├── position.php          # 面包屑导航
├── para_search.php       # 搜索组件
├── metinfo.inc.php       # 模板引擎配置
├── 13-文章格式规范.md     # 微信公众号文章格式（不影响网站）
├── fetch_media.py        # 抓取微信素材工具脚本
├── css/
│   ├── epgo-education.css   # 主样式（与根目录同名文件内容相同）
│   └── animations.css       # 动画效果
├── static/
│   ├── metinfo.css          # MetInfo框架基础样式（含$first_color$变量）
│   └── metinfo.js           # MetInfo框架基础JS
├── js/                      # 自定义JS（如有）
├── ajax/                    # 异步加载模板片段
└── install/                 # 模板安装配置
```

---

## CSS 加载顺序（关键）

MetInfo框架自动加载顺序（无需在模板里手动引入）：

```
1. public/web/css/        ← 框架全局CSS（Bootstrap等）
2. public/fonts/          ← 图标字体（font-awesome、iconfont等）
3. templates/epgo-education/static/metinfo.css  ← 框架模板基础CSS
4. templates/epgo-education/css/epgo-education.css  ← 自定义核心样式
5. templates/epgo-education/css/animations.css  ← 动画
```

**图标字体来源**：框架自动注入 `public/fonts/` 下的字体，模板无需手动引入。
图标类名用法：`wb-*`（WebApp Icons）、`fa-*`（Font Awesome）、`icon`（基础类）。

---

## 已知问题和修复记录

### 问题1：PC端左侧/导航没有图标

**根因**：`head.php` 里用了 `<i class="icon wb-*">` 图标类，依赖框架注入的iconfont。
如果图标消失，检查：
1. `public/fonts/metinfo-admin-icon/` 字体文件是否存在
2. 框架 CSS 中 `@font-face` 声明是否正常
3. `static/metinfo.css` 第2173行前后的 `.wb-search:before` 是否有对应字体

**临时方案**：用 emoji 或 SVG 替代 `<i class="icon wb-*">` 标签。

### 问题2：子栏目标题/导航不显示

**根因**：`subcolumn_nav.php` 外层有条件判断 `$lang['tagshow_2']`，
后台「语言包 → 子栏目导航开关」未开启时整块不渲染。

**修复路径**：
- 后台路径：`系统 → 语言包管理 → 中文 → 前台栏目设置 → 开启子栏目导航`
- 或直接在 `subcolumn_nav.php` 第1行删除 `<if value="$lang['tagshow_2']">` 判断

**CSS位置**：`.met-column-nav` 样式在 `css/epgo-education.css` 末尾。

### 问题3：内容太少

纯内容问题，代码层无法解决。需要：
- 后台批量发布文章（或用 `fill_content.py` 脚本）
- 每个主栏目至少8-10篇文章才能支撑页面布局

---

## 参考模板：metv75

路径：`templates/metv75/`

metv75 是框架原生标准模板，结构与 epgo-education 一致，可参考：
- `metv75/news.php`：右侧边栏的子栏目列表结构（`.sidebar-column.list-icons`）
- `metv75/head.php`：图标用法示例
- `metv75/static/metinfo.css`：框架基础CSS（与epgo-education/static/metinfo.css内容相同）

---

## 色彩系统（epgo-education 主题）

```css
--color-primary:       #1E88E5   /* 主蓝 */
--color-primary-dark:  #1565C0   /* 深蓝（导航栏背景） */
--color-primary-light: #E3F2FD   /* 浅蓝（背景/标签） */
--color-success:       #43A047   /* 绿色 */
--color-warning:       #FB8C00   /* 橙色 */
--color-danger:        #E53935   /* 红色 */
--color-text:          #333333
--color-text-muted:    #757575
--color-border:        #EBEBEB
--color-bg:            #F7F8FA
```

导航栏硬编码：`background:#1565C0`（深蓝）

---

## 部署流程

```bash
# 本地修改后推到 GitHub
cd /Users/xiachaoqing/projects/epgo
git add templates/epgo-education/
git commit -m "fix: 描述修改内容"
git push

# 服务器拉取
ssh epgo "git -C /www/wwwroot/go.xiachaoqing.com pull"
# 注意：服务器上 go.xiachaoqing.com 目前没有 git，需要手动 rsync 或 scp
```

**当前同步方式（服务器无git）**：
```bash
rsync -avz /Users/xiachaoqing/projects/epgo/templates/epgo-education/ \
  epgo:/www/wwwroot/go.xiachaoqing.com/templates/epgo-education/
```

---

## 后续AI接手注意事项

1. **不要动 `static/metinfo.css`**：这是框架文件，MetInfo升级会覆盖，自定义样式只写在 `css/epgo-education.css`
2. **不要在 `head.php` 里手动引入CSS**：框架会自动加载 `css/` 目录下的文件
3. **图标用法**：`<i class="icon wb-XXX"></i>` 或 `<i class="fa fa-XXX"></i>`，图标名查 `public/fonts/` 下的字体文件
4. **MetInfo模板标签语法**：
   - 条件：`<if value="$var">...</if>`
   - 循环：`<tag action="news.list">...</tag>`
   - 变量：`{$c.met_webname}`
5. **子栏目导航**：修改 `subcolumn_nav.php`，样式在 `css/epgo-education.css` 的 `.met-column-nav` 部分
6. **首页大Banner**：在 `index.php` 里，框架的 `met-banner` 已被 `display:none` 隐藏，使用自定义 `.epgo-banner-wrap`
