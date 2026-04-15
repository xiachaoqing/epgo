# 🚨 安全应急：暴露的数据库密码修复指南

**问题：** GitGuardian检测到Basic Auth String已暴露
**被暴露的内容：** 数据库密码 `***REMOVED***`
**仓库：** xiachaoqing/epgo
**推送日期：** 2026-04-15
**严重性：** 🔴 高风险

---

## 立即执行的操作

### 第一步：更改所有暴露的凭证

你需要在服务器上立即执行：

```bash
# 1. 更改MySQL数据库用户密码
mysql -u xiachaoqing -p
# 输入旧密码 ***REMOVED***
mysql> ALTER USER 'xiachaoqing'@'localhost' IDENTIFIED BY 'NewSecure@Pass2026!';
mysql> FLUSH PRIVILEGES;
mysql> EXIT;

# 2. 更改SSH密钥（如果有暴露）
# 如果SSH密钥也被提交过，需要重新生成
```

### 第二步：从git历史中完全移除密码

**方法1：使用BFG Repo-Cleaner（推荐）**

```bash
# 1. 下载BFG
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

# 2. 克隆裸仓库
git clone --mirror https://github.com/xiachaoqing/epgo.git epgo.git

# 3. 移除所有密码字符串
java -jar bfg-1.14.0.jar --replace-text passwords.txt epgo.git
# 其中passwords.txt包含：
# ***REMOVED***

# 4. 清理和推送
cd epgo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --mirror

# 5. 删除备份
cd ..
rm -rf epgo.git
```

**方法2：使用git filter-branch**

```bash
cd /path/to/epgo

# 1. 备份当前分支（防万一）
git branch backup-before-cleanup

# 2. 使用filter-branch移除密码
git filter-branch -f --tree-filter '
  find . -name "*.py" -type f -exec sed -i "s/password=\"***REMOVED***\"/password=\"REDACTED\"/g" {} \;
  find . -name "*.py" -type f -exec sed -i "s/password=.***REMOVED***./password=REDACTED/g" {} \;
  find . -name "*.py" -type f -exec sed -i "s/***REMOVED***/REDACTED/g" {} \;
' -- --all

# 3. 删除原始备份
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 4. 强制推送（这会改变所有commit hash）
git push -f origin main
```

**方法3：完全销毁并重建仓库（最彻底但麻烦）**

```bash
# 如果数据库密码被广泛使用，最安全的做法是：
# 1. 在服务器上彻底更改所有密码
# 2. 销毁GitHub仓库
# 3. 创建新仓库
# 4. 重新推送干净的代码
```

---

## 建议的修复方案（按优先级）

### 🔴 必须立即执行
1. **改密码** - 服务器上更改MySQL密码
2. **查审计日志** - 检查谁访问了这个仓库，有没有人用这个密码
3. **扫描其他仓库** - 检查是否在其他GitHub仓库中也暴露过这个密码

### 🟠 今天内必须完成
4. **清理git历史** - 用BFG或git filter-branch完全移除密码
5. **强制推送** - git push -f origin main

### 🟡 近期完成
6. **更新所有配置** - 使用新密码更新所有配置文件
7. **添加.gitignore** - 防止未来再暴露密码
8. **使用环境变量** - 所有敏感信息都用环境变量，不要硬编码

---

## 创建.gitignore防止未来泄露

创建文件 `epgo/.gitignore`：

```
# 敏感信息文件
.env
.env.local
.env.*.local
config/secrets.py
config/credentials.json

# 数据库配置
db_config.py
secrets.ini

# SSH密钥
*.pem
*.ppk
*.key
id_rsa
id_rsa.pub

# API密钥和令牌
.api_keys
.tokens
api_keys.txt

# 其他
node_modules/
.DS_Store
__pycache__/
*.pyc
.vscode/settings.json
```

---

## 使用环境变量的正确做法

**旧做法（危险）：**
```python
# ❌ 不要这样做！
DB = dict(
    host="127.0.0.1",
    user="xiachaoqing",
    password="***REMOVED***"  # 暴露！
)
```

**新做法（安全）：**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # 从.env文件加载

DB = dict(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    user=os.getenv("DB_USER", "xiachaoqing"),
    password=os.getenv("DB_PASSWORD"),  # 从环境变量读取
    database=os.getenv("DB_NAME", "epgo_db")
)
```

**创建.env文件（不要提交到git）：**
```
DB_HOST=127.0.0.1
DB_USER=xiachaoqing
DB_PASSWORD=NewSecure@Pass2026!
DB_NAME=epgo_db
```

`.env` 已添加到 `.gitignore`，所以不会被提交。

---

## 检查清单

- [ ] 更改了数据库密码
- [ ] 扫描了git历史中所有暴露的密码
- [ ] 用BFG或git filter-branch清理了git历史
- [ ] 强制推送到远程仓库
- [ ] 创建了.gitignore文件
- [ ] 更新了所有配置文件使用环境变量
- [ ] 通知了访问这个仓库的团队成员重新clone
- [ ] 检查了是否在其他地方也暴露了这个密码

---

## 如何回答GitGuardian

1. **不是误报** - 这确实是真实的密码泄露
2. **已修复** - 已从git历史中移除，服务器密码已更改
3. **预防措施** - 已添加.gitignore和使用环境变量

---

## 进阶安全建议

### GitHub Repository Secrets（用于CI/CD）
```yaml
# .github/workflows/deploy.yml
env:
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}  # 从GitHub Secrets读取
```

### Vault或密钥管理系统（企业级）
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault

### 代码审查流程
- 在所有PR中运行secret scanning
- 使用工具如 `truffleHog` 或 `detect-secrets`

---

## 参考资源

- GitGuardian文档：https://docs.gitguardian.com
- GitHub Secret Scanning：https://docs.github.com/en/code-security/secret-scanning
- BFG Repo-Cleaner：https://rtyley.github.io/bfg-repo-cleaner/
- OWASP密钥管理：https://owasp.org/www-community/Sensitive_Data_Exposure

---

**优先级最高：立即在服务器上更改密码！其他工作可以逐步进行。**
