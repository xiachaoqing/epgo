<?php
/**
 * One-off, CLI-only editorial rollout. Usage:
 *   php scripts/apply_article_rewrites.php docs/content-rewrites/20261006-manifest.json
 *   php scripts/apply_article_rewrites.php docs/content-rewrites/20261006-manifest.json --apply
 * The first form validates and previews. --apply writes a timestamped backup before committing.
 */
if (PHP_SAPI !== 'cli') {
    fwrite(STDERR, "CLI only\n");
    exit(1);
}
if ($argc < 2 || $argc > 3 || ($argc === 3 && $argv[2] !== '--apply')) {
    fwrite(STDERR, "Usage: php apply_article_rewrites.php MANIFEST [--apply]\n");
    exit(1);
}
$apply = $argc === 3;
$manifestPath = realpath($argv[1]);
if (!$manifestPath) {
    fwrite(STDERR, "Manifest not found\n");
    exit(1);
}
$manifest = json_decode(file_get_contents($manifestPath), true);
if (!is_array($manifest) || empty($manifest['items']) || !is_array($manifest['items'])) {
    fwrite(STDERR, "Invalid manifest\n");
    exit(1);
}
$root = dirname(__DIR__);
$config = file_get_contents($root . '/config/config_db.php');
$keys = array('con_db_host', 'con_db_id', 'con_db_pass', 'con_db_name');
$db = array();
foreach ($keys as $key) {
    if (!preg_match('/' . $key . '\s*=\s*"([^"]*)"/', $config, $match)) {
        fwrite(STDERR, "Missing DB config key: {$key}\n");
        exit(1);
    }
    $db[$key] = $match[1];
}
$pdo = new PDO(
    'mysql:host=' . $db['con_db_host'] . ';dbname=' . $db['con_db_name'] . ';charset=utf8mb4',
    $db['con_db_id'],
    $db['con_db_pass'],
    array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION)
);
unset($db, $config);
$pdo->beginTransaction();
try {
    $select = $pdo->prepare('SELECT id,title,description,content,publisher,issue,updatetime,recycle FROM ep_news WHERE id=? FOR UPDATE');
    $rewrite = $pdo->prepare('UPDATE ep_news SET content=?,description=?,publisher=?,updatetime=? WHERE id=?');
    $hide = $pdo->prepare('UPDATE ep_news SET recycle=1 WHERE id=?');
    $seen = array();
    $backup = array();
    $operations = array();
    foreach ($manifest['items'] as $item) {
        $id = filter_var($item['id'] ?? null, FILTER_VALIDATE_INT);
        if (!$id || isset($seen[$id]) || !in_array($item['action'] ?? '', array('rewrite', 'hide'), true)) {
            throw new RuntimeException('Bad or duplicate item');
        }
        $seen[$id] = true;
        $select->execute(array($id));
        $row = $select->fetch(PDO::FETCH_ASSOC);
        if (!$row || (int)$row['recycle'] !== 0) {
            throw new RuntimeException("Article {$id} missing or already hidden");
        }
        if (!hash_equals($item['expected_sha256'], hash('sha256', $row['content']))) {
            throw new RuntimeException("Article {$id} changed after audit; aborting all changes");
        }
        $backup[] = $row;
        if ($item['action'] === 'rewrite') {
            $contentPath = realpath(dirname($manifestPath) . '/' . $item['file']);
            if (!$contentPath || strpos($contentPath, dirname($manifestPath) . DIRECTORY_SEPARATOR) !== 0) {
                throw new RuntimeException("Article {$id} content file invalid");
            }
            $content = file_get_contents($contentPath);
            // Keep a meaningful minimum while allowing concise, well-structured guides.
            if (trim(strip_tags($content)) === '' || strlen($content) < 1000) {
                throw new RuntimeException("Article {$id} content too short");
            }
            $operations[] = array('action' => 'rewrite', 'id' => $id, 'content' => $content,
                'description' => $item['description']);
        } else {
            $operations[] = array('action' => 'hide', 'id' => $id);
        }
    }
    $counts = array('rewrite' => 0, 'hide' => 0);
    foreach ($operations as $op) $counts[$op['action']]++;
    echo 'Validated: ' . $counts['rewrite'] . ' rewrites, ' . $counts['hide'] . " reversible hides\n";
    if (!$apply) {
        $pdo->rollBack();
        exit(0);
    }
    $backupPath = '/tmp/epgo_editorial_backup_' . date('Ymd_His') . '.json';
    if (file_put_contents($backupPath, json_encode($backup, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)) === false) {
        throw new RuntimeException('Failed to write backup');
    }
    chmod($backupPath, 0600);
    $now = date('Y-m-d H:i:s');
    foreach ($operations as $op) {
        if ($op['action'] === 'rewrite') {
            $rewrite->execute(array($op['content'], $op['description'], '英语陪跑GO', $now, $op['id']));
        } else {
            $hide->execute(array($op['id']));
        }
    }
    $pdo->commit();
    echo "Applied. Backup: {$backupPath}\n";
} catch (Exception $e) {
    if ($pdo->inTransaction()) $pdo->rollBack();
    fwrite(STDERR, $e->getMessage() . "\n");
    exit(1);
}
