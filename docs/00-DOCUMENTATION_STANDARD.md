# 📋 项目文档组织规划与执行标准

> 规划时间：2026-04-09 | 版本：v1.0 | 目的：统一管理文档，防止混乱

---

## ❌ 当前问题

### 现状分析

```
【根目录】14个文档
├─ ANALYSIS_AND_OPTIMIZATION_PLAN.md
├─ APP_PROMOTION_DETAILED_PLAN.md
├─ ARTICLE_OPTIMIZATION_COMPLETE.md
├─ COMPLETE_REPAIR_SUMMARY.md
├─ FIX_COVERS_SUMMARY.md
├─ MAINTENANCE_GUIDE.md
├─ OPTIMIZATION_SUMMARY.md
├─ PROMOTION_EXECUTION_COMPLETE.md
├─ PROMOTION_PLAN.md
├─ README.md
├─ READY_TO_OPERATE.md
├─ SCRIPT_ANALYSIS.md
├─ SYSTEM_CHECK_REPORT.md
└─ WECHAT_INTEGRATION_GUIDE.md

【docs目录】13个文档
├─ DEV_GUIDE.md + DEV_GUIDE_v2.md（重复）
├─ TEMPLATE_GUIDE.md + TEMPLATE_MODIFICATION_GUIDE_epgo-education.md（重复）
├─ hanhong-*.md（4个，关联度不明）
├─ 修复总结-20260327.md + 修复总结-20260327-final.md（重复）
├─ 完成清单.md
└─ 开发文档.md

总计：27个文档
问题：
❌ 文档分散，不知道看哪个
❌ 版本重复（DEV_GUIDE × 2，修复总结 × 2）
❌ 命名不规范（混合中英文、下划线、连字符）
❌ 目录结构混乱（没有按功能分类）
❌ 难以维护和查找
❌ 每次修改难以快速定位最新版本
```

---

## ✅ 新的文档组织结构

### 推荐的目录结构

```
/Users/xiachaoqing/projects/epgo/
│
├─ docs/
│  │
│  ├─ 1-README.md                    【项目总览】
│  ├─ 2-DEVELOPMENT_GUIDE.md         【开发指南】合并 DEV_GUIDE.md + DEV_GUIDE_v2.md
│  ├─ 3-ARCHITECTURE.md              【系统架构】网站结构、数据模型、技术栈
│  │
│  ├─ features/                      【功能模块文档】
│  │  ├─ wechat.md                   微信公众号集成（菜单、回复规则、推广）
│  │  ├─ articles.md                 文章管理系统（创建、优化、发布）
│  │  ├─ templates.md                模板系统（epgo-education、metv75等）
│  │  ├─ covers.md                   封面图管理系统
│  │  └─ ads.md                      广告系统（Google AdSense、阿里妈妈等）
│  │
│  ├─ operations/                    【运维/部署文档】
│  │  ├─ deployment.md               部署流程
│  │  ├─ maintenance.md              日常维护
│  │  ├─ backup.md                   备份恢复
│  │  └─ troubleshooting.md          故障排查
│  │
│  ├─ projects/                      【项目记录】
│  │  ├─ 20260327-article-optimization.md    【项目1】文章优化（完成日期）
│  │  ├─ 20260327-wechat-promotion.md        【项目2】微信推广集成（完成日期）
│  │  └─ 20260401-new-project.md             【项目3】新项目（完成日期）
│  │
│  └─ archive/                       【归档文档】
│     └─ old-docs-list.md            指向旧文档的索引
│
├─ .git/                             【Git仓库】
└─ README.md                         【根目录README】简要说明
```

---

## 📊 文档聚合方案

### 核心文档（需要合并）

#### 1️⃣ 【开发指南】- 合并 DEV_GUIDE + DEV_GUIDE_v2
```
新文件：docs/2-DEVELOPMENT_GUIDE.md

包含内容：
- 项目概述
- 技术栈
- 开发环境设置
- 常用命令
- 项目结构
- 最佳实践
- FAQ

说明：
- 从DEV_GUIDE.md提取核心内容
- 从DEV_GUIDE_v2.md提取补充信息
- 整合为一份完整指南
- 旧文件移到archive目录
```

#### 2️⃣ 【微信公众号】- 集中管理
```
新文件：docs/features/wechat.md

包含内容：
- 公众号基本配置
- 菜单结构（当前4个一级 + 17个二级）
- 回复规则（44条规则的完整列表）
- APP推广配置
- 文章发布流程
- 数据统计

来源：
- WECHAT_INTEGRATION_GUIDE.md
- SYSTEM_CHECK_REPORT.md
- openclaw_file 项目的微信文档
- 本次操作的改动记录
```

