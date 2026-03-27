# 英语陪跑GO — 前端模板交接文档

> 写给下一个 AI：请从头到尾读完，再动任何文件。能力有限请谨慎，宁可少做不要乱改。

---

## 一、项目基本情况

| 项目 | 说明 |
|------|------|
| 网站 | https://xiachaoqing.com |
| CMS | MetInfo（PHP框架，有自己的模板语法，**不是普通HTML**） |
| 模板路径 | `/templates/epgo-education/` |
| 参照模板 | `/templates/metv75/`（官方自带，**遇到问题先看这个**） |
| 备案号 | 京ICP备2020039465号-1（必须出现在页脚） |

---

## 二、MetInfo 模板语法——必读，否则必出错

这是最重要的一节。MetInfo 不是普通PHP，有自己的标签系统：

```php
// 输出变量
{$data.title}          // 文章标题
{$data.content}        // 文章正文 HTML
{$data.updatetime}     // 更新时间
{$data.hits}           // 阅读数
{$data.issue}          // 所属栏目名
{$data.class1}         // 栏目ID
{$c.index_url}         // 网站根URL（含末尾斜杠）
{$c.met_webname}       // 网站名称
{$c.met_logo}          // Logo 图片URL
{$v.imgurl|thumb:400,200}  // 图片缩略图（宽x高）

// 条件
<if value="$data['imgurl']">有图内容</if>
<if value="$data['imgurl']">有图<else/>无图</if>

// 循环列表
<tag action='list' type='news' cid="$data['class1']" num="6">
  <a href="{$v.url}">{$v.title}</a>
</tag>

// 栏目分类导航
<tag action='category' cid="$data['releclass1']">
  <a href="{$m.url}">{$m.name}</a>
</tag>

// 内置功能标签
<tag action="search.column"></tag>   // 搜索框
<pagination/>                         // 分页（PC）
<pager/>                              // 加载更多（移动端）
<include file="head.php" />           // 引入子模板
<met_meta page="$met_page" />         // 页面 meta 标签（放 head.php 顶部）
<met_foot />                          // 框架脚部JS（放 foot.php 末尾）
```

**禁止事项：**
- 不要用普通PHP `echo`/`foreach` 替代上面的标签
- 不要乱改 `<met_meta>` 和 `<met_foot />` 的位置
- 不要随意增删 `m-id` 属性（框架用来识别内容区域）

---

## 三、模板文件说明

```
templates/epgo-education/
├── head.php          导航栏 + CSS + 微信SDK
├── foot.php          页脚 + <met_foot /> + 全局JS
├── index.php         首页
├── news.php          栏目列表页（分类页）
├── shownews.php      文章详情页 ← 最重要，最多问题
├── ajax/news.php     列表页文章卡片（AJAX加载）
├── para_search.php   搜索框模板
└── css/
    └── epgo-education.css   自定义样式（只用 epgo- 前缀）
```

---

## 四、详情页（shownews.php）——已知关键问题与修复

### 核心问题：文章内容不显示

**原因**：MetInfo 框架通过 `m-id="noset"` 属性识别主内容区域。没有这个属性，框架不注入文章数据，页面显示空白。

**必须保持的结构**（不能修改）：

```php
<main class="met-shownews animsition">
  <div class="container">
    <div class="row">
      <div class="clearfix">                          <!-- 必须有 clearfix -->

        <div class="col-md-9 met-shownews-body" m-id="noset">  <!-- m-id="noset" 关键！ -->
          <div class="row">
            <!-- 文章内容放这里 -->
            <section class="details-title border-bottom1">
              <h1 class="m-0">{$data.title}</h1>
              ...
            </section>
            <section class="met-editor clearfix">
              {$data.content}                         <!-- 正文必须用 met-editor 类 -->
            </section>
            <pagination/>
          </div>
        </div>

        <div class="col-md-3">                        <!-- 侧栏 -->
          <aside class="met-sidebar" m-id="news_bar" m-type="nocontent">
            ...
          </aside>
        </div>

      </div>
    </div>
  </div>
</main>
```

遇到详情页问题，先核对以上结构再改其他。

---

## 五、Logo 四个角黑点问题

**现象**：Logo 图片四个角有黑色小点（选择控制点）。

**原因**：浏览器对可编辑/可选中图片显示 selection handle，或 `outline` 属性未清除。

**修复**（已在 head.php 内 `<style>` 中写入，不要删）：

```css
.met-logo,
.met-logo .vertical-align,
.met-logo .vertical-align-middle {
  outline: none !important;
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
}
.met-logo img {
  outline: none !important;
  border: none !important;
  box-shadow: none !important;
  display: block;
}
img::selection { background: transparent; }
```

如果上线后还有黑点，检查 Logo 图片本身：`docs/图标.png` — 这是用户提供的原始图，**图片文件本身四角有黑色装饰**（不是CSS问题）。需要用户提供去掉黑角的新版图标。

