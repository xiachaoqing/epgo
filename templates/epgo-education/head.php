<met_meta page="$met_page" />
<?php
/* 动态查询子栏目，使用 PATH_CONFIG 常量定位配置文件 */
$_epgo_children = [];
try {
    $_epgo_raw  = file_get_contents(PATH_CONFIG . 'config_db.php');
    preg_match('/con_db_host\s*=\s*"([^"]+)"/', $_epgo_raw, $_eh);
    preg_match('/con_db_id\s*=\s*"([^"]+)"/',   $_epgo_raw, $_eu);
    preg_match('/con_db_pass\s*=\s*"([^"]+)"/',  $_epgo_raw, $_ep);
    preg_match('/con_db_name\s*=\s*"([^"]+)"/',  $_epgo_raw, $_en);
    preg_match('/tablepre\s*=\s*"([^"]+)"/',     $_epgo_raw, $_et);
    $_epgo_db = new mysqli($_eh[1]??'localhost', $_eu[1]??'', $_ep[1]??'', $_en[1]??'');
    if (!$_epgo_db->connect_error) {
        $_epgo_db->set_charset('utf8mb4');
        $_epgo_pre = $_et[1] ?? 'ep_';
        $_epgo_sql = 'SELECT id,name,foldername,bigclass FROM `' . $_epgo_pre . 'column`'
                   . ' WHERE bigclass>0 AND nav=1 AND isshow=1 ORDER BY no_order ASC';
        $_epgo_res = $_epgo_db->query($_epgo_sql);
        while ($_epgo_res && $_r = $_epgo_res->fetch_assoc()) {
            $_epgo_children[(int)$_r['bigclass']][] = $_r;
        }
        $_epgo_db->close();
    }
} catch (Exception $_ex) {}
unset($_epgo_raw,$_eh,$_eu,$_ep,$_en,$_et,$_epgo_db,$_epgo_pre,$_epgo_sql,$_epgo_res,$_r,$_ex);
?>
<header class='met-head' m-id='met_head' m-type="head_nav">
    <nav class="navbar navbar-default box-shadow-none met-nav" style="background:#1565C0;">
        <div class="container">
            <div class="row">
                <div class='met-nav-btn'>
                    <if value="$data['classnow'] eq 10001">
                    <h1 hidden>{$c.met_webname}</h1>
                    <else/>
                    <if value="!$data['id'] || $data['module'] eq 1">
                    <h1 hidden>{$data.name}</h1>
                    </if>
                    <h3 hidden>{$c.met_webname}</h3>
                    </if>
                    <div class="navbar-header pull-xs-left">
                        <a href="/" class="met-logo vertical-align block pull-xs-left" title="{$c.met_webname}">
                            <div class="vertical-align-middle">
                                <if value="$c['met_logo']">
                                    <img src="{$c.met_logo}" alt="{$c.met_webname}" class="pclogo mblogo" style="max-height:48px;" />
                                <else/>
                                    <span style="font-size:20px;font-weight:700;color:#fff;">{$c.met_webname}</span>
                                </if>
                            </div>
                        </a>
                    </div>
                    <button type="button" class="navbar-toggler hamburger hamburger-close collapsed p-x-5 p-y-0 met-nav-toggler" data-target="#met-nav-collapse" data-toggle="collapse">
                        <span class="sr-only"></span>
                        <span class="hamburger-bar"></span>
                    </button>
                </div>

                <div class="navbar-collapse-toolbar pull-md-right p-0 collapse" id="met-nav-collapse">
                    <ul class="nav navbar-nav navlist">
                        <li class='nav-item'>
                            <a href="/" title="{$word.home}" class="nav-link <if value="$data['classnow'] eq 10001">active</if>">{$word.home}</a>
                        </li>
                        <tag action='category' type='head' class='active'>
                        <?php
                            $_mid  = (int)$m['id'];
                            $_murl = trim($m['url']);
                            // 确保 URL 是绝对路径
                            if ($_murl && $_murl[0] !== '/' && strpos($_murl, 'http') !== 0) {
                                $_murl = '/' . ltrim($_murl, './');
                            }
                            $_nsub = isset($_epgo_children[$_mid]) ? $_epgo_children[$_mid] : [];
                        ?>
                        <?php if (!empty($_nsub)): ?>
                        <li class="nav-item dropdown">
                            <a href="<?php echo htmlspecialchars($_murl); ?>" title="{$m.name}" class="nav-link dropdown-toggle {$m.class}" data-toggle="dropdown" data-hover="dropdown">{$m._name}</a>
                            <div class="dropdown-menu dropdown-menu-right animate animate-reverse">
                                <?php foreach ($_nsub as $_sc):
                                    $_scurl = '/' . ltrim(trim($_sc['foldername']), '/') . '/list-' . $_sc['id'] . '.html';
                                ?>
                                <a href="<?php echo htmlspecialchars($_scurl); ?>" class="dropdown-item"><?php echo htmlspecialchars($_sc['name']); ?></a>
                                <?php endforeach; ?>
                            </div>
                        </li>
                        <?php else: ?>
                        <li class='nav-item'>
                            <a href="<?php echo htmlspecialchars($_murl); ?>" {$m.urlnew} title="{$m.name}" class="nav-link {$m.class}">{$m._name}</a>
                        </li>
                        <?php endif; ?>
                        </tag>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</header>
