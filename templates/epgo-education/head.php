<met_meta page="$met_page" />
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
                    <?php
                    $_epgo_children = array(
                        101 => array(
                            array('name'=>'KET真题解析','url'=>'/ket-exam/list-111.html'),
                            array('name'=>'KET词汇速记','url'=>'/ket-word/list-112.html'),
                            array('name'=>'KET写作指导','url'=>'/ket-write/list-113.html'),
                            array('name'=>'KET听力技巧','url'=>'/ket-listen/list-114.html'),
                        ),
                        102 => array(
                            array('name'=>'PET真题解析','url'=>'/pet-exam/list-121.html'),
                            array('name'=>'PET词汇速记','url'=>'/pet-word/list-122.html'),
                            array('name'=>'PET写作指导','url'=>'/pet-write/list-123.html'),
                            array('name'=>'PET阅读技巧','url'=>'/pet-read/list-124.html'),
                        ),
                    );
                    ?>
                    <ul class="nav navbar-nav navlist">
                        <li class='nav-item'>
                            <a href="/" title="{$word.home}" class="nav-link <if value="$data['classnow'] eq 10001">active</if>">{$word.home}</a>
                        </li>
                        <tag action='category' type='head' class='active'>
                        <?php $_nsub = isset($_epgo_children[(int)$m['id']]) ? $_epgo_children[(int)$m['id']] : array(); ?>
                        <if value="$_nsub">
                        <li class="nav-item dropdown">
                            <a href="{$m.url}" title="{$m.name}" class="nav-link dropdown-toggle {$m.class}" data-toggle="dropdown" data-hover="dropdown">{$m._name}</a>
                            <div class="dropdown-menu dropdown-menu-right animate animate-reverse">
                                <?php foreach($_nsub as $_sc){ ?>
                                <a href="<?php echo htmlspecialchars($_sc['url']); ?>" class="dropdown-item"><?php echo htmlspecialchars($_sc['name']); ?></a>
                                <?php } ?>
                            </div>
                        </li>
                        <else/>
                        <li class='nav-item'>
                            <a href="{$m.url}" {$m.urlnew} title="{$m.name}" class="nav-link {$m.class}">{$m._name}</a>
                        </li>
                        </if>
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
  min-width: 160px;
  padding: 6px 0 !important;
  box-shadow: 0 8px 24px rgba(0,0,0,.18) !important;
}
.met-nav .dropdown-menu > li > a,
.met-nav .dropdown-menu .dropdown-item {
  color: #fff !important;
  padding: 10px 18px !important;
  background: transparent !important;
  white-space: nowrap;
}
.met-nav .dropdown-menu > li > a:hover,
.met-nav .dropdown-menu .dropdown-item:hover {
  background: rgba(255,255,255,.15) !important;
  text-indent: 0 !important;
  color: #fff !important;
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
