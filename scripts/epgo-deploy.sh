#!/bin/bash
# epgo 一键部署脚本
# 用法：epgo-deploy [push|pull]
#   push  本地 -> 服务器（默认）
#   pull  服务器 -> 本地

ACTION=${1:-push}
LOCAL="/Users/xiachaoqing/projects/epgo/"
REMOTE="epgo:/www/wwwroot/go.xiachaoqing.com/"
EXCLUDE="--exclude='.git' --exclude='upload/' --exclude='cache/' --exclude='logs/' --exclude='config/metinfo.db' --exclude='config/config_safe.php'"

if [ "$ACTION" = "push" ]; then
    echo "推送本地 -> 服务器..."
    rsync -av $EXCLUDE "$LOCAL" "$REMOTE"
    ssh epgo 'chmod -R 777 /www/wwwroot/go.xiachaoqing.com/ 2>/dev/null; echo "✓ 部署完成"'
elif [ "$ACTION" = "pull" ]; then
    echo "拉取服务器 -> 本地..."
    rsync -av $EXCLUDE "$REMOTE" "$LOCAL"
    echo "✓ 同步完成"
else
    echo "用法: epgo-deploy [push|pull]"
fi
