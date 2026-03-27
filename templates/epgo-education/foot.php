<footer class='met-foot-info border-top1' m-id='met_foot' m-type="foot">
    <div class="met-footnav text-xs-center p-b-20" m-id='noset' m-type='foot_nav' style="background:linear-gradient(180deg, #ffffff 0%, #f9fafb 100%); border-top:1px solid #e5e7eb;">
    <div class="container">
        <div class="row mob-masonry" style="align-items:flex-start;">
            <!-- 特色功能区 -->
            <div class="col-lg-6 col-md-12 col-xs-12 left_lanmu" style="padding-right:20px; margin-bottom:30px;">
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:24px;">
                    <tag action='category' type='foot'>
                    <if value="$m['_index'] lt 4">
                    <div class="footer-feature-card" style="transition:all 0.3s ease; padding:20px; border-radius:8px; border-left:4px solid #2563eb; background:white;" onmouseover="this.style.background='#eff6ff'; this.style.transform='translateY(-4px)'" onmouseout="this.style.background='white'; this.style.transform='translateY(0)'">
                        <div style="font-size:24px; margin-bottom:12px; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.2)'" onmouseout="this.style.transform='scale(1)'">
                            <if value="$m['_index'] eq 0">🗺️</if>
                            <if value="$m['_index'] eq 1">🏷️</if>
                            <if value="$m['_index'] eq 2">🔍</if>
                            <if value="$m['_index'] eq 3">📱</if>
                        </div>
                        <h4 class='m-t-0 m-b-8' style="font-weight:700; color:#111827; font-size:15px;">
                            <a href="{$m.url}" {$m.urlnew} title="{$m.name}" style="color:inherit; text-decoration:none; transition:color 0.3s;" onmouseover="this.style.color='#2563eb'" onmouseout="this.style.color='#111827'">{$m.name}</a>
                        </h4>
                        <if value="$m['sub']">
                        <ul class='ulstyle m-b-0' style="list-style:none; padding:0; margin:0;">
                            <tag action='category' cid="$m['id']" type='son' num="3">
                            <li style="margin:4px 0;">
                                <a href="{$m.url}" {$m.urlnew} title="{$m.name}" style="color:#6b7280; text-decoration:none; font-size:13px; transition:all 0.2s; display:inline-block;" onmouseover="this.style.color='#2563eb'; this.style.transform='translateX(4px)'" onmouseout="this.style.color='#6b7280'; this.style.transform='translateX(0)'">{$m.name}</a>
                            </li>
                            </tag>
                        </ul>
                        </if>
                    </div>
                    </if>
                    </tag>
                </div>
            </div>
            <!-- 特色功能区结束 -->

            <!-- 关注我们二维码 -->
            <div class="col-lg-3 col-md-6 col-xs-12 info masonry-item" m-type="nocontent" style="margin-bottom:20px;">
                <div style="background:white; border-radius:12px; padding:24px; border:1px solid #e5e7eb; transition:all 0.3s;" onmouseover="this.style.boxShadow='0 12px 24px rgba(37,99,235,0.12)'; this.style.transform='translateY(-4px)'" onmouseout="this.style.boxShadow='0 1px 3px rgba(0,0,0,0.08)'; this.style.transform='translateY(0)'">
                    <h4 class='m-t-0 m-b-16' style="font-weight:700; font-size:15px; color:#111827; text-align:left;">
                        📱 {$lang.aboutus_text}
                    </h4>
                    <div class="erweima" style="text-align:center;">
                        <div class="imgbox1" style="margin-bottom:16px;">
                            <if value="$c['footinfo_wx']">
                                <img src="{$c.footinfo_wx|thumb:140,140}" alt="{$c.met_webname}" style="max-width:100%; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                            <else/>
                                <div style="width:140px; height:140px; background:#f3f4f6; display:flex; align-items:center; justify-content:center; border-radius:8px; margin:0 auto;">
                                    <span style="color:#9ca3af; font-size:12px;">二维码加载中</span>
                                </div>
                            </if>
                            <p class="weixintext" style="font-size:12px; color:#6b7280; margin-top:12px;">{$lang.erweima_one}</p>
                        </div>
                    </div>
                </div>
            </div>
            <!-- 关注我们二维码 -->

            <!-- 联系我们 -->
            <div class="col-lg-3 col-md-6 col-xs-12 info masonry-item" m-id='met_contact' m-type="nocontent" style="margin-bottom:20px;">
                <div style="background:linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%); border-radius:12px; padding:24px; border:1px solid #e5e7eb; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 24px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.08)'">
                    <p style='font-size:15px; font-weight:700; margin:0 0 16px 0; color:#111827;'>☎️ 联系我们</p>
                    <p class="font-size-22" style="margin:0 0 12px 0; font-weight:700;">
                        <a href="tel:17610721765" title="17610721765" style="color:#2563eb; text-decoration:none; transition:color 0.3s;" onmouseover="this.style.color='#1d4ed8'" onmouseout="this.style.color='#2563eb'">17610721765</a>
                    </p>
                    <p class="font-size-14 weekbox" style="margin:0 0 16px 0; color:#6b7280;">
                        ⏰ 工作日 9:00-18:00
                    </p>
                    <div style="display:flex; gap:12px; flex-wrap:wrap; justify-content:center;">
                        <if value="$lang['footinfo_wx_ok']">
                            <a class="p-r-5" id="met-weixin" data-plugin="webuiPopover" data-trigger="hover" data-animation="pop" data-placement='top' data-width='155' data-padding='0' data-content="<div class='text-xs-center'>
                                <img src='{$lang.footinfo_wx}' alt='{$c.met_webname}' width='150' height='150' id='met-weixin-img' style='border-radius:8px;'></div>
                            " style="display:inline-block; width:40px; height:40px; background:#eff6ff; border-radius:50%; line-height:40px; text-align:center; color:#2563eb; transition:all 0.3s; cursor:pointer;" title="微信" onmouseover="this.style.background='#2563eb'; this.style.color='white'" onmouseout="this.style.background='#eff6ff'; this.style.color='#2563eb'">
                                <i class="fa fa-weixin"></i>
                            </a>
                        </if>
                        <if value="$lang['footinfo_qq_ok']">
                        <a href="http://wpa.qq.com/msgrd?v=3&uin={$lang.footinfo_qq}&site=qq&menu=yes" rel="nofollow" target="_blank" style="display:inline-block; width:40px; height:40px; background:#eff6ff; border-radius:50%; line-height:40px; text-align:center; color:#2563eb; transition:all 0.3s; text-decoration:none;" title="QQ" onmouseover="this.style.background='#2563eb'; this.style.color='white'" onmouseout="this.style.background='#eff6ff'; this.style.color='#2563eb'">
                            <i class="fa fa-qq"></i>
                        </a>
                        </if>
                        <if value="$lang['footinfo_sina_ok']">
                        <a href="{$lang.footinfo_sina}" rel="nofollow" target="_blank" style="display:inline-block; width:40px; height:40px; background:#eff6ff; border-radius:50%; line-height:40px; text-align:center; color:#2563eb; transition:all 0.3s; text-decoration:none;" title="微博" onmouseover="this.style.background='#2563eb'; this.style.color='white'" onmouseout="this.style.background='#eff6ff'; this.style.color='#2563eb'">
                            <i class="fa fa-weibo"></i>
                        </a>
                        </if>
                        <if value="$lang['footinfo_emailok']">
                        <a href="mailto:{$lang.footinfo_email}" rel="nofollow" target="_blank" style="display:inline-block; width:40px; height:40px; background:#eff6ff; border-radius:50%; line-height:40px; text-align:center; color:#2563eb; transition:all 0.3s; text-decoration:none;" title="邮箱" onmouseover="this.style.background='#2563eb'; this.style.color='white'" onmouseout="this.style.background='#eff6ff'; this.style.color='#2563eb'">
                            <i class="fa fa-envelope"></i>
                        </a>
                        </if>
                    </div>
                </div>
            </div>
            <!-- 联系我们 -->


        </div>
    </div>
