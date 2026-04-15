#!/bin/bash
# 安全修复脚本：移除git历史中暴露的密码

echo "🚨 开始移除暴露的数据库密码..."
echo ""

# 使用git filter-branch移除所有包含密码的提交
# 这会重写所有git历史

# 第一步：找到包含密码的所有提交
echo "【第一步】扫描包含密码的提交..."
git rev-list --all | while read commit; do
  if git show $commit | grep -q "password=\"Xia@07090218\""; then
    echo "  发现密码在提交: $commit"
  fi
done

echo ""
echo "【第二步】准备重写历史..."
echo "警告：这会改变所有commit hash，需要强制推送！"
echo ""

# 第三步：使用git filter-branch移除密码
# 这会创建一个备份分支refs/original
echo "【第三步】开始过滤..."

git filter-branch -f --tree-filter '
  find . -name "*.py" -type f | while read file; do
    if grep -q "password=" "$file" 2>/dev/null; then
      # 替换所有password="Xia@07090218"为password="REDACTED"
      sed -i "s/password=\"Xia@07090218\"/password=\"REDACTED\"/g" "$file"
      sed -i "s/password=.Xia@07090218./password=REDACTED/g" "$file"
      echo "  清理: $file"
    fi
  done
  true
' -- $(git rev-list --all --not --exclude=refs/original/refs/heads/main)

echo ""
echo "✓ git历史已清理"
echo ""

# 删除备份
echo "【第四步】删除备份分支..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✓ 备份已删除"
echo ""
echo "【第五步】需要强制推送到远程..."
echo "命令：git push -f origin main"
echo ""
echo "⚠️ 注意：强制推送会改变远程历史！"
echo "如果有其他人在这个分支工作，请通知他们重新clone。"
