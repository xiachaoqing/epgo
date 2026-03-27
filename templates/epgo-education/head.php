<met_meta page="$met_page" />
<header class='met-head' m-id='met_head' m-type="head_nav">
    <nav class="navbar navbar-expand-lg" style="background:#1565C0; padding:12px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        <div class="container">
            <!-- Logo -->
            <a class="navbar-brand" href="{$c.index_url}" title="{$c.met_webname}" style="padding:6px 0;">
                <if value="$c['met_logo']">
                    <img src="{$c.met_logo}" alt="{$c.met_webname}" height="48" style="vertical-align:middle;">
                <else/>
                    <span style="font-size:22px; font-weight:700; color:#fff;">{$c.met_webname}</span>
                </if>
            </a>

            <!-- 导航切换按钮 -->
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navMenu"
                    aria-controls="navMenu" aria-expanded="false" aria-label="Toggle navigation"
                    style="border-color:rgba(255,255,255,0.5);">
                <span style="background-image:none; position:relative; display:inline-block; width:22px; height:18px;">
                    <span style="position:absolute; display:block; height:2px; width:100%; background:#fff; top:3px;"></span>
                    <span style="position:absolute; display:block; height:2px; width:100%; background:#fff; top:8px;"></span>
                    <span style="position:absolute; display:block; height:2px; width:100%; background:#fff; top:13px;"></span>
                </span>
            </button>

            <!-- 导航菜单 -->
            <div class="collapse navbar-collapse" id="navMenu">
                <ul class="navbar-nav ml-auto">
                    <!-- 首页 -->
                    <li class="nav-item">
                        <a href="{$c.index_url}" class="nav-link"
                           style="color:#fff; font-size:15px; padding:8px 14px; position:relative; transition:all 0.3s;
                                   <if value="$data['classnow'] eq 10001">border-bottom:3px solid #FFB81C;<else/>border-bottom:3px solid transparent;</if>"
                           title="{$word.home}">
                            {$word.home}
                        </a>
                    </li>

                    <!-- 一级栏目（带子菜单） -->
                    <tag action='category' type='head' class='active'>
                    <if value="$m['sub']">
                    <li class="nav-item dropdown" style="position:relative;">
                        <a class="nav-link dropdown-toggle" href="{$m.url}"
                           title="{$m.name}"
                           role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
                           style="color:#fff; font-size:15px; padding:8px 14px; display:flex; align-items:center;
                                   <if value="$m['class']">border-bottom:3px solid #FFB81C;<else/>border-bottom:3px solid transparent;</if>">
                            {$m._name}
                            <i class="fa fa-angle-down" style="margin-left:4px; font-size:12px;"></i>
                        </a>
                        <!-- 二级菜单 -->
                        <div class="dropdown-menu" style="background:#fff; border:none; box-shadow: 0 8px 16px rgba(0,0,0,0.15); border-radius:2px; padding:8px 0; min-width:200px;">
                            <tag action='category' cid="$m['id']" type='son' class='active'>
                            <if value="$m['sub']">
                            <!-- 三级菜单（更深层级） -->
                            <div class="dropdown-submenu" style="position:relative;">
                                <a class="dropdown-item" href="{$m.url}"
                                   title="{$m.name}"
                                   style="color:#333; font-size:14px; padding:10px 16px; display:flex; justify-content:space-between; align-items:center;
                                          <if value="$m['class']">background:#f0f0f0; border-left:3px solid #1565C0;<else/>background:transparent; border-left:3px solid transparent;</if>
                                          transition:all 0.2s;">
                                    {$m._name}
                                    <i class="fa fa-angle-right" style="font-size:12px; margin-left:8px;"></i>
                                </a>
                                <div class="dropdown-menu" style="background:#fff; border:none; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                                                                   position:absolute; left:100%; top:-5px; min-width:180px; padding:8px 0; border-radius:2px;">
                                    <tag action='category' cid="$m['id']" type='son' class='active'>
                                        <a class="dropdown-item" href="{$m.url}"
                                           title="{$m.name}"
                                           style="color:#333; font-size:13px; padding:8px 16px;
                                                  <if value="$m['class']">background:#E8F4FD; color:#1565C0;<else/>background:transparent;</if>
                                                  transition:all 0.2s;">
                                            {$m._name}
                                        </a>
                                    </tag>
                                </div>
                            </div>
                            <else/>
                            <!-- 只有二级 -->
                            <a class="dropdown-item" href="{$m.url}"
                               title="{$m.name}"
                               style="color:#333; font-size:14px; padding:10px 16px;
                                      <if value="$m['class']">background:#f0f0f0; border-left:3px solid #1565C0;<else/>background:transparent; border-left:3px solid transparent;</if>
                                      transition:all 0.2s;">
                                {$m._name}
                            </a>
                            </if>
                            </tag>
                        </div>
                    </li>
                    <else/>
                    <!-- 一级栏目（无子菜单） -->
                    <li class="nav-item">
                        <a class="nav-link" href="{$m.url}" title="{$m.name}"
                           style="color:#fff; font-size:15px; padding:8px 14px; position:relative; transition:all 0.3s;
                                   <if value="$m['class']">border-bottom:3px solid #FFB81C;<else/>border-bottom:3px solid transparent;</if>">
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