</div>

    <!--友情链接-->
    <tag action='link.list'></tag>
    <if value="$lang['link_ok'] && $sub">
    <div class="met-link text-xs-center p-y-10" m-id='noset' m-type='link'>
        <div class="container">
            <ul class="breadcrumb p-0 link-img m-0">
                <li class='breadcrumb-item'>{$lang.footlink_title} :</li>
                <list data="$result" name="$v">
                    <li class='breadcrumb-item'>
                        <a href="{$v.weburl}" title="{$v.info}" {$v.nofollow} target="_blank">
                            <if value="$v.link_type eq 1">
                                <img data-original="{$v.weblogo}" alt="{$v.info}" height='40'>
                            <else/>
                                <span>{$v.webname}</span>
                            </if>
                        </a>
                    </li>
                </list>
            </ul>
        </div>
    </div>
    </if>
    <!--友情链接-->

    <div class="copy p-y-10 border-top1">
        <div class="container text-xs-center">
            <if value="$c['met_footright'] || $c['met_footstat']">
                <div class="met_footright">
                    <span>{$c.met_footright}</span>&nbsp;
                    <if value="$c['met_foottel']">
                        <span>{$c.met_foottel}</span>&nbsp;
                    </if>

                    <if value="$c['met_footaddress']">
                        <span>{$c.met_footaddress}</span>
                    </if>
                </div>
            </if>
            <if value="$c['met_footother']">
                <div>{$c.met_footother}</div>
            </if>
            <if value="$c['met_foottext']">
                <div>{$c.met_foottext}</div>
            </if>
                <if value="$c['met_ch_lang'] && $lang['cn1_position'] eq 0">
                    <if value="$lang['cn1_ok']">
                    <if value="$data['synchronous'] eq 'cn' || $data['synchronous'] eq 'zh'">
                        <button type="button" class="btn btn-outline btn-default btn-squared btn-lang" id='btn-convert' m-id="lang" m-type="lang">繁体</button>
                    </if>
                    </if>
                </if>
                <if value="$c['met_lang_mark'] && $lang['langlist_position'] eq 0">
                <div class="met-langlist vertical-align" m-id="lang"  m-type="lang">
                    <div class="inline-block dropup">

                        <lang>
                        <if value="$sub gt 1">
                            <if value="$data['lang'] eq $v['mark']">
                            <button type="button" data-toggle="dropdown" class="btn btn-outline btn-default btn-squared dropdown-toggle btn-lang">
                                <if value="$lang['langlist1_icon_ok']">
                                <img src="{$v.flag}" alt="{$v.name}" width="20">
                                </if>
                                <span>{$v.name}</span>
                            </button>
                            </if>
                        <else/>
                            <a href="{$v.met_weburl}" title="{$v.name}" class="btn btn-outline btn-default btn-squared btn-lang" <if value="$v['newwindows'] eq 1">target="_blank"</if>>
                                <if value="$lang['langlist1_icon_ok']">
                                <img src="{$v.flag}" alt="{$v.name}" width="20">
                                </if>
                                {$v.name}
                            </a>
                        </if>
                        </lang>
                        <if value="$sub gt 1">
                            <ul class="dropdown-menu dropdown-menu-right animate animate-reverse" id="met-langlist-dropdown" role="menu">
                                <lang>
                                <a href="{$v.met_weburl}" title="{$v.name}" class='dropdown-item' <if value="$v['newwindows'] eq 1">target="_blank"</if>>
                                    <if value="$lang['langlist1_icon_ok']">
                                    <img src="{$v.flag}" alt="{$v.name}" width="20">
                                    </if>
                                    {$v.name}
                                </a>
                                </lang>
                            </ul>
                        </if>
                    </div>
                </div>
                </if>
            </div>
        </div>
    </div>


