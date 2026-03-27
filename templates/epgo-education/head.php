<?php defined('IN_MET') or exit('No permission'); ?><met_meta page="$met_page" /><!DOCTYPE html>
<html lang="{$g.lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- 自定义CSS（路径通过 $url.site 拼接，不要用 $metui_url / $template_url，那些变量不存在于运行时） -->
    <link rel="stylesheet" href="{$url.site}templates/epgo-education/css/epgo-education.css">

    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2043497135383313"
         crossorigin="anonymous"></script>
</head>
<body>
<!-- 顶部导航栏 -->
<nav class="met-head navbar navbar-expand-md navbar-light">
    <div class="container">
        <!-- Logo -->
        <a class="navbar-brand" href="{$c.index_url}">
            <if value="$lang.logo">
                <img src="{$lang.logo}" alt="{$lang.company_name}" style="max-height: 40px;">
            <else/>
                {$lang.company_name}
            </if>
        </a>

        <!-- 导航菜单切换按钮 -->
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <!-- 导航菜单 -->
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <!-- 首页 -->
                <li class="nav-item">
                    <a href="{$c.index_url}" class="nav-link <if value="$data['classnow'] eq 10001">active</if>">
                        {$word.home}
                    </a>
                </li>

                <!-- 动态栏目菜单 -->
                <tag action='category' type='head'>
                    <if value="$m['sub']">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle <if value="$m['class']">active</if>"
                               href="{$m.url}"
                               role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                {$m._name}
                            </a>
                            <div class="dropdown-menu">
                                <tag action='category' cid="$m['id']" type='son'>
                                    <a class="dropdown-item" href="{$m.url}" title="{$m.name}">
                                        {$m._name}
                                    </a>
                                </tag>
                            </div>
                        </li>
                    <else/>
                        <li class="nav-item">
                            <a class="nav-link <if value="$m['class']">active</if>" href="{$m.url}">
                                {$m._name}
                            </a>
                        </li>
                    </if>
                </tag>

                <!-- 公众号 -->
                <li class="nav-item">
                    <a href="javascript:void(0)" class="nav-link" onclick="epgoEducation.showQRCode()">
                        <i class="icon wb-share"></i> {$word.wechat}
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<!-- 公众号二维码弹窗 -->
<div id="qrcode-modal" class="qrcode-modal" style="display: none;">
    <div class="qrcode-modal-content">
        <span class="qrcode-modal-close" onclick="epgoEducation.closeQRCode()">&times;</span>
        <div class="qrcode-modal-body">
            <h3>关注公众号</h3>
            <p>英语陪跑GO</p>
            <div class="qrcode-box">
                <if value="$lang.wechat_qrcode">
                    <img src="{$lang.wechat_qrcode}" alt="微信公众号二维码" style="width: 240px; height: 240px;">
                <else/>
                    <div style="width: 240px; height: 240px; background: #f0f0f0; display: flex; align-items: center; justify-content: center;">
                        <p style="color: #999; text-align: center;">二维码配置中<br>(请在后台上传)</p>
                    </div>
                </if>
            </div>
            <p style="margin-top: 20px; color: #666; font-size: 14px;">长按识别二维码关注</p>
        </div>
    </div>
</div>

<style>
.qrcode-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
}

.qrcode-modal-content {
    background: white;
    padding: 40px;
    border-radius: 12px;
    text-align: center;
    position: relative;
    max-width: 400px;
    animation: slideUp 0.3s ease;
}

.qrcode-modal-close {
    position: absolute;
    top: 15px;
    right: 20px;
    font-size: 28px;
    cursor: pointer;
    color: #999;
}

.qrcode-modal-close:hover {
    color: #333;
}

@keyframes slideUp {
    from {
        transform: translateY(30px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

@media (max-width: 768px) {
    .qrcode-modal-content {
        max-width: 90%;
        padding: 30px 20px;
    }

    .qrcode-modal-content h3 {
        margin-bottom: 10px;
    }
}
</style>
