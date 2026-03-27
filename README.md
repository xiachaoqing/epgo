# 英语陪跑GO — epgo 项目

网站：https://xiachaoqing.com
服务器：101.42.21.191
模板：`templates/epgo-education/`

---

## 接手必读

**动任何文件前，先读：[docs/DEV_GUIDE.md](docs/DEV_GUIDE.md)**

重点章节：
- § 二：MetInfo 模板语法（**不是普通 PHP/HTML**）
- § 三：metinfo.inc.php 配置（**配错整站白屏**）
- § 四：数据库表结构
- § 七：部署流程
- § 八：常见错误排查
- § 九：哪些文件不能动

---

## 快速上手

```bash
# 修改完模板文件后，三步部署
git push origin main
ssh root@101.42.21.191 "cd /www/wwwroot/go.xiachaoqing.com && git pull origin main"
ssh root@101.42.21.191 "rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/"
```

---

## 目录结构

```
epgo/
├── templates/epgo-education/   前端模板（主要工作在这里）
│   ├── head.php                导航
│   ├── foot.php                页脚
│   ├── index.php               首页
│   ├── shownews.php            文章详情
│   ├── news.php                文章列表
│   ├── css/epgo-education.css  自定义样式
│   └── metinfo.inc.php         引擎配置（必须有 template_type=tag）
├── docs/
│   └── DEV_GUIDE.md            ← 开发规范（接手必读）
└── scripts/                    服务器端维护脚本
```
