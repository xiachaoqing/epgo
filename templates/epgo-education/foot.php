<footer class='met-foot-info' m-id='met_foot' m-type="foot" style="background:#1A2340; color:rgba(255,255,255,0.8);">
    <div class="met-footnav" style="padding:40px 0; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div class="container">
            <div class="row" style="display:grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap:30px;">

                <!-- 栏目导航 -->
                <div class="footer-col">
                    <tag action='category' type='head' num='4'>
                    <if value="$m['_index'] lt 4">
                    <div style="margin-bottom:20px;">
                        <h4 style="color:#fff; font-size:14px; font-weight:600; margin:0 0 14px 0; padding:0;">
                            <a href="{$m.url}" title="{$m.name}"
                               style="color:#fff; text-decoration:none; transition:color 0.3s;">
                                {$m.name}
                            </a>
                        </h4>
                        <if value="$m['sub']">
                        <ul style="list-style:none; padding:0; margin:0;">
                            <tag action='category' cid="$m['id']" type='son' num='5'>
                            <li style="margin-bottom:6px;">
                                <a href="{$m.url}" title="{$m.name}"
                                   style="color:rgba(255,255,255,0.6); font-size:13px; text-decoration:none; transition:color 0.3s;">
                                    {$m._name}
                                </a>
                            </li>
                            </tag>
                        </ul>
                        </if>
                    </div>
                    </if>
                    </tag>
                </div>

                <!-- 公众号二维码 -->
                <div class="footer-col" m-type="nocontent">
                    <h4 style="color:#fff; font-size:14px; font-weight:600; margin:0 0 14px 0; padding:0;">
                        公众号
                    </h4>
                    <if value="$lang['footinfo_wx']">
                    <div style="text-align:center;">
                        <img src="{$lang.footinfo_wx}" alt="{$c.met_webname}"
                             style="width:140px; height:140px; border-radius:4px; display:block; margin-bottom:8px;">
                        <p style="color:rgba(255,255,255,0.6); font-size:12px; margin:0;">
                            <if value="$lang['erweima_one']">{$lang.erweima_one}<else/>扫码关注</if>
                        </p>
                    </div>
                    <else/>
                    <div style="width:140px; height:140px; background:rgba(255,255,255,0.1); border-radius:4px;
                                display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,0.4); font-size:12px;">
                        二维码待配置
                    </div>
                    </if>
                </div>

                <!-- 联系我们 -->
                <div class="footer-col" m-id='met_contact' m-type="nocontent">
                    <h4 style="color:#fff; font-size:14px; font-weight:600; margin:0 0 14px 0; padding:0;">
                        联系我们
                    </h4>
                    <div style="font-size:13px;">
                        <if value="$lang['footinfo_tel']">
                        <p style="color:rgba(255,255,255,0.6); margin:0 0 8px 0;">
                            <i class="fa fa-phone" style="margin-right:6px; width:16px; text-align:center;"></i>
                            <if value="$lang['footinfo_tel']">{$lang.footinfo_tel}</if>
                        </p>
                        </if>
                        <if value="$lang['footinfo_dsc']">
                        <p style="color:rgba(255,255,255,0.6); margin:0 0 8px 0;">
                            <a href="tel:{$lang.footinfo_dsc}"
                               style="color:rgba(255,255,255,0.6); text-decoration:none; transition:color 0.3s;">
                                <i class="fa fa-phone" style="margin-right:6px; width:16px; text-align:center;"></i>
                                {$lang.footinfo_dsc}
                            </a>
                        </p>
                        </if>
                        <if value="$lang['footinfo_email']">
                        <p style="color:rgba(255,255,255,0.6); margin:0;">
                            <a href="mailto:{$lang.footinfo_email}"
                               style="color:rgba(255,255,255,0.6); text-decoration:none; transition:color 0.3s;">
                                <i class="fa fa-envelope" style="margin-right:6px; width:16px; text-align:center;"></i>
                                {$lang.footinfo_email}
                            </a>
                        </p>
                        </if>
                    </div>
                </div>

                <!-- 关于我们 -->
                <div class="footer-col" m-type="nocontent">
                    <h4 style="color:#fff; font-size:14px; font-weight:600; margin:0 0 14px 0; padding:0;">
                        关于我们
                    </h4>
                    <p style="color:rgba(255,255,255,0.6); font-size:13px; line-height:1.8; margin:0;">
                        英语陪跑GO 是一个专业的英语教育平台，专注于 KET/PET 考试培训和英语学习资源分享。每日干货推送，让英语学习不再孤单。
                    </p>
                </div>

            </div>
        </div>
    </div>

    <!-- 友情链接 -->
    <tag action='link.list'></tag>
    <if value="$lang['link_ok'] && $sub">
    <div class="met-link" style="padding:12px 0; border-top:1px solid rgba(255,255,255,0.06); border-bottom:1px solid rgba(255,255,255,0.06);"
         m-id='noset' m-type='link'>
        <div class="container">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; justify-content:center;">
                <span style="color:rgba(255,255,255,0.5); font-size:13px;">友情链接：</span>
                <list data="$result" name="$v">
                    <a href="{$v.weburl}" title="{$v.info}" {$v.nofollow} target="_blank"
                       style="color:rgba(255,255,255,0.5); font-size:12px; text-decoration:none; transition:color 0.3s;">
                        {$v.webname}
                    </a>
                </list>
            </div>
        </div>
    </div>
    </if>

    <!-- 页脚底部 -->
    <div class="copy" style="padding:20px 0; text-align:center;">
        <div class="container">
            <div style="color:rgba(255,255,255,0.5); font-size:12px; line-height:1.8;">
                <if value="$c['met_footright']">
                    <div>{$c.met_footright}</div>
                </if>
                <if value="$c['met_foottel']">
                    <div>{$c.met_foottel}</div>
                </if>
                <if value="$c['met_footother']">
                    <div>{$c.met_footother}</div>
                </if>
                <if value="$c['met_foottext']">
                    <div>{$c.met_foottext}</div>
                </if>
            </div>
        </div>
    </div>
</footer>

<!-- 移动底部菜单 -->
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
