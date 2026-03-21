<?php defined('IN_MET') or exit('No permission'); ?>
<footer class="met-foot">
    <div class="footer-main container">
        <div class="footer-brand">
            <div style="font-size:20px; font-weight:700; color:#fff; margin-bottom:12px;">英语陪跑GO</div>
            <p>专注剑桥英语备考，KET/PET/FCE全阶段陪伴。每日干货推送，让英语学习不再孤单。</p>
        </div>
        <div class="footer-col">
            <h4>学习栏目</h4>
            <ul>
                <tag action='category' type='head' num='5'>
                <li><a href="{$m.url}">{$m.name}</a></li>
                </tag>
            </ul>
        </div>
        <div class="footer-col">
            <h4>备考资源</h4>
            <ul>
                <li><a href="#">KET词汇表</a></li>
                <li><a href="#">PET真题解析</a></li>
                <li><a href="#">写作模板</a></li>
                <li><a href="#">听力训练</a></li>
                <li><a href="#">单词对战游戏</a></li>
            </ul>
        </div>
        <div class="footer-col">
            <h4>关于我们</h4>
            <ul>
                <li><a href="javascript:void(0)" onclick="epgoEducation.showQRCode()">关注公众号</a></li>
                <if value="$c['met_foottel']"><li><a href="tel:{$c.met_foottel}">{$c.met_foottel}</a></li></if>
                <if value="$lang['company_email']"><li><a href="mailto:{$lang.company_email}">{$lang.company_email}</a></li></if>
            </ul>
        </div>
    </div>

    <!-- 友情链接 -->
    <tag action='link.list'></tag>
    <if value="$lang['link_ok'] && $sub">
    <div style="border-top:1px solid rgba(255,255,255,0.06); padding:16px 0; text-align:center;">
        <div class="container">
            <list data="$result" name="$v">
            <a href="{$v.weburl}" {$v.nofollow} target="_blank" style="color:rgba(255,255,255,0.4); font-size:13px; margin:0 10px; text-decoration:none;">{$v.webname}</a>
            </list>
        </div>
    </div>
    </if>

    <div class="footer-bottom container">
        <span>{$c.met_footright}</span>
        <if value="$c['met_foottext']"><span style="margin-left:16px;">{$c.met_foottext}</span></if>
        <if value="$lang['icp']">
        <a href="https://beian.miit.gov.cn" target="_blank" style="color:rgba(255,255,255,0.4); margin-left:16px; text-decoration:none;">{$lang.icp}</a>
        </if>
    </div>
</footer>

<script src="{$metui_url2}vendor/jquery/jquery-3.6.0.min.js"></script>
<script src="{$metui_url2}vendor/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="{$template_url}js/epgo-education.js?v=2026032201"></script>
<if value="$_M['html']['js']">
<list data="$_M['html']['js']" name="$v">
<script src="{$v}"></script>
</list>
</if>
{$g.foot}
<met_foot />
</body>
</html>
