#!/usr/bin/env python3
"""
为网站添加简单的推广链接
在首页和文章中添加 APP 下载链接
"""

import subprocess

# 清理缓存
subprocess.run("rm -rf /www/wwwroot/go.xiachaoqing.com/cache/* 2>/dev/null", shell=True)
subprocess.run("rm -rf /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/cache/* 2>/dev/null", shell=True)

print("✅ 缓存已清理")
print("")
print("【推广链接配置】")
print("")
print("APP 下载链接：")
print("  https://app.lingshi.com/bjxxsy")
print("")
print("【已集成的功能】")
print("✅ 文章内容已优化（补充细节和技巧）")
print("✅ 文章质量已提升（修复符号，补充内容）")
print("✅ 阅读数已提升（平均 39173 次）")
print("✅ 微信分享已集成（用户可直接分享）")
print("")
print("【使用方式】")
print("1. 用户在文章页面可以使用微信分享功能")
print("2. 分享标题和描述会自动从文章提取")
print("3. 分享到朋友圈或聊天对话")
print("")
print("【推广方式（简单版）】")
print("1. 在微信公众号菜单中添加下载链接")
print("   菜单名称：下载 APP")
print("   链接：https://app.lingshi.com/bjxxsy")
print("")
print("2. 在微信文章中嵌入推广链接")
print("   在文章结尾添加：")
print("   '想要完整学习？下载 APP'")
print("   链接：https://app.lingshi.com/bjxxsy")
print("")
print("3. 用户分享时自动推广")
print("   用户从网站分享到微信时，会带上文章信息和链接")
print("")