<style>
/* 蓝色下拉菜单 */
.met-nav .dropdown-menu {
  background: #1565C0 !important;
  border: none !important;
  border-radius: 0 !important;
  min-width: 140px;
  padding: 6px 0 !important;
  box-shadow: 0 8px 24px rgba(0,0,0,.18) !important;
}
.met-nav .dropdown-menu .dropdown-item {
  color: #fff !important;
  padding: 10px 18px !important;
  background: transparent !important;
  white-space: nowrap;
  display: block;
}
.met-nav .dropdown-menu .dropdown-item:hover {
  background: rgba(255,255,255,.18) !important;
  color: #fff !important;
}
/* 隐藏 banner 轮播黄色指示点 */
.met-banner .carousel-indicators {
  display: none !important;
}
/* 选中导航项无黄色下划线 */
.met-nav .nav li > a.active::after,
.met-nav .nav-item > a.active::after {
  display: none !important;
  background: transparent !important;
}
</style>

<if value="$data['classnow']">
<tag action="banner.list"></tag>
<if value="$sub || $data['classnow'] eq 10001">
<div class="met-banner carousel slide" id="exampleCarouselDefault" data-ride="carousel" m-id='banner' m-type='banner'>
    <ol class="carousel-indicators carousel-indicators-fall">
        <tag action="banner.list">
            <li data-slide-to="{$v._index}" data-target="#exampleCarouselDefault" class="<if value="$v['_first']">active</if>"></li>
        </tag>
    </ol>
    <if value="$sub">
        <a class="left carousel-control" href="#exampleCarouselDefault" role="button" data-slide="prev">
            <span class="icon" aria-hidden="true"><</span>
        </a>
        <a class="right carousel-control" href="#exampleCarouselDefault" role="button" data-slide="next">
            <span class="icon" aria-hidden="true">></span>
        </a>
    </if>
    <div class="carousel-inner <if value="$data['classnow'] eq 10001 && $sub eq 0">met-banner-mh</if>" role="listbox">
        <tag action="banner.list">
            <div class="carousel-item <if value="$v['_first']">active</if>">
                <if value="$v['mobile_img_path']">
                    <img class="w-full mobile_img" src="{$v.mobile_img_path}" alt="{$v.img_title_mobile}" pch="{$v.height}" adh="{$v.height_t}" iph="{$v.height_m}">
                    <img class="w-full pc_img" src="{$v.img_path}" alt="{$v.img_title}" pch="{$v.height}" adh="{$v.height_t}" iph="{$v.height_m}">
                <else/>
                    <img class="w-full mobile_img" src="{$v.img_path}" alt="{$v.img_title}" pch="{$v.height}" adh="{$v.height_t}" iph="{$v.height_m}">
                    <img class="w-full pc_img" src="{$v.img_path}" alt="{$v.img_title}" pch="{$v.height}" adh="{$v.height_t}" iph="{$v.height_m}">
                </if>
                <if value="$v['img_title'] || $v['img_des'] || $v['button'] || $v['img_link']">
                    <div class="met-banner-text pc-content" met-imgmask>
                        <div class='container'>
                            <div class='met-banner-text-con p-{$v.img_text_position}'>
                                <div><div>
                                <if value="$v['img_link']">
                                    <a href="{$v.img_link}" title="{$v.img_des}" class="all-imgmask" <if value="$v['target']">target="_blank"</if>></a>
                                </if>
                                <if value="$v['img_title']">
                                    <h3 class="animation-slide-top animation-delay-300 font-weight-500" style="color:{$v.img_title_color};font-size:{$v.img_title_fontsize}px;">{$v.img_title}</h3>
                                </if>
                                <if value="$v['img_des']">
                                    <p class="animation-slide-bottom animation-delay-600" style='color:{$v.img_des_color};font-size:{$v.img_des_fontsize}px;'>{$v.img_des}</p>
                                </if>
                                <list data="$v['button']" name="$btn">
                                    <a href="{$btn.but_url}" title="{$btn.but_text}" <if value="$btn['target']">target="_blank"</if> class="btn slick-btn" infoset="{$btn.but_text_size}|{$btn.but_text_color}|{$btn.but_text_hover_color}|{$btn.but_color}|{$btn.but_hover_color}|{$btn.but_x}|{$btn.but_y}">{$btn.but_text}</a>
                                </list>
                                </div></div>
                            </div>
                        </div>
                    </div>
                </if>
            </div>
        </tag>
    </div>
</div>
<else if value="$data['classnow'] neq 10001"/>
<tag action='category' type="current" cid="$data['classnow']">
<div class="met-banner-ny vertical-align text-center" m-id="banner">
    <if value="$m['module'] eq 1">
        <h2 class="vertical-align-middle">{$m.name}</h2>
    <else/>
        <h3 class="vertical-align-middle">{$m.name}</h3>
    </if>
</div>
</tag>
</if>
<if value="$data['classnow'] neq 10001">
    <if value="$data['name']">
        <include file="subcolumn_nav.php" />
    <else/>
        <include file="position.php" />
    </if>
</if>
</if>
