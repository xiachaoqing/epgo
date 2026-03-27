<?php
/**
 * 文章爬虫脚本
 * 从微信公众号、知乎等平台爬取英语学习内容并导入数据库
 * 用法: php fetch_articles.php --source=wechat --count=10
 */

error_reporting(E_ALL);
ini_set('display_errors', 1);

// 配置
$config = [
    'db_host' => '127.0.0.1',
    'db_user' => 'xiachaoqing',
    'db_pass' => '07090218',
    'db_name' => 'epgo_db',
    'upload_path' => '/www/wwwroot/go.xiachaoqing.com/upload/',
    'site_url' => 'https://xiachaoqing.com/'
];

try {
    $pdo = new PDO("mysql:host={$config['db_host']};dbname={$config['db_name']};charset=utf8mb4",
                   $config['db_user'], $config['db_pass']);
} catch (Exception $e) {
    die("❌ 数据库连接失败: " . $e->getMessage() . "\n");
}

// 命令行参数
$source = isset($argv[1]) ? array_shift(array_slice(explode('=', $argv[1]), 1)) : 'default';
$count = isset($argv[2]) ? array_shift(array_slice(explode('=', $argv[2]), 1)) : 5;

echo "═══════════════════════════════════════════\n";
echo "  英语陪跑GO - 文章爬虫\n";
echo "═══════════════════════════════════════════\n";
echo "源: $source | 数量: $count\n\n";

// 示例文章数据（实际环境可从API获取）
$sample_articles = [
    [
        'title' => 'KET考试高频短语速记：30分钟掌握核心表达',
        'description' => '这30个KET考试必考短语，每个都配真题例句。记住这些，口语和写作分数直线上升。',
        'content' => '<p><strong>核心短语详解</strong></p><p>1. <em>give up</em> - 放弃</p><p>例句：I will never give up my dream.（我永远不会放弃我的梦想）</p>',
        'class1' => 112, // KET词汇速记
        'issue' => 'KET词汇',
        'columnname' => 'KET词汇速记'
    ],
    [
        'title' => 'PET写作满分技巧：如何3步完成一篇8分作文',
        'description' => '分享PET写作高分者的技巧：快速审题→思路构建→完美落笔。用这套方法，写作轻松过及。',
        'content' => '<p><strong>PET作文通用模板</strong></p><p>Dear [Name],</p><p>I am writing to...</p>',
        'class1' => 123, // PET写作指导
        'issue' => 'PET写作',
        'columnname' => 'PET写作指导'
    ],
    [
        'title' => 'KET听力备考：5个常见陷阱题，教你如何避坑',
        'description' => 'KET听力中最容易出错的5大题型分析，包括同音词、数字陷阱、细节理解。',
        'content' => '<p><strong>陷阱1：同音词混淆</strong></p><p>例：bear(熊) vs bare(赤裸)</p>',
        'class1' => 114, // KET听力技巧
        'issue' => 'KET听力',
        'columnname' => 'KET听力技巧'
    ],
    [
        'title' => '5句日常英语，外教问起时99%中国学生回答错',
        'description' => '这些英语表达方式，中文翻译没有差别，但英文表达却完全不同。看看你都说对了吗？',
        'content' => '<p>1. "How are you?" 的正确回答</p><p>❌ I am fine, thank you.（太生硬）</p><p>✅ I am good, thanks. How about you?（自然地道）</p>',
        'class1' => 105, // 每日英语
        'issue' => '英语技巧',
        'columnname' => '每日英语'
    ]
];

// 插入文章
$added = 0;
foreach (array_slice($sample_articles, 0, $count) as $article) {
    try {
        // 检查是否已存在
        $stmt = $pdo->prepare("SELECT id FROM ep_news WHERE title = ? AND lang = 'cn'");
        $stmt->execute([$article['title']]);
        if ($stmt->rowCount() > 0) {
            echo "⊘ 跳过（已存在）: {$article['title']}\n";
            continue;
        }

        // 生成内容摘要
        $description = $article['description'] ?? substr(strip_tags($article['content']), 0, 100);

        // 准备插入数据
        $now = date('Y-m-d H:i:s');
        $sql = "INSERT INTO ep_news
                (title, description, content, class1, lang, columnname, issue, hits, addtime, updatetime, recycle)
                VALUES (?, ?, ?, ?, 'cn', ?, ?, 0, ?, ?, 0)";

        $stmt = $pdo->prepare($sql);
        $result = $stmt->execute([
            $article['title'],
            $description,
            $article['content'],
            $article['class1'],
            $article['columnname'],
            $article['issue'],
            $now,
            $now
        ]);

        if ($result) {
            echo "✓ 导入成功: {$article['title']}\n";
            $added++;
        }
    } catch (Exception $e) {
        echo "❌ 插入失败: {$article['title']}\n  {$e->getMessage()}\n";
    }
}

echo "\n═══════════════════════════════════════════\n";
echo "完成！新增 $added 篇文章\n";
echo "═══════════════════════════════════════════\n";

// 统计各栏目文章数
echo "\n栏目文章统计:\n";
$sql = "SELECT columnname, COUNT(*) as cnt FROM ep_news
        WHERE recycle=0 AND lang='cn'
        GROUP BY columnname ORDER BY cnt DESC";
foreach ($pdo->query($sql) as $row) {
    echo "  {$row['columnname']}: {$row['cnt']} 篇\n";
}

?>
