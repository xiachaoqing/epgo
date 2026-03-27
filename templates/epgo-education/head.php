<met_meta page="$met_page" />
<header class="met-head epgo-header" m-id="met_head" m-type="head_nav">
    <nav class="navbar navbar-default epgo-navbar">
        <div class="container">
            <div class="row">
                <!-- Logo + 汉堡按钮 -->
                <div class="met-nav-btn">
                    <if value="$data['classnow'] eq 10001">
                    <h1 hidden>{$c.met_webname}</h1>
                    <else/>
                    <if value="!$data['id'] || $data['module'] eq 1">
                    <h1 hidden>{$data.name}</h1>
                    </if>
                    <h3 hidden>{$c.met_webname}</h3>
                    </if>

                    <div class="navbar-header pull-xs-left">
                        <a href="{$c.index_url}" class="met-logo vertical-align block pull-xs-left" title="{$c.met_webname}">
                            <div class="vertical-align-middle">
                                <if value="$c['met_logo']">
                                    <img src="{$c.met_logo}" alt="{$c.met_webname}" class="pclogo" style="max-height:44px;">
                                    <img src="{$c.met_logo}" alt="{$c.met_webname}" class="mblogo" style="max-height:36px;">
                                <else/>
                                    <span class="epgo-logo-text">{$c.met_webname}</span>
                                </if>
                            </div>
                        </a>
                    </div>

                    <button type="button"
                            class="navbar-toggler hamburger hamburger-close collapsed p-x-5 p-y-0 met-nav-toggler"
                            data-target="#met-nav-collapse" data-toggle="collapse">
                        <span class="sr-only">菜单</span>
                        <span class="hamburger-bar"></span>
                    </button>
                </div>

                <!-- 导航菜单 -->
                <div class="navbar-collapse-toolbar pull-md-right p-0 collapse" id="met-nav-collapse">
                    <ul class="nav navbar-nav navlist">
                        <li class="nav-item">
                            <a href="{$c.index_url}" title="{$word.home}"
                               class="nav-link <if value="$data['classnow'] eq 10001">active</if>">{$word.home}</a>
                        </li>
                        <tag action='category' type='head' class='active'>
                        <if value="$m['sub']">
                        <li class="nav-item dropdown">
                            <a href="{$m.url}" title="{$m.name}" {$m.urlnew}
                               class="nav-link dropdown-toggle {$m.class}"
                               data-toggle="dropdown" data-hover="dropdown">{$m._name}</a>
                            <div class="dropdown-menu dropdown-menu-right animate animate-reverse">
                                <tag action='category' cid="$m['id']" type='son' class='active'>
                                <if value="$m['sub']">
                                    <div class="dropdown-submenu">
                                        <a href="{$m.url}" {$m.urlnew} class="dropdown-item {$m.class}">{$m._name}</a>
                                        <div class="dropdown-menu animate animate-reverse">
                                            <tag action='category' cid="$m['id']" type='son' class='active'>
                                                <a href="{$m.url}" {$m.urlnew} class="dropdown-item {$m.class}">{$m._name}</a>
                                            </tag>
                                        </div>
                                    </div>
                                <else/>
                                    <a href="{$m.url}" {$m.urlnew} title="{$m.name}" class="dropdown-item {$m.class}">{$m._name}</a>
                                </if>
                                </tag>
                            </div>
                        </li>
                        <else/>
                        <li class="nav-item">
                            <a href="{$m.url}" {$m.urlnew} title="{$m.name}" class="nav-link {$m.class}">{$m._name}</a>
                        </li>
                        </if>
                        </tag>

                        <!-- 公众号入口 -->
                        <li class="nav-item">
                            <a href="javascript:void(0)" class="nav-link epgo-qrcode-toggle"
                               onclick="document.getElementById('epgo-qrcode-modal').style.display='flex'">
                                关注公众号
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</header>

<!-- 二维码弹窗 -->
<div id="epgo-qrcode-modal"
     style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:9999;align-items:center;justify-content:center;"
     onclick="if(event.target===this)this.style.display='none'">
    <div style="background:#fff;border-radius:12px;padding:36px 40px;text-align:center;max-width:320px;width:90%;position:relative;">
        <button onclick="document.getElementById('epgo-qrcode-modal').style.display='none'"
                style="position:absolute;top:10px;right:14px;background:none;border:none;font-size:24px;color:#999;cursor:pointer;line-height:1;">×</button>
        <h4 style="margin:0 0 20px;font-size:18px;color:#1f2937;">关注公众号</h4>
        <if value="$lang['footinfo_wx']">
            <img src="{$lang.footinfo_wx}" alt="英语陪跑GO 公众号二维码"
                 style="width:200px;height:200px;border-radius:8px;border:1px solid #e5e7eb;">
        <else/>
            <div style="width:200px;height:200px;background:#f9fafb;border:2px dashed #d1d5db;border-radius:8px;display:flex;align-items:center;justify-content:center;margin:0 auto;">
                <span style="color:#9ca3af;font-size:13px;">二维码配置中</span>
            </div>
        </if>
        <p style="margin:16px 0 0;color:#6b7280;font-size:13px;">长按识别 · 关注英语陪跑GO</p>
    </div>
</div>

<!-- 非首页 Banner + 面包屑 -->
<if value="$data['classnow']">
<tag action="banner.list"></tag>
<if value="$sub || $data['classnow'] eq 10001">
<div class="met-banner carousel slide" id="epgoBanner" data-ride="carousel" m-id="banner" m-type="banner">
    <ol class="carousel-indicators carousel-indicators-fall">
        <tag action="banner.list">
        <li data-slide-to="{$v._index}" data-target="#epgoBanner"
            class="<if value="$v['_first']">active</if>"></li>
        </tag>
    </ol>
    <if value="$sub">
        <a class="left carousel-control" href="#epgoBanner" role="button" data-slide="prev">
            <span class="icon" aria-hidden="true"><</span>
        </a>
        <a class="right carousel-control" href="#epgoBanner" role="button" data-slide="next">
            <span class="icon" aria-hidden="true">></span>
        </a>
    </if>
    <div class="carousel-inner <if value="$data['classnow'] eq 10001 && $sub eq 0">met-banner-mh</if>" role="listbox">
        <tag action="banner.list">
        <div class="carousel-item <if value="$v['_first']">active</if>">
            <img class="w-full" src="{$v.img_path}" alt="{$v.img_title}"
                 pch="{$v.height}" adh="{$v.height_t}" iph="{$v.height_m}">
            <if value="$v['img_title'] || $v['img_des']">
            <div class="met-banner-text pc-content" met-imgmask>
                <div class="container">
                    <div class="met-banner-text-con p-{$v.img_text_position}">
                        <if value="$v['img_link']">
                            <a href="{$v.img_link}" class="all-imgmask" <if value="$v['target']">target="_blank"</if>></a>
                        </if>
                        <if value="$v['img_title']">
                            <h3 class="animation-slide-top animation-delay-300"
                                style="color:{$v.img_title_color}">{$v.img_title}</h3>
                        </if>
                        <if value="$v['img_des']">
                            <p class="animation-slide-bottom animation-delay-600"
                               style="color:{$v.img_des_color}">{$v.img_des}</p>
                        </if>
                    </div>
                </div>
            </div>
            </if>
        </div>
        </tag>
    </div>
</div>
<elseif value="$data['classnow'] neq 10001"/>
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
