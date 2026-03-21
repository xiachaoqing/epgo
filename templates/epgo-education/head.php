<?php defined('IN_MET') or exit('No permission'); ?><!DOCTYPE html>
<html lang="{$g.lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<met_meta page="$met_page" />
<link rel="stylesheet" href="{$metui_url2}vendor/bootstrap/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="{$metui_url3}fonts/iconfont/iconfont.css">
<link rel="stylesheet" href="{$template_url}css/epgo-education.css?v=2026032201">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2043497135383313" crossorigin="anonymous"></script>
<if value="$_M['html']['css']">
<list data="$_M['html']['css']" name="$v">
<link rel="stylesheet" href="{$v}">
</list>
</if>
{$g.head}
</head>
<body>

<!-- 顶部导航 -->
<nav class="met-head navbar navbar-expand-md" id="mainNav">
    <div class="container">
        <a class="navbar-brand" href="{$c.index_url}" title="{$c.met_webname}">
            <if value="$c['met_logo']">
                <img src="{$c.met_logo}" alt="{$c.met_webname}" height="40">
            <else/>
                <span class="brand-text">英语陪跑GO</span>
            </if>
        </a>

        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navMenu">
            <span class="hamburger-bar"></span>
            <span class="hamburger-bar"></span>
            <span class="hamburger-bar"></span>
        </button>

        <div class="collapse navbar-collapse" id="navMenu">
            <ul class="navbar-nav ml-auto align-items-center">
                <li class="nav-item">
                    <a href="{$c.index_url}" class="nav-link <if value="$data['classnow'] eq 10001">active</if>">{$word.home}</a>
                </li>
                <tag action='category' type='head' class='active'>
                <if value="$m['sub']">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle {$m.class}" href="{$m.url}" data-toggle="dropdown">{$m._name}</a>
                    <div class="dropdown-menu">
                        <tag action='category' cid="$m['id']" type='son' class='active'>
                        <a class="dropdown-item {$m.class}" href="{$m.url}">{$m._name}</a>
                        </tag>
                    </div>
                </li>
                <else/>
                <li class="nav-item">
                    <a class="nav-link {$m.class}" href="{$m.url}">{$m._name}</a>
                </li>
                </if>
                </tag>
                <li class="nav-item">
                    <a href="javascript:void(0)" class="nav-link nav-wechat" onclick="epgoEducation.showQRCode()">
                        <i class="icon wb-share"></i> 公众号
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<!-- 内页Banner（首页不显示）-->
<if value="$data['classnow'] neq 10001">
<tag action='category' type='current' cid="$data['classnow']">
<div class="inner-banner">
    <div class="container">
        <h1 class="inner-banner-title">{$m.name}</h1>
        <nav class="breadcrumb-nav" aria-label="breadcrumb">
            <a href="{$c.index_url}">{$word.home}</a>
            <span class="sep">›</span>
            <span>{$m.name}</span>
        </nav>
    </div>
</div>
</tag>
</if>

<!-- 二维码弹窗 -->
<div id="qrcode-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.55); z-index:2000; align-items:center; justify-content:center; backdrop-filter:blur(2px);">
    <div class="qrcode-modal-content">
        <span onclick="epgoEducation.closeQRCode()" class="qrcode-close">&times;</span>
        <h3 style="margin-bottom:4px;">英语陪跑GO</h3>
        <p style="color:#999; font-size:14px; margin-bottom:16px;">扫码关注公众号</p>
        <div style="background:#f7f8fa; padding:10px; border-radius:10px; display:inline-block;">
            <if value="$lang['wechat_qrcode']">
                <img src="{$lang.wechat_qrcode}" alt="英语陪跑GO公众号" style="width:200px; height:200px; display:block;">
            <else/>
                <div style="width:200px; height:200px; display:flex; align-items:center; justify-content:center; color:#ccc; font-size:13px;">二维码待配置</div>
            </if>
        </div>
        <p style="margin-top:12px; font-size:13px; color:#999;">长按识别二维码关注</p>
    </div>
</div>

<style>
/* 弹窗样式 */
#qrcode-modal { display: none; }
#qrcode-modal.show { display: flex !important; }
.qrcode-modal-content {
    background: #fff;
    padding: 36px 32px;
    border-radius: 16px;
    text-align: center;
    position: relative;
    width: 320px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    animation: slideUp .3s ease;
}
.qrcode-close {
    position: absolute; top: 14px; right: 18px;
    font-size: 24px; cursor: pointer; color: #bbb; line-height: 1;
}
.qrcode-close:hover { color: #333; }
/* 导航hamburger */
.hamburger-bar {
    display: block; width: 22px; height: 2px;
    background: #333; margin: 5px 0; transition: .3s;
}
/* 内页banner */
.inner-banner {
    background: linear-gradient(135deg, #1565C0 0%, #1E88E5 100%);
    padding: 48px 0 36px;
    color: #fff;
}
.inner-banner-title { font-size: 28px; font-weight: 700; margin-bottom: 10px; color: #fff; }
.breadcrumb-nav { font-size: 14px; color: rgba(255,255,255,0.8); }
.breadcrumb-nav a { color: rgba(255,255,255,0.8); text-decoration: none; }
.breadcrumb-nav a:hover { color: #fff; }
.breadcrumb-nav .sep { margin: 0 8px; }
.brand-text { font-size: 20px; font-weight: 700; color: var(--color-primary); }
/* dropdown */
.met-head .dropdown-menu { border:1px solid #eee; box-shadow: 0 8px 24px rgba(0,0,0,0.1); border-radius:10px; padding:6px; }
.met-head .dropdown-item { border-radius:6px; padding:8px 14px; font-size:14px; color:#333; }
.met-head .dropdown-item:hover { background: var(--color-primary-light); color: var(--color-primary); }
</style>
