# 英语陪跑 GO 开发交接文档

更新日期：2026-09-20  
当前分支：`main`  
当前提交：`d12a154 feat: 接入自托管平台媒体工具`

这份文档给下一位 AI 或开发者使用。先读本文件，再读 [`docs/EPGO_入学测评与交接说明.md`](docs/EPGO_入学测评与交接说明.md)。不要把支付链路、第三方 App 账号开通流程和入学测评混在一起修改。

## 一、项目定位与边界

这是英语陪跑 GO 的静态网站项目，服务对象是孩子和家长。网站现有购买页、入学测评、工具集合和公众号引导。英语陪跑 GO App 是第三方产品，网站没有 App 运营接口；不要假设网站可以自动创建 App 账号、同步 App 作业或查询 App 订单。

本阶段的原则：

- 测评和工具页面可以独立迭代。
- 购买页的价格、套餐、订单请求、微信 OAuth、支付 SDK、支付结果和账号开通流程保持不变。
- 本地文件工具默认在浏览器内处理，不上传文件。
- 平台视频解析只有在用户主动提交链接并确认有权处理时才调用服务端。
- 不把未验证的平台能力写成“所有链接都支持”。

## 二、当前已经完成

### 1. 入学测评

入口：`/epgo/assessment.html`

- 当前开放 KET 入学初筛，29 道客观题，满分 29 分。
- 支持草稿保存、恢复、计时、漏答提示、评分、分项成绩和结果报告。
- 支持打印/保存题本 PDF。
- 支持本机选择照片或 PDF 做答题卡文件检查，但没有上传服务器，也没有 OCR 自动判分。
- 结果页可以进入现有 App 套餐购买页；测评本身不创建订单。
- PET/FCE 题库仍处于校对状态，不要直接开放。

详细题库、评分规则和已知问题见 `docs/EPGO_入学测评与交接说明.md`。

### 2. 工具集合

入口：`/epgo/tools.html`

已完成的本地工具：

- 学习日历：添加、完成、删除、按日期查看。
- 英语备忘录：错题、生词、老师点评、复习日期、搜索和删除。
- 我的单词本：添加、搜索、标记掌握和删除。
- 专注计时器：15/25/45 分钟、开始、暂停、重置。
- 测评报告：读取当前浏览器保存的测评结果，只读展示。
- 一寸证件照：本地图片裁剪、缩放和 JPG 下载。
- 图片压缩：本地调整质量和最长边并下载。
- 视频画面提取：本地上传视频，按时间点截取 JPG。

页面已按手机、平板、PC 做响应式布局，工具入口在手机端为两列，表单会自动变为单列。

### 3. 平台视频解析

前端入口仍在 `epgo/tools.html` 的“平台视频提取”卡片。

调用链：

```text
浏览器
  -> POST /epgo/media-api.php
  -> PHP 校验请求、白名单域名和授权确认
  -> http://127.0.0.1:9000/（服务器本机 Cobalt）
  -> 返回 redirect / tunnel / picker
  -> 浏览器打开短时下载地址
```

当前服务器使用 `ghcr.io/imputnet/cobalt:11`，容器名为 `epgo-cobalt`，只监听 `127.0.0.1:9000`，外部通过 Nginx 的 `/epgo/cobalt/` 访问。

当前页面标记为已接入的方向：B 站、TikTok、Instagram、YouTube。抖音、快手、小红书只做域名识别，页面标记为“待适配”，不要把它们宣传成已经可用。Cobalt 的服务支持会随版本和平台规则变化，真实链接仍需逐个平台验证。

服务端限制：

- 只接受 `http/https`，拒绝带用户名密码的 URL。
- PHP 只接受白名单域名。
- 前端要求用户确认拥有内容处理权或已经获得授权。
- Cobalt 配置了请求频率、时长和临时 tunnel 限制。
- PHP 不代理媒体字节，也不建立长期内容库。
- API 密钥不放在浏览器；线上密钥位于站点目录隐藏文件，权限为 600，并由 Nginx 精确返回 404。

部署配置和密钥格式见 [`deploy/cobalt/README.md`](deploy/cobalt/README.md) 与 [`deploy/cobalt/docker-compose.yml`](deploy/cobalt/docker-compose.yml)。真实 `keys.json`、`media-api-key.txt` 不得提交 Git。

## 三、线上环境