---

## 六、导航下拉菜单

下拉菜单样式在 `head.php` 内 `<style>` 块写死，当前样式：白色圆角卡片 + 淡入动画。

**注意**：导航链接 URL 是硬编码在 `head.php` 里的（不是从数据库动态读取），如果后台新增栏目，必须手动在 head.php 的 `<ul class="nav navbar-nav navlist">` 里加 `<li>`。

当前导航结构：
```
首页 | KET备考(下拉) | PET备考(下拉) | 英语阅读 | 英语演讲 | 每日英语 | 资料下载 | 关于我们
```

---

## 七、CSS 规范

- 自定义样式全部写在 `css/epgo-education.css`
- **只用 `epgo-` 前缀**，不要覆盖框架原有 class（`.met-*`、`.navbar`、`.btn` 等）
- 颜色变量定义在 `:root` 里，修改主色只改 `--epgo-blue: #2563EB`
- 框架有自己的 CSS 缓存机制，样式改后可能需要到 MetInfo 后台清除缓存

---

## 八、资源文件位置

| 文件 | 位置 | 说明 |
|------|------|------|
| 网站图标 | `docs/图标.png` | 用户提供，当前Logo |
| 公众号二维码 | `docs/微信公众号二维码.png` | 页脚展示用 |
| 部署脚本 | `docs/deploy.sh` | 参考用，不直接执行 |

---

## 九、未完成 / 待处理事项

1. **Logo 黑点（图片本身问题）**：`docs/图标.png` 原图四角有黑色装饰元素，需要用户提供干净版本
2. **首页轮播图**：用户提出要加，尚未实现。推荐用 MetInfo 自带的 `<tag action='banner'>` 标签，参考 metv75/index.php
3. **微信分享签名**：当前分享是弹窗提示手动分享，完整签名需要后端 API（服务器在 wechat.xiachaoqing.com）
4. **FCE 备考栏目**：用户提到缺失，需确认 MetInfo 后台是否已建该栏目，建完后在 head.php 导航手动加链接
5. **图片素材**：文章列表页图片缩略图依赖文章在 MetInfo 后台上传图片，当前文章可能缺图

---

## 十、公众号文章（另一个项目）

**注意：公众号文章和这个网站是两个独立项目！**

| 项目 | 路径 |
|------|------|
| 网站前端模板 | `/Users/xiachaoqing/projects/epgo/` |
| 公众号后端 | `/Users/xiachaoqing/projects/openclaw_file/` |

公众号发文章的正确方式（不要自己写脚本绕过）：

```bash
# 服务器上运行：
VENV="/www/wwwroot/wechat_platform/venv/bin/python3"
SKILL="/root/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/public/article-writer/scripts/article_writer.py"
$VENV $SKILL --topic "今日选题" --style 干货 --auto-push
```

文章格式规范看：`/Users/xiachaoqing/projects/openclaw_file/docs/13-文章格式规范.md`

今天（周六）应该写的类型：**周六·家长等娃内容**，约600字，标题公式：`《[情绪词]+[具体场景或对比]》`

---

## 十一、同步到服务器

**两台服务器，不要搞混：**

| 别名 | IP | 用途 |
|------|-----|------|
| `epgo` | 101.42.21.191 | **网站服务器**（MetInfo，改模板这里） |
| `openclaw` | 39.105.154.244 | 公众号后端（wechat_platform） |

网站根目录：`/www/wwwroot/go.xiachaoqing.com/`

```bash
# 同步单个模板文件
scp templates/epgo-education/shownews.php epgo:/www/wwwroot/go.xiachaoqing.com/templates/epgo-education/

# 同步后必须清除MetInfo模板缓存！
ssh epgo 'rm -f /www/wwwroot/go.xiachaoqing.com/cache/templates/*.php'

# 数据库连接（在epgo服务器上）
mysql -h 127.0.0.1 -u xiachaoqing -p***REMOVED*** epgo_db
# 表前缀是 ep_（如 ep_news, ep_column, ep_flash）
```

**Nginx伪静态规则**（重要，已修复，不要乱改）：
文件：`/www/server/panel/vhost/rewrite/go.xiachaoqing.com.conf`
- `/栏目名/数字.html` → `news/shownews.php?id=数字`（详情页）
- 其他 → `news/index.php`（列表页）

**轮播图管理**：图片存在 `ep_flash` 表，用 `scripts/fetch_banners.py` 脚本管理。

---

## 十二、遇到问题的排查顺序

1. 先看 `templates/metv75/` 对应文件的写法
2. 检查 MetInfo 标签拼写（大小写敏感）
3. 检查 `m-id` 属性是否存在
4. 清除 MetInfo 后台缓存
5. 清除浏览器缓存（Ctrl+Shift+Delete）
6. 看浏览器 Console 有无 JS 报错

---

最后更新：2026-03-21
