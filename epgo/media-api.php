<?php
declare(strict_types=1);

// Thin same-origin proxy for the private Cobalt instance.
// The browser never receives the Cobalt API key. This endpoint accepts only
// public URLs from the allowlist and requires an explicit rights confirmation.
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

// The production PHP runtime is 7.2, so avoid PHP 8-only return types.
function respond(int $status, array $body) {
    http_response_code($status);
    echo json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    respond(405, ['status' => 'error', 'message' => '只支持 POST 请求']);
}

$raw = file_get_contents('php://input');
$input = json_decode($raw ?: '', true);
if (!is_array($input)) respond(400, ['status' => 'error', 'message' => '请求格式不正确']);

$url = trim((string)($input['url'] ?? ''));
$platform = trim((string)($input['platform'] ?? ''));
if (strlen($url) < 12 || strlen($url) > 2048) {
    respond(400, ['status' => 'error', 'message' => '链接长度不正确']);
}
if (($input['consent'] ?? true) !== true) {
    respond(400, ['status' => 'error', 'message' => '请确认你拥有内容处理权或已获得授权']);
}

$parts = parse_url($url);
$scheme = strtolower((string)($parts['scheme'] ?? ''));
$host = strtolower((string)($parts['host'] ?? ''));
if (!in_array($scheme, ['http', 'https'], true) || $host === '' || isset($parts['user']) || isset($parts['pass'])) {
    respond(400, ['status' => 'error', 'message' => '只支持公开的 http/https 链接']);
}

$domains = [
    'douyin.com', 'iesdouyin.com', 'kuaishou.com', 'gifshow.com',
    'xiaohongshu.com', 'xhslink.com', 'bilibili.com', 'b23.tv',
    'tiktok.com', 'instagram.com', 'youtube.com', 'youtu.be',
    'weibo.com', 'weibo.cn', 'vimeo.com',
];
$allowed = false;
foreach ($domains as $domain) {
    // Keep this compatible with the PHP 7.2 runtime on the production host.
    $suffix = '.' . $domain;
    if ($host === $domain || (strlen($host) > strlen($suffix) && substr($host, -strlen($suffix)) === $suffix)) {
        $allowed = true;
        break;
    }
}
if (!$allowed) respond(400, ['status' => 'error', 'message' => '暂不支持该平台链接']);

$keyFile = '/www/wwwroot/go.xiachaoqing.com/epgo/.media-api-key';
$apiKey = is_readable($keyFile) ? trim((string)file_get_contents($keyFile)) : '';
$cobaltUrl = 'http://127.0.0.1:9000/';
if ($apiKey === '' || !function_exists('curl_init')) {
    respond(503, ['status' => 'error', 'message' => '媒体服务尚未配置完成']);
}

$payload = json_encode([
    'url' => $url,
    'downloadMode' => 'auto',
    'videoQuality' => '1080',
    'localProcessing' => 'disabled',
    'filenameStyle' => 'basic',
], JSON_UNESCAPED_SLASHES);
$ch = curl_init($cobaltUrl);
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $payload,
    CURLOPT_HTTPHEADER => [
        'Accept: application/json',
        'Content-Type: application/json',
        'Authorization: Api-Key ' . $apiKey,
    ],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CONNECTTIMEOUT => 8,
    CURLOPT_TIMEOUT => 30,
]);
$response = curl_exec($ch);
$curlError = curl_error($ch);
$httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($response === false || $curlError !== '') {
    respond(502, ['status' => 'error', 'message' => '媒体服务连接失败，请稍后再试']);
}
$data = json_decode((string)$response, true);
if (!is_array($data)) respond(502, ['status' => 'error', 'message' => '媒体服务返回格式错误']);
if ($httpCode >= 400 || ($data['status'] ?? '') === 'error') {
    $code = (string)($data['error']['code'] ?? '');
    $friendly = $code !== '' ? '该链接暂时无法处理：' . $code : '该链接暂时无法处理';
    respond($httpCode >= 400 ? $httpCode : 422, ['status' => 'error', 'message' => $friendly]);
}

// Do not proxy media bytes through PHP. Cobalt returns a short-lived redirect
// or tunnel URL, which the browser can open directly.
respond(200, [
    'status' => $data['status'] ?? 'error',
    'url' => $data['url'] ?? null,
    'filename' => $data['filename'] ?? null,
    'picker' => $data['picker'] ?? null,
]);
