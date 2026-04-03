<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<!-- 内页顶部标题栏 -->
<div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);padding:40px 0 36px;text-align:center;">
    <div class="container">
        <h1 style="font-size:28px;font-weight:800;color:white;margin:0 0 8px;">{$data.title}</h1>
        <!-- 面包屑 -->
        <div style="font-size:13px;color:rgba(255,255,255,.7);">
            <a href="{$c.index_url}" style="color:rgba(255,255,255,.7);text-decoration:none;">首页</a>
            <span style="margin:0 8px;">›</span>
            <span style="color:white;">{$data.title}</span>
        </div>
    </div>
</div>

<section style="background:#F9FAFB;padding:40px 0 60px;min-height:400px;">
    <div class="container">
        <div style="max-width:860px;margin:0 auto;background:white;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.07);padding:40px;">
            <div class="met-editor epgo-show-content">
                {$data.content}
            </div>
        </div>
    </div>
</section>

<style>
.epgo-show-content{line-height:1.9;font-size:15px;color:#374151;}
.epgo-show-content h1,.epgo-show-content h2,.epgo-show-content h3{color:#111827;font-weight:700;margin-top:2em;margin-bottom:.8em;}
.epgo-show-content h2{font-size:22px;}
.epgo-show-content h3{font-size:18px;}
.epgo-show-content p{margin-bottom:1.2em;}
.epgo-show-content img{max-width:100%;border-radius:8px;}
.epgo-show-content a{color:#2563EB;}
.epgo-show-content ul,.epgo-show-content ol{padding-left:24px;margin-bottom:1.2em;}
.epgo-show-content li{margin-bottom:.5em;}
.epgo-show-content blockquote{border-left:4px solid #2563EB;padding:12px 20px;background:#EFF6FF;border-radius:0 8px 8px 0;margin:1.5em 0;color:#1e40af;}
@media(max-width:767px){
  .epgo-show-content{font-size:14px;}
  section .container > div{padding:20px !important;}
}
</style>

<include file="foot.php" />
