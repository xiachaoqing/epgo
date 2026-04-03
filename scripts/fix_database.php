<?php
/**
 * 数据库诊断和修复脚本
 * 处理栏目结构问题
 */

// 数据库配置
$db_host = 'localhost';
$db_user = 'xiachaoqing';
$db_pass = '***REMOVED***';
$db_name = 'epgo_db';
$db_prefix = 'ep_';

// 连接数据库
$mysqli = new mysqli($db_host, $db_user, $db_pass, $db_name);
if ($mysqli->connect_error) {
    die('数据库连接失败: ' . $mysqli->connect_error);
}
$mysqli->set_charset('utf8');

echo "=== 栏目结构诊断和修复 ===\n";
echo "数据库: " . $db_name . "\n\n";

// 1. 查询现有栏目结构
echo "1. 查询现有一级栏目...\n";
$sql = "SELECT id, name, classtype, nav, isshow, bigclass FROM {$db_prefix}column
        WHERE lang='cn' AND classtype=1 AND bigclass=0
        ORDER BY no_order, id";
$result = $mysqli->query($sql);

$categories = [];
if ($result && $result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $categories[] = $row;
        printf("  [%d] %s (nav=%d, isshow=%d)\n", $row['id'], $row['name'], $row['nav'], $row['isshow']);
    }
}

// 2. 针对KET和PET栏目，检查子栏目
echo "\n2. 检查子栏目结构...\n";
$sql = "SELECT id, name, classtype, nav, isshow, bigclass FROM {$db_prefix}column
        WHERE lang='cn' AND classtype=2 AND bigclass > 0
        ORDER BY bigclass, no_order, id";
$result = $mysqli->query($sql);

$subcategories = [];
if ($result && $result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $subcategories[] = $row;
        printf("  [%d] %s (parent=%d, classtype=%d, nav=%d, isshow=%d)\n",
            $row['id'], $row['name'], $row['bigclass'], $row['classtype'], $row['nav'], $row['isshow']);
    }
}

// 3. 修复问题
echo "\n3. 开始修复...\n";

// 修复3a: 确保所有子栏目 classtype=2, nav=0, isshow=1
echo "\n3a. 修复子栏目（classtype=2, nav=0, isshow=1）...\n";
$sql = "UPDATE {$db_prefix}column SET classtype=2, nav=0, isshow=1
        WHERE lang='cn' AND bigclass > 0";
$mysqli->query($sql);
echo "  受影响的行数: " . $mysqli->affected_rows . "\n";

// 修复3b: 确保一级栏目正确显示
echo "3b. 修复一级栏目（classtype=1, isshow=1）...\n";
$sql = "UPDATE {$db_prefix}column SET classtype=1, isshow=1
        WHERE lang='cn' AND bigclass=0 AND id NOT IN (1, 2)"; // 排除系统栏目
$mysqli->query($sql);
echo "  受影响的行数: " . $mysqli->affected_rows . "\n";

// 修复3c: 确保导航显示的只有一级栏目
echo "3c. 调整导航显示（只有一级栏目显示在导航）...\n";
$sql = "UPDATE {$db_prefix}column SET nav=1 WHERE lang='cn' AND classtype=1 AND bigclass=0 AND isshow=1 LIMIT 10";
$mysqli->query($sql);
echo "  一级栏目导航修复: " . $mysqli->affected_rows . "\n";

$sql = "UPDATE {$db_prefix}column SET nav=0 WHERE lang='cn' AND (classtype=2 OR classtype=3)";
$mysqli->query($sql);
echo "  二级/三级栏目导航移除: " . $mysqli->affected_rows . "\n";

// 4. 验证修复结果
echo "\n4. 验证修复结果...\n";
$sql = "SELECT id, name, classtype, nav, isshow, bigclass FROM {$db_prefix}column
        WHERE lang='cn' ORDER BY classtype, no_order, id LIMIT 20";
$result = $mysqli->query($sql);

echo "\n修复后的栏目结构（前20个）:\n";
if ($result && $result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $level = ($row['bigclass'] > 0) ? '  ├─' : '─';
        printf("%s [%d] %s (type=%d, nav=%d, show=%d)\n",
            $level, $row['id'], $row['name'], $row['classtype'], $row['nav'], $row['isshow']);
    }
}

// 5. 检查文章数据
echo "\n5. 检查栏目文章数量...\n";
$sql = "SELECT classid, COUNT(*) as cnt FROM {$db_prefix}news
        WHERE lang='cn' GROUP BY classid
        ORDER BY cnt DESC LIMIT 10";
$result = $mysqli->query($sql);

if ($result && $result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $sql_get = "SELECT name FROM {$db_prefix}column WHERE id=" . intval($row['classid']);
        $res_get = $mysqli->query($sql_get);
        if ($res_get && $res_get->num_rows > 0) {
            $col = $res_get->fetch_assoc();
            printf("  栏目[%d] %s: %d篇文章\n", $row['classid'], $col['name'], $row['cnt']);
        }
    }
} else {
    echo "  未找到文章数据\n";
}

// 6. 删除缓存指令
echo "\n6. 缓存清理指令（需要在服务器执行）:\n";
echo "  rm -rf /www/wwwroot/go.xiachaoqing.com/cache/templates/\n";
echo "  rm -f /www/wwwroot/go.xiachaoqing.com/cache/column_cn.php\n";
echo "  mkdir -p /www/wwwroot/go.xiachaoqing.com/cache/templates\n";
echo "  chown -R www:www /www/wwwroot/go.xiachaoqing.com/cache\n";

echo "\n=== 修复完成 ===\n";
$mysqli->close();
?>
