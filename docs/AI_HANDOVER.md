# 英语陪跑 GO 前端交接文档

最后更新：2026-11-16

## 代码源

- 本地：`/Users/xiachaoqing/projects/epgo`
- Git：`git@github.com:xiachaoqing/epgo.git`
- 线上：`/www/wwwroot/go.xiachaoqing.com`
- 当前前端提交：`3337be6 align listening guide with weekly review flow`

公众号后端不在本仓库，使用独立项目：

`/Users/xiachaoqing/projects/wechat-platform`

后端 Git：`git@github.com:xiachaoqing/wechat-platform.git`

## 熏听页面

- 主页面：`/epgo/listening/`
- 说明页：`/epgo/listening/guide/`
- 主页面负责方案展示、微信支付入口、公众号咨询和 App 权益说明。
- 说明页负责痛点、计划示例、陪跑流程、设备说明和 FAQ。
- 公众号菜单只放“熏听陪跑”，不单独放“熏听说明”。
- “熏听说明”通过主页面内部链接和公众号自动回复访问。

## 当前宣传口径

- 品牌：Cathy 熏听陪跑营
- 3 个月：¥1299
- 6 个月：¥1999
- 购买熏听陪跑营包含服务期内英语陪跑 GO App 学员端使用权限。
- 支付成功后由人工确认孩子信息并开通第三方 App。
- 不承诺考试通过、固定提分或固定学习结果。

## 前端发布

```bash
cd /Users/xiachaoqing/projects/epgo
git pull --ff-only origin main
# 修改、检查、提交、推送
git add .
git commit -m "说明修改内容"
git push origin main
```

当前页面部署后应检查：

```bash
curl -I https://go.xiachaoqing.com/epgo/listening/
curl -I https://go.xiachaoqing.com/epgo/listening/guide/
```

不要直接在服务器改前端文件；需要改动时先改本地 Git，再部署。
