<?php defined('IN_MET') or exit('No permission'); ?>
<footer class='met-foot-info border-top1' m-id='met_foot' m-type="foot">
    <div class="met-footnav p-b-20" m-id='noset' m-type='foot_nav'>
        <div class="container">
            <div class="row mob-masonry">

                <!-- 特色功能（栏目导航） -->
                <div class="col-lg-3 col-md-3 col-xs-12 masonry-item foot-nav">
                    <h4 class='font-size-20 m-t-0'>特色功能</h4>
                    <ul class='ulstyle m-b-0'>
                        <tag action='category' type='foot'>
                        <if value="$m['_index'] lt 3">
                        <li>
                            <a href="{$m.url}" title="{$m.name}">{$m.name}</a>
                        </li>
                        </if>
                        </tag>
                        <li><a href="{$url.site}sitemap/">网站地图</a></li>
                        <li><a href="{$url.site}tags/">聚合标签</a></li>
                        <li><a href="{$url.site}search/">站内搜索</a></li>
                    </ul>
                </div>

                <!-- 占位 -->
                <div class="col-lg-3 col-md-3 col-xs-12 masonry-item"></div>

                <!-- 关注我们二维码 -->
                <div class="col-lg-3 col-md-3 col-xs-12 info masonry-item" m-type="nocontent">
                    <h4 class='font-size-20 m-t-0'>关注我们</h4>
                    <div class="erweima">
                        <div class="imgbox1">
                            <if value="$lang['footinfo_wx']">
                                <img src='{$lang.footinfo_wx}' alt='{$c.met_webname}' style="width:130px;height:130px;">
                            </if>
                            <p class="weixintext">
                                <if value="$lang['erweima_one']">{$lang.erweima_one}<else/>关注公众号</if>
                            </p>
                        </div>
                    </div>
                </div>

                <!-- 联系我们 -->
                <div class="col-lg-3 col-md-3 col-xs-12 info masonry-item font-size-20" m-id='met_contact' m-type="nocontent">
                    <h4 class='font-size-20 m-t-0'>联系我们</h4>
                    <if value="$lang['footinfo_tel']">
                        <p class='font-size-20'>{$lang.footinfo_tel}</p>
                    </if>
                    <if value="$lang['footinfo_dsc']">
                        <p class="font-size-24">
                            <a href="tel:{$lang.footinfo_dsc}" title="{$lang.footinfo_dsc}">{$lang.footinfo_dsc}</a>
                        </p>
                    </if>
                    <if value="$lang['wooktime_text']">
                        <p class="font-size-16 weekbox">{$lang.wooktime_text}</p>
                    </if>
                    <if value="$lang['footinfo_wx_ok']">
                        <a class="p-r-5" id="met-weixin" data-plugin="webuiPopover" data-trigger="hover" data-animation="pop" data-placement='top' data-width='155' data-padding='0'
                           data-content="<div class='text-xs-center'><img src='{$lang.footinfo_wx}' alt='{$c.met_webname}' width='150' height='150'></div>">
                            <i class="fa fa-weixin"></i>
                        </a>
                    </if>
                </div>

            </div>
        </div>
    </div>

    <!-- 友情链接 -->
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

    <!-- 版权信息 -->
    <div class="copy p-y-10 border-top1">
        <div class="container text-xs-center">
            <if value="$c['met_footright'] || $c['met_footstat']">
                <div class="met_footright">
                    <span>{$c.met_footright}</span>
                    <if value="$c['met_foottel']"><span>&nbsp;{$c.met_foottel}</span></if>
                    <if value="$c['met_footaddress']"><span>&nbsp;{$c.met_footaddress}</span></if>
                </div>
            </if>
            <if value="$c['met_footother']"><div>{$c.met_footother}</div></if>
            <if value="$c['met_foottext']"><div>{$c.met_foottext}</div></if>
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
