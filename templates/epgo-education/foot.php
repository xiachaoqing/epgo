<?php defined('IN_MET') or exit('No permission'); ?>
<footer class="met-foot-info border-top1 epgo-footer" m-id="met_foot" m-type="foot">
    <!-- 页脚主体 -->
    <div class="met-footnav p-b-20" m-id="noset" m-type="foot_nav">
        <div class="container">
            <div class="row mob-masonry">

                <!-- 栏目导航 -->
                <div class="col-lg-6 col-md-12 col-xs-12 left_lanmu">
                    <tag action='category' type='foot'>
                    <if value="$m['_index'] lt 4">
                    <div class="col-lg-3 col-md-3 col-xs-6 masonry-item foot-nav">
                        <h4 class="font-size-16 m-t-0">
                            <a href="{$m.url}" {$m.urlnew} title="{$m.name}">{$m.name}</a>
                        </h4>
                        <if value="$m['sub']">
                        <ul class="ulstyle m-b-0">
                            <tag action='category' cid="$m['id']" type='son' num="5">
                            <li><a href="{$m.url}" {$m.urlnew} title="{$m.name}">{$m.name}</a></li>
                            </tag>
                        </ul>
                        </if>
                    </div>
                    </if>
                    </tag>
                </div>

                <!-- 公众号二维码 -->
                <div class="col-lg-3 col-md-3 col-xs-12 masonry-item" m-type="nocontent">
                    <h4 class="font-size-16 m-t-0">关注我们</h4>
                    <div class="erweima">
                        <div class="imgbox1 col-lg-8 col-md-8 col-xs-6">
                            <if value="$lang['footinfo_wx']">
                                <img src="{$lang.footinfo_wx|thumb:120,120}" alt="英语陪跑GO公众号"
                                     style="border-radius:6px;border:1px solid rgba(255,255,255,.2);">
                            </if>
                            <p class="weixintext" style="font-size:12px;margin-top:8px;">英语陪跑GO</p>
                        </div>
                    </div>
                </div>

                <!-- 联系信息 -->
                <div class="col-lg-3 col-md-3 col-xs-12 masonry-item" m-id="met_contact" m-type="nocontent">
                    <h4 class="font-size-16 m-t-0">联系我们</h4>
                    <if value="$lang['footinfo_tel']">
                        <p style="font-size:14px;">{$lang.footinfo_tel}</p>
                    </if>
                    <if value="$lang['footinfo_email']">
                        <p style="font-size:14px;">
                            <a href="mailto:{$lang.footinfo_email}" style="color:inherit;">{$lang.footinfo_email}</a>
                        </p>
                    </if>
                    <if value="$lang['wooktime_text']">
                        <p style="font-size:13px;opacity:.8;">{$lang.wooktime_text}</p>
                    </if>
                </div>

            </div>
        </div>
    </div>

    <!-- 友情链接 -->
    <tag action='link.list'></tag>
    <if value="$lang['link_ok'] && $sub">
    <div class="met-link text-xs-center p-y-10" m-id="noset" m-type="link">
        <div class="container">
            <ul class="breadcrumb p-0 link-img m-0">
                <li class="breadcrumb-item">{$lang.footlink_title}：</li>
                <list data="$result" name="$v">
                <li class="breadcrumb-item">
                    <a href="{$v.weburl}" title="{$v.info}" {$v.nofollow} target="_blank">
                        <if value="$v.link_type eq 1">
                            <img data-original="{$v.weblogo}" alt="{$v.info}" height="40">
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
            <if value="$c['met_footright']">
                <div class="met_footright" style="font-size:13px;opacity:.85;">
                    {$c.met_footright}
                </div>
            </if>
            <if value="$c['met_footother']">
                <div style="font-size:12px;opacity:.7;margin-top:4px;">{$c.met_footother}</div>
            </if>
            <if value="$c['met_foottext']">
                <div style="font-size:12px;opacity:.7;">{$c.met_foottext}</div>
            </if>
        </div>
    </div>
</footer>

<!-- 移动端底部菜单 -->
<div class="met-menu-list text-xs-center <if value="$_M['form']['pageset']">iskeshi</if>"
     m-id="noset" m-type="menu">
    <div class="main">
        <tag action="menu.list">
        <div style="background-color:{$v.but_color};">
            <a href="{$v.url}" class="item" <if value="$v['target']">target="_blank"</if>
               style="color:{$v.text_color};">
                <i class="{$v.icon}"></i>
                <span>{$v.name}</span>
            </a>
        </div>
        </tag>
    </div>
</div>

<met_foot />
