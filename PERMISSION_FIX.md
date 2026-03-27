# 🔧 权限问题修复指南 - 快速参考

**问题**: `error templates file is not found`
**原因**: 模板文件权限不正确
**状态**: ✅ 已修复

---

## 🎯 问题原因分析

### 权限混乱情况

```
修复前的权限混乱:
├─ 部分文件: 501:games (错误用户组)
├─ 部分文件: root:root (错误用户组)
├─ 部分文件: -rw-r--r-- (无执行权限)
└─ 结果: PHP无法读取和执行这些文件

这就导致:
❌ "templates file is not found"
❌ "Permission denied"
❌ 白屏错误
❌ 500错误
```

---

## ✅ 已执行的修复操作

### 第1步: 修复所有权限

```bash
# 已执行的命令:
chown -R www:www templates/epgo-education/
chmod -R 755 templates/epgo-education/

# 结果:
✅ 所有文件现在属于 www:www 用户组
✅ 所有文件权限设为 755 (rwxr-xr-x)
✅ PHP能正常读取和执行
```

### 第2步: 清除缓存

```bash
# 已执行的命令:
rm -rf cache/*

# 结果:
✅ 旧缓存已删除
✅ 新请求会重新生成缓存
```

### 第3步: 重启Web服务

```bash
# 已执行的命令:
systemctl restart nginx

# 结果:
✅ Nginx已重启
✅ 新配置已加载
```

---

## 📋 修复后的文件权限

```
正确的权限状态:
-rwxr-xr-x 1 www www   295 Mar 22 10:01 404.php
-rwxr-xr-x 1 www www  4195 Mar 27 11:42 foot.php
-rwxr-xr-x 1 www www  6344 Mar 27 11:42 head.php
-rwxr-xr-x 1 www www 13887 Mar 27 11:42 index.php
-rwxr-xr-x 1 www www 10700 Mar 27 11:42 shownews.php
... 其他文件 ...

特点:
✅ 用户组: www:www (正确)
✅ 权限: 755 (正确，允许执行)
✅ 所有PHP文件可读可执行
✅ Nginx能正常调用
```

---

## 🔍 验证修复效果

### 检查权限是否正确

```bash
ssh root@101.42.21.191 "ls -la /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/*.php | head -5"

# 应该看到:
# -rwxr-xr-x 1 www www (所有PHP文件)
```

### 测试网站

访问您的网站，应该能看到：
- ✅ 首页正常显示
- ✅ 文章页面正常显示
- ✅ 下一篇/上一篇导航显示（如果已部署）
- ✅ 没有"file is not found"错误

---

## 💡 权限问题预防

### 宝塔面板修复权限

如果以后权限又出问题，可通过宝塔面板快速修复：

```
1. 打开宝塔面板
   https://101.42.21.191:8888/

2. 文件管理 → 找到 templates/epgo-education 目录

3. 右键 → 修改权限
   用户: www
   组: www
   权限: 755

4. 递归应用到所有子文件
```

### 通过SSH快速修复

如果需要快速修复，记住这个命令：

```bash
chown -R www:www /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/
chmod -R 755 /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/
```

---

## 📝 常见权限错误及解决

### 错误1: "templates file is not found"

**原因**: 权限不正确
**解决**:
```bash
chown -R www:www templates/
chmod -R 755 templates/
```

### 错误2: "Permission denied"

**原因**: 用户组不是 www
**解决**:
```bash
chown -R www:www [目录]
```

### 错误3: 白屏错误

**原因**: 权限不足导致PHP无法执行
**解决**:
```bash
chmod -R 755 [目录]
systemctl restart nginx
```

### 错误4: 上传文件后变成root权限

**原因**: 使用root上传文件
**解决**:
```bash
# 使用这个命令修复所有权限
find /www/wwwroot/go.xiachaoqing.com -user root -exec chown www:www {} \;
chmod -R 755 /www/wwwroot/go.xiachaoqing.com/
```

---

## ✅ 修复验证清单

- [x] 修改文件所有者为 www:www
- [x] 修改权限为 755
- [x] 清除缓存目录
- [x] 重启 Nginx
- [x] 验证 PHP 文件可执行
- [x] 检查 shownews.php 权限正确

---

## 🎊 现在该做什么

### 立即测试

```
1. 打开网站: http://go.xiachaoqing.com (或 https://101.42.21.191)
2. 检查是否能正常访问
3. 如果还有错误，检查 Nginx 错误日志:
   tail -50 /www/server/nginx/logs/error.log
```

### 如果还有问题

```
1. 检查 PHP 错误日志:
   tail -50 /www/server/php/*/log/php-error.log

2. 检查 Nginx 访问日志:
   tail -50 /www/server/nginx/logs/access.log

3. 查看数据库连接:
   mysql -u xiachaoqing -p***REMOVED*** -e "SELECT 1;"
```

---

## 📞 快速命令参考

```bash
# 修复权限 (最常用)
chown -R www:www /www/wwwroot/go.xiachaoqing.com/templates/
chmod -R 755 /www/wwwroot/go.xiachaoqing.com/templates/

# 清除所有缓存
rm -rf /www/wwwroot/go.xiachaoqing.com/cache/*

# 重启 Web 服务
systemctl restart nginx

# 查看权限
ls -la /www/wwwroot/go.xiachaoqing.com/templates/epgo-education/

# 查看错误日志
tail -100 /www/server/nginx/logs/error.log
```

---

**问题已修复！网站应该正常了！** ✅

如果还有问题，检查上面的"常见权限错误"部分。
