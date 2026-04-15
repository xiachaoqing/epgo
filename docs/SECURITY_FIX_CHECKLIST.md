# 🚨 安全事件：GitHub密码泄露修复指南

**事件：** GitGuardian 检测到暴露的Basic Auth String
**被暴露内容：** MySQL数据库密码 `07090218`
**仓库：** xiachaoqing/epgo
**推送日期：** 2026-04-15 10:49:47 UTC
**风险等级：** 🔴 严重
**状态：** ⚠️ 正在修复

---

## 📋 问题分析

### 暴露的密码出现在：
```
scripts/emergency_restore.py:13    password="07090218"
scripts/multi_source_crawler.py:26 password="07090218"
scripts/quality_article_system.py:23 password="07090218"
... (多个Python文件)
```

### 潜在风险：
- ❌ 任何人都可以从公开仓库的git历史中获取这个密码
- ❌ 攻击者可以直接访问数据库
- ❌ 可能导致数据泄露、数据篡改或系统破坏

---

## 🔧 修复步骤（必须立即执行）

### 第一步：更改数据库密码（🟢 已准备）

在服务器上执行：
```bash
ssh root@101.42.21.191

# 登录MySQL
mysql -u xiachaoqing -p
# 输入旧密码: 07090218

# 执行以下SQL
ALTER USER 'xiachaoqing'@'localhost' IDENTIFIED BY 'NewSecurePass@2026#xyz';
FLUSH PRIVILEGES;
EXIT;
```

**新密码应该：**
- ✓ 至少16个字符
- ✓ 包含大小写字母、数字、特殊符号
- ✓ 不易被猜测
- ✓ 与旧密码完全不同

### 第二步：从git历史移除密码

在本地执行以下脚本：

```bash
cd /Users/xiachaoqing/projects/epgo

# 使脚本可执行
chmod +x scripts/security_cleanup.sh

# 执行清理脚本
bash scripts/security_cleanup.sh
```

这个脚本会：
1. 扫描git历史中的暴露密码
2. 创建备份分支（安全起见）
3. 使用git filter-branch移除所有密码
4. 进行垃圾回收和优化

### 第三步：强制推送到GitHub

执行脚本后会提示强制推送。执行以下命令：

```bash
# 推送清理后的main分支（会覆盖远程历史）
git push -f origin main

# 推送备份分支（以防万一）
git push -f origin backup-before-password-cleanup
```

⚠️ **警告：** 强制推送会改变历史，其他克隆这个仓库的人需要：
```bash
# 重新clone（推荐）
git clone https://github.com/xiachaoqing/epgo.git

# 或者（如果有本地改动）
git fetch origin
git reset --hard origin/main
```

### 第四步：更新所有配置文件

将所有硬编码的密码改为环境变量：

```python
# ❌ 旧做法（危险）
DB = dict(
    user="xiachaoqing",
    password="07090218"  # 不要这样！
)

# ✅ 新做法（安全）
import os
DB = dict(
    user="xiachaoqing",
    password=os.getenv("DB_PASSWORD")  # 从环境变量读取
)
```

### 第五步：创建.env文件（本地，不提交）

在服务器上创建：
```bash
cat > /www/wwwroot/go.xiachaoqing.com/.env << EOF
DB_HOST=127.0.0.1
DB_USER=xiachaoqing
DB_PASSWORD=NewSecurePass@2026#xyz
DB_NAME=epgo_db
EOF

chmod 600 /www/wwwroot/go.xiachaoqing.com/.env  # 只有所有者可读
```

---

## ✅ 已完成的安全改进

### 本地提交（已推送）
- ✅ 增强了`.gitignore`，防止敏感文件被提交
- ✅ 创建了`.env.example`模板（这个可以安全地提交）
- ✅ 编写了完整的安全修复指南
- ✅ 提供了自动化清理脚本

### 待执行
- ⏳ 执行`security_cleanup.sh`清理git历史
- ⏳ 强制推送到GitHub
- ⏳ 更新所有配置文件使用环境变量
- ⏳ 服务器上更新密码

---

## 📚 使用环境变量的完整示例

**scripts/quality_article_system.py（修改后）：**

```python
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

DB = dict(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),  # 安全！
    database=os.getenv("DB_NAME", "epgo_db"),
    charset="utf8mb4"
)

# 确保密码已设置
if not os.getenv("DB_PASSWORD"):
    raise ValueError("DB_PASSWORD environment variable not set!")
```

---

## 🛡️ 预防措施

### 1. 本地开发最佳实践
```bash
# 创建本地.env文件
cp .env.example .env
# 编辑.env，填入本地密码

# .env已在.gitignore中，不会被意外提交
git status  # 应该看不到.env文件
```

### 2. 代码审查流程
- 在所有PR中检查是否有硬编码的密钥
- 使用自动工具如 `detect-secrets` 或 `truffleHog`

### 3. Git hooks防止泄露
```bash
# 安装pre-commit hook
pip install pre-commit detect-secrets

# 配置.pre-commit-config.yaml
git hooks install
```

### 4. CI/CD中使用Secrets
```yaml
# GitHub Actions example
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: python deploy.py
```

---

## 📋 检查清单

### 立即执行（今天）
- [ ] 确认你看到了这个通知
- [ ] 告知团队其他成员这个安全问题
- [ ] 在服务器上更改数据库密码

### 本周执行
- [ ] 执行 `bash scripts/security_cleanup.sh`
- [ ] 强制推送到GitHub (`git push -f origin main`)
- [ ] 更新所有Python脚本使用环境变量
- [ ] 在服务器上创建.env文件
- [ ] 测试所有脚本是否正常工作

### 之后
- [ ] 建立密码管理流程
- [ ] 添加git pre-commit hooks
- [ ] 定期扫描git历史中是否有泄露的密钥
- [ ] 建立安全文化培训

---

## 🆘 如果出现问题

### 问题：无法运行security_cleanup.sh
```bash
# 确保文件可执行
chmod +x scripts/security_cleanup.sh

# 或者直接用bash运行
bash scripts/security_cleanup.sh
```

### 问题：强制推送失败
```bash
# 检查是否有未提交的改动
git status

# 如果有，先stash或提交
git stash
git push -f origin main
```

### 问题：其他开发者无法pull
```bash
# 他们需要重新clone或强制更新
git fetch origin
git reset --hard origin/main
```

---

## 📞 联系信息

遇到安全问题，请立即：
1. 通知团队lead
2. 参考 [GitHub Security Guide](https://docs.github.com/en/code-security)
3. 查看 [GitGuardian文档](https://docs.gitguardian.com)

---

**重要提醒：安全无小事。今天采取的行动将防止未来可能的严重数据泄露。**

---

*最后更新：2026-04-15*
*修复文档：SECURITY_EXPOSED_PASSWORD_FIX.md*
*清理脚本：scripts/security_cleanup.sh*