</footer>
<div class="met-menu-list text-xs-center <if value="$_M['form']['pageset']">iskeshi</if>" m-id="noset" m-type="menu">
    <div class="main">
        <tag action="menu.list">
            <div style="background-color: {$v.but_color};">
                <a href="{$v.url}" class="item" <if value="$v['target']">target="_blank"</if> style="color: {$v.text_color};">
                    <i class="{$v.icon}"></i>
                    <span>{$v.name}</span>
                </a>
            </div>
        </tag>
    </div>
</div>
<met_foot />

<!-- 微信SDK初始化 -->
<script src="https://res.wx.qq.com/open/js/jweixin-1.6.0.js"></script>

<!-- 全局脚本 -->
<script>
// 修复子栏目CSS路径问题
window.addEventListener('load', function() {
    var links = document.querySelectorAll('link[rel="stylesheet"]');
    links.forEach(function(link) {
        var href = link.getAttribute('href');
        if (href && href.startsWith('../')) {
            var newHref = href.replace(/^\.\.\//, '/');
            var newLink = document.createElement('link');
            newLink.rel = 'stylesheet';
            newLink.type = 'text/css';
            newLink.href = newHref;
            document.head.appendChild(newLink);
        }
    });
});

// 微信分享配置（后端可通过meta标签或JS传入）
(function() {
    // 如果后端配置了微信AppID，则初始化分享
    var appId = '{$c.met_weixin_appid}'; // 从后端配置读取
    if (appId && appId.length > 0 && window.wx) {
        // 获取签名等信息（通常由后端计算）
        // 这里简化处理，实际应通过API获取
        console.log('微信分享SDK已加载');
    }
})();

// 页面分析和跟踪
(function() {
    // 谷歌分析（如果配置）
    if (window.gtag) {
        gtag('config', 'GA_MEASUREMENT_ID', {
            'page_path': window.location.pathname
        });
    }
})();
</script>