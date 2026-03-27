<?php defined('IN_MET') or exit('No permission'); ?><met_meta page="$met_page" />
<!-- 顶部导航栏 -->
<nav class="met-head navbar navbar-expand-md navbar-light" m-id="met_head" m-type="head_nav">
    <div class="container">
        <a class="navbar-brand" href="{$c.index_url}">
            <if value="$c['met_logo']">
                <img src="{$c.met_logo}" alt="{$c.met_webname}" style="max-height:44px;">
            <else/>
                <span>{$c.met_webname}</span>
            </if>
        </a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a href="{$c.index_url}" class="nav-link<if value="$data['classnow'] eq 10001"> active</if>">首页</a>
                </li>
                <tag action='category' type='head'>
                    <if value="$m['sub']">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle<if value="$m['class']"> active</if>"
                               href="{$m.url}" role="button"
                               data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                {$m._name}
                            </a>
                            <div class="dropdown-menu">
                                <tag action='category' cid="$m['id']" type='son'>
                                    <a class="dropdown-item" href="{$m.url}">{$m._name}</a>
                                </tag>
                            </div>
                        </li>
                    <else/>
                        <li class="nav-item">
                            <a class="nav-link<if value="$m['class']"> active</if>" href="{$m.url}">{$m._name}</a>
                        </li>
                    </if>
                </tag>
                <li class="nav-item">
                    <a href="javascript:void(0)" class="nav-link" onclick="document.getElementById('qrcode-modal').style.display='flex'">
                        关注公众号
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<!-- 公众号二维码弹窗 -->
<div id="qrcode-modal" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);align-items:center;justify-content:center;z-index:2000;">
    <div style="background:#fff;padding:40px;border-radius:12px;text-align:center;position:relative;max-width:360px;width:90%;">
        <span onclick="document.getElementById('qrcode-modal').style.display='none'"
              style="position:absolute;top:12px;right:18px;font-size:26px;cursor:pointer;color:#999;">&times;</span>
        <h4 style="margin-bottom:16px;">关注公众号</h4>
        <if value="$lang['wechat_qrcode']">
            <img src="{$lang.wechat_qrcode}" alt="微信公众号二维码" style="width:200px;height:200px;">
        <else/>
            <div style="width:200px;height:200px;background:#f5f5f5;display:flex;align-items:center;justify-content:center;margin:0 auto;border-radius:8px;">
                <span style="color:#aaa;font-size:13px;">二维码配置中</span>
            </div>
        </if>
        <p style="margin-top:14px;color:#888;font-size:13px;">长按识别二维码关注</p>
    </div>
</div>
