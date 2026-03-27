<?php defined('IN_MET') or exit('No permission'); ?>
<footer class="met-foot" style="background:#2C3E50; color:rgba(255,255,255,0.75);">
    <div class="container">
        <!-- 页脚内容 3列布局 -->
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:40px; padding:40px 0;
                    border-bottom:1px solid rgba(255,255,255,0.1);">

            <!-- 特色功能 -->
            <div class="footer-col" style="color:rgba(255,255,255,0.75);">
                <h4 style="color:#fff; font-size:14px; font-weight:600; margin:0 0 14px 0;">特色功能</h4>
                <ul style="list-style:none; padding:0; margin:0;">
                    <tag action='category' type='head' num='4'>
                    <li style="margin-bottom:8px;">
                        <a href="{$m.url}" title="{$m.name}"
                           style="color:rgba(255,255,255,0.6); font-size:13px; text-decoration:none; transition:color 0.3s;">
                            {$m._name}
                        </a>
                    </li>
                    </tag>
                    <li style="margin-bottom:8px;">
                        <a href="#" style="color:rgba(255,255,255,0.6); font-size:13px; text-decoration:none; transition:color 0.3s;">
                            网站地图
                        </a>
                    </li>
                    <li style="margin-bottom:8px;">
                        <a href="#" style="color:rgba(255,255,255,0.6); font-size:13px; text-decoration:none; transition:color 0.3s;">
                            聚合标签
                        </a>
                    </li>
                    <li>
                        <a href="#" style="color:rgba(255,255,255,0.6); font-size:13px; text-decoration:none; transition:color 0.3s;">
                            站内搜索
                        </a>
                    </li>
                </ul>
            </div>

            <!-- 关注我们 -->
            <div class="footer-col" style="text-align:center;">
                <h4 style="color:#fff; font-size:14px; font-weight:600; margin:0 0 14px 0;">关注我们</h4>
                <div style="display:flex; justify-content:center; align-items:center; flex-direction:column;">
                    <if value="$lang['footinfo_wx']">
                    <img src="{$lang.footinfo_wx}" alt="{$c.met_webname}"
                         style="width:130px; height:130px; border-radius:4px; margin-bottom:10px;">
                    <p style="color:rgba(255,255,255,0.5); font-size:12px; margin:0;">
                        <if value="$lang['erweima_one']">{$lang.erweima_one}<else/>扫码关注公众号</if>
                    </p>
                    <else/>
                    <div style="width:130px; height:130px; background:rgba(255,255,255,0.1); border-radius:4px;
                                display:flex; align-items:center; justify-content:center; color:rgba(255,255,255,0.3); font-size:12px; margin-bottom:10px;">
                        二维码待配置
                    </div>
                    </if>
                </div>
            </div>

            <!-- 联系我们 -->
            <div class="footer-col" style="color:rgba(255,255,255,0.75);">
                <h4 style="color:#fff; font-size:14px; font-weight:600; margin:0 0 14px 0;">联系我们</h4>
                <div style="font-size:13px;">
                    <if value="$lang['footinfo_tel']">
                    <p style="margin:0 0 10px 0; color:rgba(255,255,255,0.6);">
                        <i class="fa fa-phone" style="margin-right:6px; width:16px; text-align:center;"></i>
                        {$lang.footinfo_tel}
                    </p>
                    </if>
                    <if value="$lang['footinfo_dsc']">
                    <p style="margin:0 0 10px 0; color:rgba(255,255,255,0.6);">
                        <i class="fa fa-mobile" style="margin-right:6px; width:16px; text-align:center;"></i>
                        {$lang.footinfo_dsc}
                    </p>
                    </if>
                    <if value="$lang['footinfo_email']">
                    <p style="margin:0 0 10px 0; color:rgba(255,255,255,0.6);">
                        <i class="fa fa-envelope" style="margin-right:6px; width:16px; text-align:center;"></i>
                        <a href="mailto:{$lang.footinfo_email}"
                           style="color:rgba(255,255,255,0.6); text-decoration:none; transition:color 0.3s;">
                            {$lang.footinfo_email}
                        </a>
                    </p>
                    </if>
                    <if value="$lang['wooktime_text']">
                    <p style="margin:0; color:rgba(255,255,255,0.5); font-size:12px;">
                        <i class="fa fa-clock-o" style="margin-right:6px; width:16px; text-align:center;"></i>
                        {$lang.wooktime_text}
                    </p>
                    </if>
                </div>
            </div>

        </div>

        <!-- 友情链接 -->
        <tag action='link.list'></tag>
        <if value="$lang['link_ok'] && $sub">
        <div style="padding:12px 0; text-align:center; border-bottom:1px solid rgba(255,255,255,0.1);">
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; justify-content:center;">
                <span style="color:rgba(255,255,255,0.4); font-size:12px;">友情链接：</span>
                <list data="$result" name="$v">
                    <a href="{$v.weburl}" title="{$v.info}" {$v.nofollow} target="_blank"
                       style="color:rgba(255,255,255,0.4); font-size:12px; text-decoration:none; transition:color 0.3s;">
                        {$v.webname}
                    </a>
                </list>
            </div>
        </div>
        </if>

        <!-- 版权信息 -->
        <div style="padding:16px 0; text-align:center; color:rgba(255,255,255,0.4); font-size:12px;">
            <if value="$c['met_footright']">
                <p style="margin:0 0 4px 0;">{$c.met_footright}</p>
            </if>
            <if value="$c['met_foottel']">
                <p style="margin:0 0 4px 0;">{$c.met_foottel}</p>
            </if>
            <if value="$c['met_footother']">
                <p style="margin:0 0 4px 0;">{$c.met_footother}</p>
            </if>
            <if value="$c['met_foottext']">
                <p style="margin:0;">{$c.met_foottext}</p>
            </if>
        </div>
    </div>
</footer>

<!-- 移动端底部菜单 -->
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
