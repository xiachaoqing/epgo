#!/bin/bash
#
# 安全修复脚本：完全移除暴露的数据库密码
# 使用：bash security_cleanup.sh
#
# 警告：这个脚本会：
# 1. 重写git历史（所有commit hash会改变）
# 2. 需要强制推送（会覆盖远程历史）
# 3. 其他克隆这个仓库的人需要重新fetch
#

set -e

echo ""
echo "=========================================="
echo "🚨 Git安全修复：移除暴露的密码"
echo "=========================================="
echo ""

# 检查是否在git仓库中
if [ ! -d ".git" ]; then
  echo "❌ 错误：不在git仓库目录中"
  exit 1
fi

# 检查是否有未提交的更改
if [ -n "$(git status --short)" ]; then
  echo "❌ 错误：有未提交的更改，请先提交或stash"
  exit 1
fi

echo "【第一步】扫描包含密码的提交..."
echo ""

# 扫描git历史
PASSWORD_COUNT=$(git rev-list --all | wc -l)
COMMITS_WITH_PASSWORD=$(git log -p --all | grep -c "password=\"***REMOVED***\"" || echo "0")

if [ "$COMMITS_WITH_PASSWORD" -gt 0 ]; then
  echo "  ⚠️  检测到 $COMMITS_WITH_PASSWORD 处暴露密码"
else
  echo "  ℹ️ 未检测到明显的密码暴露（但GitGuardian可能检测到其他格式）"
fi

echo ""
echo "【第二步】创建备份分支..."
git branch -f backup-before-password-cleanup
echo "  ✓ 已创建: backup-before-password-cleanup"

echo ""
echo "【第三步】开始过滤（这需要一些时间）..."
echo "  移除目标: password=\"***REMOVED***\" 和相关变体"
echo ""

# 使用git filter-branch
git filter-branch -f --tree-filter '
  # 对所有文件进行替换
  for file in $(find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.yml" -o -name "*.yaml" \) 2>/dev/null); do
    if [ -f "$file" ] && grep -q "***REMOVED***" "$file" 2>/dev/null; then
      # 替换所有可能的密码格式
      sed -i.bak "s/password=\"***REMOVED***\"/password=\"REDACTED_FOR_SECURITY\"/g" "$file" 2>/dev/null || true
      sed -i.bak "s/password=.***REMOVED***./password=REDACTED_FOR_SECURITY/g" "$file" 2>/dev/null || true
      sed -i.bak "s/password=***REMOVED***/password=REDACTED_FOR_SECURITY/g" "$file" 2>/dev/null || true
      sed -i.bak "s/\"***REMOVED***\"/\"REDACTED_FOR_SECURITY\"/g" "$file" 2>/dev/null || true
      sed -i.bak "s/***REMOVED***/REDACTED_FOR_SECURITY/g" "$file" 2>/dev/null || true

      # 删除备份文件
      rm -f "$file.bak"
      echo "  清理: $file"
    fi
  done
  true
' HEAD

if [ $? -eq 0 ]; then
  echo ""
  echo "  ✓ 过滤完成"
else
  echo ""
  echo "  ❌ 过滤失败，请检查错误信息"
  exit 1
fi

echo ""
echo "【第四步】删除git备份..."

# 删除filter-branch创建的备份
rm -rf .git/refs/original/

# 过期所有reflog条目
git reflog expire --expire=now --all
echo "  ✓ 已过期reflog"

# 垃圾回收
git gc --prune=now --aggressive
echo "  ✓ 已执行垃圾回收"

echo ""
echo "=========================================="
echo "✅ 本地清理完成！"
echo "=========================================="
echo ""
echo "下一步（需要你手动执行）："
echo ""
echo "1️⃣  验证本地分支:"
echo "   git log --oneline -5"
echo "   # 确保没有显示密码"
echo ""
echo "2️⃣  强制推送到远程（警告：会覆盖历史）:"
echo "   git push -f origin main"
echo ""
echo "3️⃣  强制推送备份分支（以防万一）:"
echo "   git push -f origin backup-before-password-cleanup"
echo ""
echo "4️⃣  其他开发者需要重新clone:"
echo "   git clone https://github.com/xiachaoqing/epgo.git"
echo ""
echo "=========================================="
echo ""

# 提示用户
read -p "是否现在执行强制推送？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo ""
  echo "执行强制推送..."
  git push -f origin main && echo "✓ 主分支推送成功" || echo "❌ 推送失败"
  git push -f origin backup-before-password-cleanup && echo "✓ 备份分支推送成功" || echo "❌ 推送失败"
else
  echo ""
  echo "⏭️  跳过推送，请在准备好时手动执行："
  echo "   git push -f origin main"
fi

echo ""