- 线上站点：`https://go.xiachaoqing.com/epgo/`
- 工具页：`https://go.xiachaoqing.com/epgo/tools.html`
- 测评页：`https://go.xiachaoqing.com/epgo/assessment.html`
- 生产 SSH 别名：`epgo`
- 网站根目录：`/www/wwwroot/go.xiachaoqing.com/`
- Nginx 配置：`/www/server/panel/vhost/nginx/go.xiachaoqing.com.conf`
- Cobalt Compose 目录：`/opt/epgo-cobalt/`
- PHP 运行时：PHP 7.2，受 `open_basedir` 限制

线上已验证：

- 本地工具页和 `media-api.php` 的线上 SHA-256 与仓库文件一致。
- `docker compose ps` 显示 `epgo-cobalt` 持续运行，重启次数为 0。
- Cobalt 健康接口返回 200。
- `media-api.php` 的 GET 返回预期 405。
- 非白名单域名返回 400。
- 密钥 URL 返回 404。
- 一个公开 YouTube 测试链接已到达 Cobalt，但上游返回 `error.api.fetch.fail`；这证明调用链通了，不证明该平台在当前服务器网络下可稳定抓取。

## 四、关键文件

| 文件 | 用途 |
| --- | --- |
| `epgo/index.html` | 现有购买页；支付逻辑属于敏感边界 |
| `epgo/assessment.html` | KET 测评、评分、报告和购买 CTA |
| `epgo/tools.html` | 工具集合和平台视频解析前端 |
| `epgo/media-api.php` | PHP 7.2 同源媒体代理 |
| `epgo/logo.png` / `epgo/favicon.ico` | 统一品牌图标 |
| `epgo/share.jpg` | 微信/Open Graph 分享图 |
| `scripts/test_assessment_flow.cjs` | 测评 Chromium 回归脚本 |
| `scripts/test_tools_flow.cjs` | 工具 Chromium 回归脚本，已加入平台解析负向测试 |
| `docs/EPGO_入学测评与交接说明.md` | 测评、工具和购买隔离的详细说明 |
| `deploy/cobalt/` | Cobalt Compose、部署说明和忽略规则 |

## 五、测试与运行方式

PHP 和内嵌 JavaScript 可先执行：

```bash
php -l epgo/media-api.php
git diff --check
```

如果环境安装了 Playwright，再执行：

```bash
node scripts/test_assessment_flow.cjs /path/to/node_modules/playwright
node scripts/test_tools_flow.cjs /path/to/node_modules/playwright
```

工具回归覆盖日历、备忘录、单词本、计时器、测评报告、证件照、图片压缩、平台链接识别、待适配平台提示和媒体接口错误展示。当前交接时没有在本机重新跑完整 Chromium 回归，因为项目环境没有可用的 `playwright` npm 模块；不要把语法检查当成浏览器回归。

线上只做只读健康检查时可使用：

```bash
ssh epgo 'cd /opt/epgo-cobalt && docker compose ps'
ssh epgo 'nginx -t'
curl -i https://go.xiachaoqing.com/epgo/media-api.php
```

修改 Nginx 或 Compose 前先备份线上文件，修改后必须执行 `nginx -t`，再 reload。不要在命令输出、文档或 Git 中打印 API 密钥。

## 六、尚未完成与建议顺序

### 第一优先级：真实平台验收

收集 B 站、TikTok、Instagram、YouTube 的公开测试链接，逐个平台记录成功、`redirect`、`tunnel`、`picker`、上游失败和超时。不要只用首页链接判断成功；需要使用真实公开视频页。

### 第二优先级：抖音等平台适配决策

抖音、快手、小红书不能因为域名识别成功就算完成。先确认官方开放能力、授权范围和内容权利，再选择官方接口或单独适配器。若使用第三方下载器，必须单独审查许可证、平台条款、服务器网络和缓存策略。

### 第三优先级：工具转化链路

先保持工具免费，观察访问量、使用工具后测评点击率、测评完成率、套餐点击率和 App 购买转化。确认有稳定使用后，再考虑微信身份、云端保存、限额、会员或报告收费。不要先把工具和现有支付订单混在一起。

### 第四优先级：测评升级

可做受保护的答题卡上传和教师复核，但需要独立上传接口、文件大小/类型限制、隐私说明、教师权限和删除策略。当前本机照片/PDF 选择只是预览，不能直接改成“自动验证成绩”。

## 七、禁止事项

- 不要把第三方 App 账号自动开通写进网站逻辑；App 没有开放接口。
- 不要修改购买页的支付字段、套餐价格、OAuth 回调和订单状态机，除非先单独审计。
- 不要提交线上 API 密钥、服务器密码、真实用户数据或原始答案资料。
- 不要把抖音、快手、小红书标成“已支持”，除非完成真实链接验收并确认合规方案。
- 不要因为一次 Cobalt 200 响应就声称所有平台下载成功。