#### 3️⃣ 【文章系统】- 集中管理
```
新文件：docs/features/articles.md

包含内容：
- 文章创建流程
- 文章优化标准（符号、格式、内容长度）
- 文章发布流程
- 优化历史记录

来源：
- ARTICLE_OPTIMIZATION_COMPLETE.md
- ANALYSIS_AND_OPTIMIZATION_PLAN.md
- SYSTEM_CHECK_REPORT.md
```

#### 4️⃣ 【项目记录】- 时间戳命名
```
新目录：docs/projects/

每个项目一个文件：
- 20260327-article-optimization.md
  ├─ 项目目标
  ├─ 执行步骤
  ├─ 数据统计
  ├─ 问题解决
  ├─ 最终结果
  └─ Git提交记录

- 20260327-wechat-promotion.md
  ├─ 项目目标
  ├─ 数据库改动
  ├─ 服务重启
  ├─ 验证结果
  └─ 用户体验改进
```

---

## 🔄 工作流程标准化

### 新的操作流程

#### Step 1️⃣：计划阶段
```bash
📋 创建项目任务
- 定义目标
- 分解步骤
- 估算时间
- 创建对应的项目记录文档：docs/projects/YYYYMMDD-project-name.md
```

#### Step 2️⃣：执行阶段
```bash
🔄 分步执行 + 分步验证 + 分步提交

每完成一个小步骤（约15-30分钟的工作）：

a) 执行操作
   - 修改代码/数据库/配置

b) 验证改动
   - 直接查询数据库/服务器验证
   - 运行测试确认
   - 确保没有bug

c) 更新项目文档
   - 在 docs/projects/YYYYMMDD-*.md 中记录
   - 记录具体改动内容
   - 记录验证结果

d) 提交到Git
   - git add 变更文件
   - git add 项目文档
   - git commit -m "描述此步骤改动"
   - git push origin main

示例：
执行步骤1：添加APP菜单
├─ a) INSERT INTO we_menus ...
├─ b) SELECT * FROM we_menus WHERE id=18
├─ c) 在docs/projects/20260409-wechat-promotion.md更新记录
└─ d) git commit "step1: 添加APP菜单（ID=18）"

执行步骤2：添加APP回复规则
├─ a) INSERT INTO we_reply_rules ...
├─ b) SELECT * FROM we_reply_rules WHERE id=44
├─ c) 在docs/projects/20260409-wechat-promotion.md更新记录
└─ d) git commit "step2: 添加APP回复规则（ID=44）"

执行步骤3：重启后端
├─ a) systemctl restart wechat-platform
├─ b) systemctl status wechat-platform
├─ c) 在docs/projects/20260409-wechat-promotion.md更新记录
└─ d) git commit "step3: 重启后端并验证"
```

#### Step 3️⃣：总结阶段
```bash
📚 完成后更新相关核心文档

项目完成后：
- 归档项目记录：docs/projects/YYYYMMDD-*.md（已完成）
- 更新功能文档：docs/features/*.md（添加改动说明）
- 更新开发指南：docs/2-DEVELOPMENT_GUIDE.md（如有新的最佳实践）
- 更新README：docs/1-README.md（如果涉及重大改动）

示例：
项目"20260409-wechat-promotion"完成后
- 更新 docs/features/wechat.md
  添加段落：【最新改动 - 2026-04-09】
  记录：新增APP菜单、新增APP回复规则等
  附上：git提交哈希 / 操作步骤 / 验证结果
```

---

## 🔒 防止回滚的措施

### 1️⃣ 代码版本控制
```bash
✅ 分步提交：每个小步骤提交一次
   - 不要一次性修改多个功能后再提交
   - 每次提交对应一个具体改动
   - 便于快速定位和回滚

✅ 清晰的提交信息：
   格式：feat/fix/docs: 具体改动描述

   示例：
   "feat: 添加APP推广菜单（ID=18）
    - INSERT we_menus 新菜单
    - UPDATE 调整关于我们排序
    - 验证：SELECT 确认成功"
```

### 2️⃣ 验证前提交
```bash
✅ 操作 → 验证 → 提交（不是先提交再验证）

❌ 错误做法：
   改动 → 提交 → 验证发现问题 → 需要回滚

✅ 正确做法：
   改动 → 验证成功 → 提交 → 继续下一步
```

