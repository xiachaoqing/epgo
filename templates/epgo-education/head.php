<met_meta page="$met_meta" />
<header class='met-head' m-id='met_head' m-type="head_nav">
    <nav class="navbar navbar-default box-shadow-none met-nav" style="background:#1565C0;">
        <div class="container">
            <div class="row">
                <div class='met-nav-btn'>
                    <if value="$data['classnow'] eq 10001">
                    <h1 hidden>{$c.met_webname}</h1>
                    <else/>
                    <h3 hidden>{$c.met_webname}</h3>
                    </if>
                    <div class="navbar-header pull-xs-left">
                        <a href="{$c.index_url}" class="met-logo vertical-align block pull-xs-left" title="{$c.met_webname}">
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
                        <span class="hamburger-bar" style="background:#fff;"></span>
                    </button>
                </div>

                <div class="navbar-collapse-toolbar pull-md-right p-0 collapse" id="met-nav-collapse">
                    <ul class="nav navbar-nav navlist">
                        <li class='nav-item'>
                            <a href="{$c.index_url}" title="{$word.home}" class="nav-link <if value="$data['classnow'] eq 10001">active</if>">{$word.home}</a>
                        </li>
                        <tag action='category' type='head' class='active'>
                        <if value="$m['sub']">
                        <li class="nav-item dropdown">
                            <a href="{$m.url}" title="{$m.name}" class="nav-link dropdown-toggle {$m.class}" data-toggle="dropdown" data-hover="dropdown">
                                {$m._name}
                            </a>
                            <div class="dropdown-menu dropdown-menu-right animate animate-reverse">
                                <tag action='category' cid="$m['id']" type='son' class='active'>
                                <if value="$m['sub']">
                                    <div class="dropdown-submenu">
                                        <a href="{$m.url}" class="dropdown-item {$m.class}">{$m._name}</a>
                                        <div class="dropdown-menu animate animate-reverse">
                                            <tag action='category' cid="$m['id']" type='son' class='active'>
                                                <a href="{$m.url}" class="dropdown-item {$m.class}">{$m._name}</a>
                                            </tag>
                                        </div>
                                    </div>
                                <else/>
                                    <a href="{$m.url}" title="{$m.name}" class='dropdown-item {$m.class}'>{$m._name}</a>
                                </if>
                                </tag>
                            </div>
                        </li>
                        <else/>
                        <li class='nav-item'>
                            <a href="{$m.url}" title="{$m.name}" class="nav-link {$m.class}">{$m._name}</a>
                        </li>
                        </if>
                        </tag>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</header>
