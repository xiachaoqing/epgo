<met_meta page="$met_page" />
<header class='met-head' m-id='met_head' m-type="head_nav">
    <nav class="navbar navbar-expand-md navbar-light" style="background:#fff; border-bottom:1px solid #eee; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <div class="container">
            <!-- Logo -->
            <a class="navbar-brand" href="{$c.index_url}" title="{$c.met_webname}">
                <if value="$c['met_logo']">
                    <img src="{$c.met_logo}" alt="{$c.met_webname}" height="40">
                <else/>
                    <span style="font-size:18px; font-weight:700; color:#1E88E5;">{$c.met_webname}</span>
                </if>
            </a>

            <!-- 导航切换按钮 -->
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navMenu" aria-controls="navMenu" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <!-- 导航菜单 -->
            <div class="collapse navbar-collapse" id="navMenu">
                <ul class="navbar-nav ml-auto">
                    <!-- 首页 -->
                    <li class="nav-item">
                        <a href="{$c.index_url}" class="nav-link <if value="$data['classnow'] eq 10001">active</if>" title="{$word.home}">
                            {$word.home}
                        </a>
                    </li>

                    <!-- 一级栏目（带子菜单） -->
                    <tag action='category' type='head' class='active'>
                    <if value="$m['sub']">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle {$m.class}" href="{$m.url}"
                           title="{$m.name}"
                           role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            {$m._name}
                        </a>
                        <!-- 二级菜单 -->
                        <div class="dropdown-menu" style="border:1px solid #eee; box-shadow: 0 8px 16px rgba(0,0,0,0.1); border-radius:4px; padding:4px;">
                            <tag action='category' cid="$m['id']" type='son' class='active'>
                            <if value="$m['sub']">
                            <!-- 三级菜单（更深层级） -->
                            <div class="dropdown-submenu">
                                <a class="dropdown-item" href="{$m.url}"
                                   title="{$m.name}" {$m.class}>
                                    {$m._name}
                                    <i class="fa fa-angle-right" style="margin-left:8px;"></i>
                                </a>
                                <div class="dropdown-menu" style="border:1px solid #eee; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-radius:4px;">
                                    <tag action='category' cid="$m['id']" type='son' class='active'>
                                        <a class="dropdown-item" href="{$m.url}"
                                           title="{$m.name}" {$m.class}>
                                            {$m._name}
                                        </a>
                                    </tag>
                                </div>
                            </div>
                            <else/>
                            <!-- 只有二级 -->
                            <a class="dropdown-item" href="{$m.url}"
                               title="{$m.name}" {$m.class}>
                                {$m._name}
                            </a>
                            </if>
                            </tag>
                        </div>
                    </li>
                    <else/>
                    <!-- 一级栏目（无子菜单） -->
                    <li class="nav-item">
                        <a class="nav-link {$m.class}" href="{$m.url}" title="{$m.name}">
                            {$m._name}
                        </a>
                    </li>
                    </if>
                    </tag>
                </ul>
            </div>
        </div>
    </nav>
</header>
