# EPGO项目 - Git工作流完全指南

> 最后更新：2026-03-21

---

## 📌 项目信息

| 项目 | 值 |
|------|-----|
| **项目名称** | EPGO - 英语陪跑GO |
| **Git仓库** | git@github.com:xiachaoqing/epgo.git |
| **主分支** | main |
| **部署服务器** | 阿里云ECS (39.105.154.244) |
| **部署路径** | /www/wwwroot/epgo (根据实际调整) |

---

## 🔄 完整的开发到部署流程

### 步骤1：克隆仓库（第一次）

```bash
# 克隆项目
git clone git@github.com:xiachaoqing/epgo.git
cd epgo

# 查看分支和远程
git branch -a
git remote -v
```

输出示例：
```
* main                 3a4c257 [origin/main] feat: 添加英文演讲视频播放功能...
  remotes/origin/main  3a4c257 feat: 添加英文演讲视频播放功能...
origin  git@github.com:xiachaoqing/epgo.git (fetch)
origin  git@github.com:xiachaoqing/epgo.git (push)
```

### 步骤2：创建本地分支（推荐）

虽然本项目主要用main分支，但为了安全，建议创建特性分支：

```bash
# 创建新分支（功能分支）
git checkout -b feature/首页优化

# 或创建修复分支
git checkout -b fix/移动端菜单对齐

# 或创建文档分支
git checkout -b docs/内容填充指南
```

**分支命名规范**：
- `feature/功能名` - 新增功能
- `fix/问题名` - 修复bug
- `docs/文档名` - 文档更新
- `style/样式名` - 样式优化
- `refactor/重构名` - 代码重构

### 步骤3：做出改动

在本地编辑文件，例如修改首页：

```bash
# 查看修改了哪些文件
git status

# 查看具体修改内容
git diff templates/epgo-education/index.php

# 查看某个文件的修改历史
git log --oneline templates/epgo-education/index.php
```

### 步骤4：暂存改动

```bash
# 暂存单个文件
git add templates/epgo-education/index.php

# 暂存特定目录
git add templates/epgo-education/css/

# 暂存所有改动
git add -A

# 查看已暂存的内容
git status
```

### 步骤5：提交改动

```bash
# 标准commit格式
git commit -m "feat: 添加英文演讲视频播放功能"

# 详细commit（带描述）
git commit -m "feat: 添加英文演讲视频播放功能

- 新增speech.php视频播放页面
- 支持YouTube/优酷/Vimeo嵌入
- 添加视频分类筛选功能
- 优化移动端视频显示"

# 修正上一个commit
git commit --amend -m "新的commit信息"

# 查看commit历史
git log --oneline -10
```

**Commit消息规范**：

```
feat: 添加新功能 (特性)
fix: 修复bug
style: 样式优化 (不影响代码逻辑)
refactor: 重构代码
docs: 文档更新
perf: 性能优化
chore: 构建或依赖调整
test: 测试相关
ci: CI/CD相关

格式示例:
feat: 添加用户登录功能
^--- 类型
      ^--- 简短描述 (50字以内)

可选的详细描述:
- 改动1
- 改动2
```

### 步骤6：推送到GitHub

```bash
# 推送当前分支
git push origin feature/首页优化

# 推送main分支
git push origin main

# 推送所有分支
git push origin --all

# 首次推送新分支时加-u参数
git push -u origin feature/首页优化
```

### 步骤7：创建Pull Request（可选但推荐）

如果在特性分支上工作，建议创建PR来审查：

```bash
# 1. 访问GitHub项目页面
https://github.com/xiachaoqing/epgo

# 2. 点击"Compare & pull request"按钮
# 3. 填写PR标题和描述
# 4. 点击"Create pull request"

# 或使用命令行工具（需要安装gh）
gh pr create --title "添加首页优化" --body "改进首页布局和样式"
```

### 步骤8：服务器拉取并部署

**本地确认无误后**，在服务器执行：

```bash
# 1. SSH登录服务器
ssh root@39.105.154.244

# 2. 进入项目目录
cd /www/wwwroot/epgo

# 3. 拉取最新代码
git pull origin main

# 4. 查看git状态
git status

# 5. 检查改动的文件
git diff HEAD~1

# 6. 清除MetInfo缓存（重要！）
# 登录MetInfo后台，系统设置 → 缓存管理 → 清空所有缓存

# 7. 验证页面效果
curl -s http://localhost/index.php | head -20
```

---

## 📋 常用命令速查表

### 查看和对比

```bash
# 查看当前分支和状态
git status

# 查看所有分支
git branch -a

# 查看最近的commits
git log --oneline -10

# 查看特定文件的改动历史
git log --oneline templates/epgo-education/index.php

# 对比工作区和暂存区
git diff

# 对比暂存区和HEAD
git diff --cached

# 对比两个commit
git diff a1b2c3d..e4f5g6h

# 对比两个分支
git diff main feature/优化
```

### 撤销和回滚

