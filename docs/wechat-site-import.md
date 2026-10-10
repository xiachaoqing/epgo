# 公众号文章导入网站说明

## 结论

公众号数据库 `we_articles` 只保存了 46 条发布记录的标题和摘要，正文不完整，不能作为网站导入源。公众号服务保留了微信官方历史文章接口，使用 `freepublish/batchget` 可以读取完整正文。最近一次只读检查返回 113 个图文集合、163 篇文章，正文均非空。

导入时使用的是公众号自有内容，保留真实的微信发布时间，清理微信专属属性和危险标签，添加作者与原文说明，再按 KET/PET/阅读/每日英语栏目映射到网站的 `ep_news`。同标题文章跳过，不覆盖网站已有内容；支付、账号开通、通知和评测流程不参与这个导入。

## 两步流程

在公众号服务器执行导出（使用正在运行服务的虚拟环境）：

```bash
cd /www/wwwroot/wechat_platform
venv/bin/python3 /path/to/fetch_wechat_history.py > /tmp/wechat-history.json
```

把 JSON 放到 EPGO 服务器后，先干跑：

```bash
python3 /path/to/import_wechat_history_to_epgo.py \
  --input /tmp/wechat-history.json
```

确认新增数量、标题和栏目后，再加 `--apply` 写入。脚本默认不写库，也不会删除或更新已有文章。

## 内容规则

- 作者字段统一为网站现有的「英语陪跑GO」，正文保留公众号作者名（通常是 Cathy）。
- 使用官方接口返回的真实更新时间，不人为平移日期。
- 网站版保留原文链接和原创说明，并增加入学测评、英语陪跑GO的站内入口。
- 不抓取其他公众号，不把外部爆文直接复制到站内。
- 导入完成后仍需抽查移动端图片、外链和文章目录；导入数量本身不代表 AdSense 一定通过。

## 站点地图

网站的 `sitemap.xml` 以前是手工维护的，文章增加后必须重新生成。使用
`scripts/generate_sitemap_from_epgo.py` 从 `ep_news` 和 `ep_column` 读取公开文章，
先输出到临时文件检查 URL 数量，再原子替换站点根目录的 `sitemap.xml`。
