<?php
/**
 * 生成导航栏目结构
 * 从数据库查询一级&二级栏目，生成HTML导航代码
 */
error_reporting(E_ALL);
ini_set('display_errors', 1);

// 数据库配置
$db_host = '127.0.0.1';
$db_user = 'xiachaoqing';
$db_pass = '07090218';
$db_name = 'epgo_db';

try {
    $pdo = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_THROW);
} catch (Exception $e) {
    die("数据库连接失败: " . $e->getMessage());
}

// 查询一级栏目
$sql_level1 = "
    SELECT id,name,foldername,nav FROM ep_column
    WHERE lang='cn' AND isshow=1 AND bigclass=0 AND nav=1
    ORDER BY no_order
";
$stmt = $pdo->query($sql_level1);
$level1 = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo "=== 导航栏目结构 ===\n";
echo json_encode($level1, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";

$nav_html = "<ul class=\"nav navbar-nav navlist\">\n";
$nav_html .= "  <li class='nav-item'>\n";
$nav_html .= "    <a href=\"/\" title=\"网站首页\" class=\"nav-link\">网站首页</a>\n";
$nav_html .= "  </li>\n";

foreach ($level1 as $p1) {
    // 查询子栏目
    $sql_level2 = "
        SELECT id,name,foldername FROM ep_column
        WHERE lang='cn' AND isshow=1 AND bigclass={$p1['id']}
        ORDER BY no_order
    ";
    $stmt2 = $pdo->query($sql_level2);
    $level2 = $stmt2->fetchAll(PDO::FETCH_ASSOC);

    if (count($level2) > 0) {
        // 有子栏目，用dropdown
        $nav_html .= "  <li class=\"nav-item dropdown\">\n";
        $nav_html .= "    <a href=\"{$p1['foldername']}/\" title=\"{$p1['name']}\" class=\"nav-link dropdown-toggle\" data-toggle=\"dropdown\" role=\"button\" aria-haspopup=\"true\" aria-expanded=\"false\">{$p1['name']}</a>\n";
        $nav_html .= "    <ul class=\"dropdown-menu\">\n";
        foreach ($level2 as $p2) {
            $nav_html .= "      <li><a href=\"{$p2['foldername']}/\" title=\"{$p2['name']}\">{$p2['name']}</a></li>\n";
        }
        $nav_html .= "    </ul>\n";
        $nav_html .= "  </li>\n";
    } else {
        // 无子栏目
        $nav_html .= "  <li class=\"nav-item\">\n";
        $nav_html .= "    <a href=\"{$p1['foldername']}/\" title=\"{$p1['name']}\" class=\"nav-link\">{$p1['name']}</a>\n";
        $nav_html .= "  </li>\n";
    }
}

$nav_html .= "</ul>\n";

echo "\n=== 生成的导航HTML ===" . substr($nav_html, 0, 500) . "...\n";
echo "\n✓ 导航结构查询完成\n";
echo "建议手动将此HTML复制到 head.php 的 navlist 中，或修改 head.php 调用此脚本\n";
?>