```bash
# 放弃工作区的改动
git checkout -- templates/epgo-education/index.php

# 放弃所有工作区改动
git checkout -- .

# 取消暂存
git reset templates/epgo-education/index.php

# 回到上一个commit（保留改动）
git reset --soft HEAD~1

# 回到上一个commit（丢弃改动）
git reset --hard HEAD~1

# 撤销已push的commit（创建新commit）
git revert a1b2c3d
```

### 分支操作

```bash
# 创建分支
git branch feature/新功能

# 切换分支
git checkout feature/新功能

# 创建并切换分支
git checkout -b feature/新功能

# 删除本地分支
git branch -d feature/旧功能

# 删除远程分支
git push origin --delete feature/旧功能

# 重命名分支
git branch -m old-name new-name

# 合并分支到main
git checkout main
git merge feature/新功能
```

### 远程操作

```bash
# 查看远程配置
git remote -v

# 添加远程仓库
git remote add origin git@github.com:xiachaoqing/epgo.git

# 修改远程URL
git remote set-url origin git@github.com:xiachaoqing/epgo.git

# 拉取远程更新（不合并）
git fetch origin

# 拉取并合并
git pull origin main

# 推送到远程
git push origin main

# 推送所有分支
git push --all

# 删除远程分支
git push origin --delete feature/旧功能
```

---

## 🚨 常见问题与解决方案

### 问题1：忘记commit就切换分支了

```bash
# 保存当前改动到临时存储
git stash

# 切换分支
git checkout main

# 回到原分支后恢复改动
git checkout feature/优化
git stash pop
```

### 问题2：commit提交了但想修改内容

```bash
# 如果还没push
git commit --amend -m "新的消息"

# 如果已经push
git revert a1b2c3d  # 创建新commit来撤销
# 或强制push（⚠️ 谨慎使用）
git push origin main --force-with-lease
```

### 问题3：不小心删除了本地分支

```bash
# 查看reflog找回删除的分支
git reflog

# 恢复分支
git checkout -b recovered-branch abc123d
```

### 问题4：拉取时出现冲突

```bash
# 查看冲突的文件
git status

# 打开冲突文件，手动解决冲突标记
# 冲突标记示例：
# <<<<<<< HEAD
# 本地改动
# =======
# 远程改动
# >>>>>>> origin/main

# 解决完后
git add 冲突文件
git commit -m "fix: 解决merge冲突"
git push origin main
```

### 问题5：推送被拒绝（远程有其他人的改动）

```bash
# 先拉取最新代码
git pull origin main

# 解决可能的冲突（同问题4）

# 再推送
git push origin main
```

---

## 🔐 SSH密钥配置（如果还没做）

### 生成密钥对

```bash
# 生成新的SSH密钥
ssh-keygen -t rsa -b 4096 -C "xiachaoqing@example.com"

# 按提示输入文件位置（默认: ~/.ssh/id_rsa）
# 按提示输入密码（可以为空）
```

### 添加到GitHub

```bash
# 复制公钥
cat ~/.ssh/id_rsa.pub

# 1. 访问 https://github.com/settings/keys
# 2. 点击 "New SSH key"
# 3. 粘贴公钥内容
# 4. 点击 "Add SSH key"
```

### 测试连接

```bash
ssh -T git@github.com

# 输出应该是:
# Hi xiachaoqing! You've successfully authenticated...
```

---

## 📊 项目提交统计

```bash
# 查看所有提交者的统计
git shortlog -sne

# 查看自己的提交数
git shortlog -sne | grep "Your Name"

# 查看最近一周的提交
git log --since="1 week ago" --oneline

# 查看某个文件的贡献者
git blame templates/epgo-education/index.php
```

---

## 🎯 完整的工作流示例

### 场景：优化首页样式

```bash
# 1. 更新main分支
git checkout main
git pull origin main

# 2. 创建特性分支
git checkout -b feature/首页样式优化

# 3. 编辑文件
# 编辑 templates/epgo-education/css/epgo-education.css
# 编辑 templates/epgo-education/index.php

# 4. 检查改动
git status
git diff

# 5. 暂存改动
git add templates/epgo-education/css/epgo-education.css
git add templates/epgo-education/index.php

# 6. 提交
git commit -m "style: 优化首页样式和布局

- 增加gradient渐变背景
- 改进数据统计卡片的hover效果
- 优化移动端的响应式布局
- 修复文章卡片的对齐问题"

# 7. 推送
git push -u origin feature/首页样式优化

# 8. 创建PR（可选）
# 在GitHub网页创建Pull Request

# 9. 审查并合并
# 如果直接合并到main:
git checkout main
git pull origin main
git merge feature/首页样式优化

# 10. 推送到远程main
git push origin main

# 11. 删除特性分支
git branch -d feature/首页样式优化
git push origin --delete feature/首页样式优化

# 12. 在服务器拉取并部署
ssh root@39.105.154.244
cd /www/wwwroot/epgo
git pull origin main
# 清除缓存...
```

---

## 📚 扩展阅读

- [Git官方文档](https://git-scm.com/doc)
- [GitHub工作流](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git分支模型](https://nvie.com/posts/a-successful-git-branching-model/)

---

**提示**: 养成好的Git习惯，让代码管理变得轻松！ 🚀
