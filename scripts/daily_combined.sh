#!/bin/bash
# 每天运行两个系统：模板系统 + 高质量系统
# 配置：0 2 * * * bash /www/wwwroot/go.xiachaoqing.com/scripts/daily_combined.sh

echo "=== 开始日常文章生成 ===" >> /www/wwwroot/go.xiachaoqing.com/logs/daily.log

# 1. 运行模板系统（补充）
python3 /www/wwwroot/go.xiachaoqing.com/scripts/daily_maintain_epgo.py >> /www/wwwroot/go.xiachaoqing.com/logs/daily.log 2>&1

# 2. 运行高质量系统（主体）
python3 /www/wwwroot/go.xiachaoqing.com/scripts/quality_article_system.py >> /www/wwwroot/go.xiachaoqing.com/logs/daily.log 2>&1

echo "=== 完成 ===" >> /www/wwwroot/go.xiachaoqing.com/logs/daily.log
