<footer class='met-foot-info border-top1' m-id='met_foot' m-type="foot">
    <div class="met-footnav text-xs-center p-b-20" m-id='noset' m-type='foot_nav'>
    <div class="container">
        <div class="row mob-masonry epgo-footer-grid">
            <!-- 关于英语陪跑GO：页脚保持居中，给搜索和用户一个明确的品牌入口 -->
            <div class="col-lg-4 col-md-4 col-xs-12 info masonry-item epgo-footer-about">
                <h4 class='font-size-20 m-t-0'>关于英语陪跑GO</h4>
                <p class="epgo-footer-about-text">专注 KET / PET 学习内容、入学测评、英语学习工具和陪跑 App，帮助孩子建立可执行的学习路径。</p>
                <div class="epgo-footer-quicklinks">
                    <a href="/about/">了解我们</a>
                    <a href="/ket/">KET 备考</a>
                    <a href="/pet/">PET 备考</a>
                    <a href="/reading/">英语阅读</a>
                </div>
            </div>

            <!-- 关注我们二维码 -->
            <div class="col-lg-4 col-md-4 col-xs-12 info masonry-item epgo-footer-center" m-type="nocontent">
                <h4 class='font-size-20 m-t-0'>
                    {$lang.aboutus_text}
                </h4>
                <div class="erweima">
                    <div class="imgbox1 col-lg-6 col-md-6 col-xs-6">
                        <img src='{$lang.footinfo_wx|thumb:112,112}' alt='{$c.met_webname}'>
                        <p class="weixintext">{$lang.erweima_one}</p>
                    </div>
                    <div class="imgbox2 col-lg-6 col-md-6 col-xs-6">
                        <!-- <img src='{$lang.footinfo_wx2|thumb:112,112}' alt='{$c.met_webname}'>
                        <p class="weixintext">{$lang.erweima_two}</p> -->
                    </div>
                </div>
            </div>
            <!-- 关注我们二维码 -->

            <!-- 联系我们 -->
            <div class="col-lg-4 col-md-4 col-xs-12 info masonry-item epgo-footer-center font-size-20" m-id='met_contact' m-type="nocontent">
                <if value="$lang['footinfo_tel']">
                    <p class='font-size-20'>{$lang.footinfo_tel}</p>
                </if>
                <if value="$lang['footinfo_dsc']">
                    <?php $_phone = preg_replace('/[^0-9+\-]/', '', $lang['footinfo_dsc']); ?>
                    <p class="font-size-24">
                        <a href="tel:<?php echo $_phone; ?>" title="{$lang.footinfo_dsc}" rel="nofollow">{$lang.footinfo_dsc}</a>
                    </p>
                </if>
                <if value="$lang['wooktime_text']">
                    <p class="font-size-16 weekbox">
                        {$lang.wooktime_text}
                    </p>
                </if>
                <if value="$lang['footinfo_wx_ok']">
                    <a class="p-r-5" id="met-weixin" data-plugin="webuiPopover" data-trigger="hover" data-animation="pop" data-placement='top' data-width='155' data-padding='0' data-content="<div class='text-xs-center'>
                        <img src='{$lang.footinfo_wx}' alt='{$c.met_webname}' width='150' height='150' id='met-weixin-img'></div>
                    ">
                        <i class="fa fa-weixin"></i>
                    </a>
                </if>
                <if value="$lang['footinfo_qq_ok']">
                <a
                <if value="$lang['foot_info_qqtype'] eq 1">
                href="http://wpa.qq.com/msgrd?v=3&uin={$lang.footinfo_qq}&site=qq&menu=yes"
                <else/>
                href="http://crm2.qq.com/page/portalpage/wpa.php?uin={{$lang.footinfo_qq}&aty=0&a=0&curl=&ty=1"
                </if>
                rel="nofollow" target="_blank" class="p-r-5">
                    <i class="fa fa-qq"></i>
                </a>
                </if>
                <if value="$lang['footinfo_sina_ok']">
                <a href="{$lang.footinfo_sina}" rel="nofollow" target="_blank" class="p-r-5">
                    <i class="fa fa-weibo"></i>
                </a>
                </if>
                <if value="$lang['footinfo_twitterok']">
                <a href="{$lang.footinfo_twitter}" rel="nofollow" target="_blank" class="p-r-5">
                    <i class="fa fa-twitter red-600"></i>
                </a>
                </if>
                <if value="$lang['footinfo_googleok']">
                <a href="{$lang.footinfo_google}" rel="nofollow" target="_blank" class="p-r-5">
                    <i class="fa fa-google red-600"></i>
                </a>
                </if>
                <if value="$lang['footinfo_facebookok']">
                <a href="{$lang.footinfo_facebook}" rel="nofollow" target="_blank" class="p-r-5">
                    <i class="fa fa-facebook red-600"></i>
                </a>
                </if>
                <if value="$lang['footinfo_emailok']">
                <a href="mailto:{$lang.footinfo_email}" rel="nofollow" target="_blank" class="p-r-5">
                    <i class="fa fa-envelope red-600"></i>
                </a>
                </if>
            </div>
            <!-- 联系我们 -->


        </div>
    </div>