### 3️⃣ 文档记录
```bash
✅ 实时更新项目文档：
   - 每个步骤完成立即记录
   - 记录具体的SQL、命令、结果
   - 便于查证和回滚追踪

✅ 文档内容包含：
   - 【操作】做了什么
   - 【验证】用什么命令验证的
   - 【结果】验证结果是什么
   - 【问题】是否有问题
   - 【Git】提交哈希
```

### 4️⃣ Git标签
```bash
✅ 为重要改动打标签：

# 项目完成时
git tag -a v20260409-wechat-promo \
  -m "完成微信APP推广集成
  - 添加菜单 + 回复规则
  - 重启后端验证
  - 项目文档：docs/projects/20260409-wechat-promotion.md"
git push origin --tags
```

---

## 📋 文档维护清单

### 每次操作后的检查清单

```
操作完成后，每步完成时：
☐ 执行了操作（代码/SQL/命令）
☐ 验证了改动（查询数据库/查看服务状态）
☐ 更新了项目文档（docs/projects/YYYYMMDD-*.md）
☐ 提交到了Git（git add + git commit + git push）

项目完成后，交付前：
☐ 项目文档完整（docs/projects/YYYYMMDD-*.md）
☐ 功能文档更新（docs/features/*.md）
☐ 核心文档更新（docs/2-DEVELOPMENT_GUIDE.md）
☐ Git标签已打（git tag）
☐ 所有改动已推送（git push --tags）
☐ 清理旧文档（整理docs目录）
```

---

## 🚀 执行计划

### Phase 1️⃣：清理整理（今天立即做）
```bash
时间：30分钟

Step 1: 清理旧文档
  - 在根目录创建：PROJECTS_ARCHIVE.md
  - 列出所有27个旧文档
  - 标记哪些要保留、哪些要归档
  - 移动旧文档到 docs/archive/

Step 2: 创建新的目录结构
  mkdir -p docs/features
  mkdir -p docs/operations
  mkdir -p docs/projects
  mkdir -p docs/archive

Step 3: 创建项目文档
  创建 docs/projects/20260327-article-optimization.md
  创建 docs/projects/20260409-wechat-promotion.md
  记录这两个已完成项目的详细信息
```

### Phase 2️⃣：文档聚合（明天）
```bash
时间：1小时

Step 1: 合并开发指南
  创建 docs/2-DEVELOPMENT_GUIDE.md
  整合 DEV_GUIDE.md + DEV_GUIDE_v2.md + 最佳实践

Step 2: 创建功能文档
  创建 docs/features/wechat.md
  创建 docs/features/articles.md
  创建 docs/features/templates.md
  创建 docs/features/covers.md

Step 3: 创建操作文档
  创建 docs/operations/deployment.md
  创建 docs/operations/maintenance.md
  创建 docs/operations/troubleshooting.md
```

### Phase 3️⃣：建立规范（后续）
```bash
- 所有新操作都按照"工作流程标准化"进行
- 每个项目对应一个docs/projects/YYYYMMDD-*.md
- 每次操作分步执行、验证、提交、记录
```

---

## 🎯 最终目标

### 操作规范
```
✅ 所有操作都是可追溯的
✅ 每个改动都有对应的文档记录
✅ 出问题可以快速回滚（通过git）
✅ 新人能快速了解项目（通过统一的文档）
✅ 文档容易维护和查找
```

### 文档结构
```
docs/
├─ 1-README.md              # 项目总览
├─ 2-DEVELOPMENT_GUIDE.md   # 开发指南
├─ 3-ARCHITECTURE.md        # 系统架构
├─ features/                # 功能模块（每个功能一个文件）
├─ operations/              # 运维部署（部署、维护、故障排查）
├─ projects/                # 项目记录（每个项目一个文件，YYYYMMDD命名）
└─ archive/                 # 归档旧文档
```

---

## ❓ 确认事项

您同意吗？我的理解是：

1️⃣ **分步提交**：每个小改动立即提交，不要等全部完成再提交
   - 优点：容易定位问题、快速回滚、实时记录

2️⃣ **操作→验证→提交→记录**：每步都要验证才能提交
   - 验证方法：直接查数据库、查服务状态等
   - 不能靠"感觉"，必须有数据证明

3️⃣ **单文件记录**：每个项目一个docs/projects/YYYYMMDD-*.md
   - 不要分散成多个文件
   - 便于查找和回滚追踪

4️⃣ **文档聚合**：功能文档集中在docs/features/下
   - 微信功能 → docs/features/wechat.md
   - 文章系统 → docs/features/articles.md
   - 不要混乱分散

5️⃣ **清理整理**：立即清理27个混乱的文档
   - 新建目录结构
   - 旧文档到archive
   - 创建对应新文档

这样可以吗？

