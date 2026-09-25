# 英语陪跑GO AdSense 整改对照表

更新时间：2026-09-25

这份记录按 Google AdSense 官方说明整理，用来给后续维护者复核，不代表 Google 已经批准网站。

## 已完成

| Google 关注点 | 当前处理 | 验证方式 |
| --- | --- | --- |
| 原创、对用户有价值的内容 | KET/PET 核心文章统一为 Cathy 原创专题，保留自编例句、练习步骤和复盘方法 | 当前 sitemap 中 16 篇文章数据库 `publisher=Cathy`、`issue=原创专题` |
| 避免低价值和重复页面 | 13 篇旧重复专题保留访问但设置 `noindex,follow`，并从 sitemap 移除 | `templates/epgo-education/head.php` 与线上 sitemap |
| 清晰导航 | 移除数据库中的“会员中心”和“特色功能”前台栏目，保留数据不删除 | `ep_column.id=1`、`id=76` 的 `nav=0, isshow=0` |
| 隐私和服务说明 | 完善隐私政策、服务条款、儿童学习数据、Cookie、第三方 App 履约和删除申请说明 | `/privacy.html`、`/terms.html` |
| ads.txt | 已配置授权销售方记录 | `/ads.txt` HTTP 200 |
| sitemap 和站点所有权 | sitemap 可公网解析，站点可访问，HTML 可控 | `/sitemap.xml`、主题模板 |
| 非内容页面广告控制 | 测评、工具、搜索、反馈、下载等页面不加载 AdSense 脚本；文章和学习内容页按模板加载 | 线上 HTML 检查 `pagead2.googlesyndication.com` |

## 仍需人工确认

- 隐私政策中的实际运营主体名称、联系地址和隐私邮箱，应按真实备案主体、订单主体和支付凭证填写，不能虚构。
- 在 AdSense 后台确认提交的 URL 与实际站点一致，并查看 Policy Center 的具体拒绝原因。
- 广告上线后不要把广告放在测评提交按钮、工具操作按钮、导航或弹窗附近，也不要用文字诱导点击。
- 继续增加真实的家长问题、课堂观察和经过授权的学习案例，避免只发布模板化文章。

## 官方依据

- [让网站准备好加入 AdSense](https://support.google.com/adsense/answer/7299563?hl=zh-Hans)
- [AdSense 资格要求](https://support.google.com/adsense/answer/9724?hl=zh-Hans)
- [AdSense 未获批准时的常见内容问题](https://support.google.com/adsense/answer/81904?hl=zh-Hans)
- [AdSense 计划政策](https://support.google.com/adsense/answer/48182?hl=zh-Hans)
