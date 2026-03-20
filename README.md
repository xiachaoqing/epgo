# English Pacing Go (EPGO)

## 项目简介

English Pacing Go（英语陪跑GO）是一个面向英语学习者的在线教育平台，主要针对：
- KET（Key English Test）考试培训
- PET（Preliminary English Test）考试培训
- 英语学习资源分享
- 公众号推广和内容集成

## 技术栈

- **框架**: MetInfo CMS（PHP）
- **数据库**: SQLite（开发）/ MySQL（生产）
- **前端**: HTML/CSS/JavaScript
- **部署**: Nginx + PHP-FPM + Baota Panel

## 环境配置

### 本地开发

1. Clone 项目
```bash
git clone git@github.com:xiachaoqing/epgo.git
cd epgo
```

2. 配置数据库（在 `config/config_db.php`）
```php
con_db_name = "epgo_db"
tablepre    = "ep_"
```

3. 启动开发服务器
```bash
php -S localhost:8000
```

### 生产部署

- **服务器**: 101.42.21.191
- **部署目录**: /www/wwwroot/go.xiachaoqing.com/
- **域名**: go.xiachaoqing.com
- **数据库**: MySQL (epgo_db)

## 项目结构

```
epgo/
├── admin/          # 后台管理
├── app/            # 应用模块
├── config/         # 配置文件
├── download/       # 下载资源
├── img/            # 图片资源
├── member/         # 会员系统
├── news/           # 新闻/文章
├── product/        # 产品/课程
├── upload/         # 用户上传文件
└── index.php       # 入口文件
```

## 内容结构（EPGO规划）

- **首页**: 英语学习资源汇总
- **KET栏目**: KET考试真题、词汇、教程
- **PET栏目**: PET考试真题、词汇、教程
- **资源下载**: 学习材料、练习题
- **新闻资讯**: 英语学习技巧、考试动态
- **公众号**: 推广 "英语陪跑GO" 微信公众号

## Google AdSense 集成

- 广告位规划：顶部、侧边栏、文章末尾
- 内容优化：高质量教育内容，吸引评测/教程类流量
- SEO优化：目标关键词 KET、PET 等

## 部署命令参考

```bash
# 在101.42.21.191上
ssh root@101.42.21.191

# 部署步骤
cd /www/wwwroot
git clone git@github.com:xiachaoqing/epgo.git go.xiachaoqing.com
cd go.xiachaoqing.com

# 复制数据库
cp config/metinfo.db config/metinfo.db.backup
# 在宝塔中配置新网站和数据库
```

## 维护

- 定期更新英语学习内容
- 监控Google Analytics和AdSense数据
- 优化内容以提高点击率
- 更新SEO优化

## 许可证

Private Project
