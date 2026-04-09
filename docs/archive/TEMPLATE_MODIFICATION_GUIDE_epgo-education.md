# epgo-education 模板修改说明（供后续 AI 接手）

## 1. 本次修改目标
- 修复首页顶部导航点击异常
- 保留 `epgo-education` 当前样式，不回退为 `metv75`
- 仅修当前模板实际问题，不整体重构

## 2. 本次已确认的问题与结论

### 2.1 导航点击异常
现象：
- `KET/PET` 可点击且可下拉
- `英语阅读`、`关于我们` 点击异常，曾表现为无反应或回到首页

结论：
- 不是数据库缺链接
- 不是栏目缺父级
- 不是 `about` 单页模块导致
- 问题集中在 `templates/epgo-education/head.php` 的导航链接输出与下拉结构适配

### 2.2 KET/PET 子栏目白条问题
现象：
- 下拉菜单出现白条，子栏目未显示

结论：
- 当前模板内原始 `type='son'` 在该场景下没有稳定输出子栏目
- 已改为当前模板内显式输出 KET/PET 子栏目列表

## 3. 已修改文件

### 3.1 `templates/epgo-education/head.php`
已做的修改：
- 首页导航改为稳定输出 `/`
- 一级栏目统一显式输出稳定 `href`
- 保留当前模板样式
- KET/PET 在当前模板中显式输出下拉子栏目：
  - KET真题解析 `/ket-exam/list-111.html`
  - KET词汇速记 `/ket-word/list-112.html`
  - KET写作指导 `/ket-write/list-113.html`
  - KET听力技巧 `/ket-listen/list-114.html`
  - PET真题解析 `/pet-exam/list-121.html`
  - PET词汇速记 `/pet-word/list-122.html`
  - PET写作指导 `/pet-write/list-123.html`
  - PET阅读技巧 `/pet-read/list-124.html`
- 下拉菜单样式做了最小增强，避免空白白条

注意：
- 不要再把整个头部回滚到 `metv75`
- 不要再把导航改成 fixed/sticky 独立头部，那次改动会破坏首页头图区布局
- 不要再全局统一所有一级导航点击 JS，这会误伤 KET/PET 下拉

### 3.2 `templates/epgo-education/static/metinfo.js`
当前处理原则：
- 保留 dropdown 的 hover/open 行为
- 不再对所有一级导航做统一 click 劫持
- 当前版本已经撤回那次误伤 KET/PET 的 click 统一绑定

## 4. 当前首页链接复查结果
复查时间：本次会话

### 已确认正常
- 首页顶部主导航：
  - `/`
  - `/ket/`
  - `/pet/`
  - `/reading/`
  - `/speech/`
  - `/daily/`
  - `/download/`
  - `/about/`

### 当前仍建议后续处理
首页中仍存在以下相对路径链接：
- `ket-exam/list-111.html`
- `ket-word/list-112.html`
- `ket-write/list-113.html`
- `ket-listen/list-114.html`
- `pet-exam/list-121.html`
- `pet-word/list-122.html`
- `pet-write/list-123.html`
- `pet-read/list-124.html`

说明：
- 这些多半出现在首页内容区快捷入口，不是顶部主导航
- 后续优化首页时建议统一替换为绝对站内路径 `/xxx/...`

另有一个空链接：
- 空文本 + 空 href

后续优化首页时建议顺手清理。

## 5. 后续修改约束（非常重要）
1. 优先改当前模板，不要直接回退 `metv75`
2. 不要用“大范围样式覆盖”来猜问题
3. 不要把导航整体 click 逻辑全局接管
4. 修改导航前先读：
   - `templates/epgo-education/head.php`
   - `templates/epgo-education/static/metinfo.js`
5. 修改首页前先检查最终 HTML 输出，而不是只看模板源码
6. 首页文章、封面图、栏目内容优先走数据库和现有内容结构，不要盲目新建冗余模板

## 6. 下一步建议
1. 清理首页内容区相对路径链接
2. 删除非英语相关文章
3. 扩充英语相关文章数量
4. 替换默认封面图
5. 优化首页模块内容与排版
6. 补全“关于我们”页面内容

## 7. 导航修复补充说明（后续 AI 必看）
最近再次核对 `metv75` 后确认：
- `metv75` 的普通一级导航栏目，写法是原生：`href="{$m.url}" {$m.urlnew}`
- 只有“有子栏目”的一级栏目才走 dropdown 分支

因此当前 `epgo-education` 后续修导航时，原则应为：
- `KET/PET`：保留当前手工子栏目输出
- `英语阅读 / 英语演讲 / 每日英语 / 资料下载 / 关于我们`：恢复为 `metv75` 原生普通链接写法
- 不要再对普通一级栏目手工拼 `$_nav_url`，这很可能会破坏当前模板与前端脚本的原生配合方式