</div>

    <!-- 友情链接：只保留与英语学习主站直接相关的入口 -->
    <div class="met-link epgo-friend-link text-xs-center p-y-10" m-id='noset'>
        <div class="container">
            <span class="epgo-friend-label">友情链接：</span>
            <a class="epgo-friend-card" href="https://go.xiachaoqing.com/epgo/" title="英语陪跑GO App、KET/PET测评与学习工具" target="_blank">
                <strong>英语陪跑GO</strong>
                <span>KET/PET 测评 · 学习工具 · App 下载</span>
            </a>
        </div>
    </div>

    <style>
    .epgo-footer-grid{display:flex;align-items:stretch;}
    .epgo-footer-grid > [class*="col-"]{float:none;display:flex;flex-direction:column;align-items:center;text-align:center;}
    .epgo-footer-about-text{max-width:300px;margin:0 auto 16px;color:rgba(255,255,255,.62);font-size:13px;line-height:1.8;}
    .epgo-footer-quicklinks{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;font-size:13px;}
    .epgo-footer-quicklinks a{color:rgba(255,255,255,.82);}
    .epgo-footer-quicklinks a:hover{color:#fff;}
    .epgo-footer-center{text-align:center;}
    .epgo-footer-center .erweima{display:flex;justify-content:center;}
    .epgo-friend-link{border-top:1px solid rgba(255,255,255,.12);border-bottom:1px solid rgba(255,255,255,.12);}
    .epgo-friend-label{color:rgba(255,255,255,.55);font-size:13px;margin-right:10px;}
    .epgo-friend-card{display:inline-flex;align-items:center;gap:10px;color:#fff;text-decoration:none;}
    .epgo-friend-card strong{font-size:14px;font-weight:700;}
    .epgo-friend-card span{color:rgba(255,255,255,.58);font-size:12px;}
    .epgo-friend-card:hover strong{color:#8ec5ff;}
    .epgo-legal-links a{color:rgba(255,255,255,.72);}
    .epgo-legal-links a:hover{color:#fff;}
    @media(max-width:767px){
      .epgo-footer-grid{display:block;}
      .epgo-footer-grid > [class*="col-"]{display:block;margin-bottom:24px;}
      .epgo-friend-card{display:flex;flex-direction:column;gap:3px;margin:6px auto 0;}
      .epgo-friend-label{display:block;margin:0;}
    }
    </style>

    <div class="copy p-y-10 border-top1">
        <div class="container text-xs-center">
            <div class="epgo-legal-links" style="margin-bottom:8px;font-size:13px;">
                <a href="/privacy.html" rel="nofollow">隐私政策</a>
                <span style="margin:0 8px;opacity:.45;">|</span>
                <a href="/terms.html" rel="nofollow">服务条款</a>
                <span style="margin:0 8px;opacity:.45;">|</span>
                <a href="/about/">关于我们</a>
                <span style="margin:0 8px;opacity:.45;">|</span>
                <a href="/feedback/">联系我们</a>
            </div>
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
            <?php
                $_menu_url = trim($v['url']);
                if ($_menu_url == '' || $_menu_url == '../' || $_menu_url == '..//' || $_menu_url == './') $_menu_url = '/';
                if ($_menu_url && $_menu_url[0] != '/' && strpos($_menu_url, 'http') !== 0 && strpos($_menu_url, 'tel:') !== 0) $_menu_url = '/' . ltrim($_menu_url, './');
            ?>
            <div style="background-color: {$v.but_color};">
                <a href="<?php echo $_menu_url; ?>" class="item" <if value="$v['target']">target="_blank"</if> style="color: {$v.text_color};">
                    <i class="{$v.icon}"></i>
                    <span>{$v.name}</span>
                </a>
            </div>
        </tag>
    </div>
</div>
<met_foot />
