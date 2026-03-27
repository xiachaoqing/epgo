<?php defined('IN_MET') or exit('No permission'); ?>
<!-- ========== 页脚 ========== -->
<footer class="met-foot">
    <div class="container">
        <div class="footer-content">
            <!-- 关于我们 -->
            <div class="footer-section">
                <h4>关于EPGO</h4>
                <p style="color: rgba(255,255,255,0.7); font-size: 14px; line-height: 1.8;">
                    英语陪跑GO是一个专业的英语教育平台，专注于KET/PET考试培训和英语学习资源分享。
                </p>
                <div style="margin-top: 15px;">
                    <a href="javascript:void(0)" onclick="epgoEducation.showQRCode()" style="color: rgba(255,255,255,0.7); text-decoration: none; margin-right: 15px;">
                        <i class="icon wb-wechat" style="font-size: 18px;"></i>
                    </a>
                    <if value="$lang['footinfo_email']">
                    <a href="mailto:{$lang.footinfo_email}" style="color: rgba(255,255,255,0.7); text-decoration: none;">
                        <i class="icon wb-envelope" style="font-size: 18px;"></i>
                    </a>
                    </if>
                </div>
            </div>

            <!-- 快速链接 -->
            <div class="footer-section">
                <h4>快速链接</h4>
                <ul>
                    <li><a href="{$c.index_url}">首页</a></li>
                    <tag action='category' type='head' num='5'>
                    <li><a href="{$m.url}" title="{$m.name}">{$m._name}</a></li>
                    </tag>
                </ul>
            </div>

            <!-- 学习资源 -->
            <div class="footer-section">
                <h4>学习资源</h4>
                <ul>
                    <li><a href="#">KET考试教程</a></li>
                    <li><a href="#">PET考试教程</a></li>
                    <li><a href="#">词汇表下载</a></li>
                    <li><a href="#">真题精选</a></li>
                </ul>
            </div>

            <!-- 联系我们 -->
            <div class="footer-section">
                <h4>联系我们</h4>
                <ul style="list-style: none; padding: 0;">
                    <if value="$lang['footinfo_tel']">
                    <li style="margin-bottom: 10px;">
                        <i class="icon wb-mobile" style="margin-right: 8px;"></i>
                        {$lang.footinfo_tel}
                    </li>
                    </if>
                    <if value="$lang['footinfo_dsc']">
                    <li style="margin-bottom: 10px;">
                        <i class="icon wb-mobile" style="margin-right: 8px;"></i>
                        {$lang.footinfo_dsc}
                    </li>
                    </if>
                    <if value="$lang['footinfo_email']">
                    <li style="margin-bottom: 10px;">
                        <i class="icon wb-envelope" style="margin-right: 8px;"></i>
                        {$lang.footinfo_email}
                    </li>
                    </if>
                </ul>
            </div>
        </div>

        <!-- 友情链接 -->
        <tag action='link.list'></tag>
        <if value="$lang['link_ok'] && $sub">
        <div style="border-top:1px solid rgba(255,255,255,0.08); padding:14px 0;">
            <list data="$result" name="$v">
            <a href="{$v.weburl}" {$v.nofollow} target="_blank"
               style="color:rgba(255,255,255,0.4); font-size:13px; margin:0 10px; text-decoration:none;">{$v.webname}</a>
            </list>
        </div>
        </if>

        <!-- 页脚底部 -->
        <div class="footer-bottom">
            <p style="margin-bottom: 6px;">{$c.met_footright}</p>
            <if value="$c['met_footother']">
                <p style="color: rgba(255,255,255,0.5); font-size: 12px;">{$c.met_footother}</p>
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
