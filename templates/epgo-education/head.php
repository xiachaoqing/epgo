<met_meta page="$met_page" />
<header class='met-head' m-id='met_head' m-type="head_nav">
    <nav class="navbar navbar-expand-lg" style="background:#1565C0; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
        <div class="container">
            <!-- Logo -->
            <a class="navbar-brand" href="{$c.index_url}" style="padding:8px 0;">
                <if value="$c['met_logo']">
                    <img src="{$c.met_logo}" alt="{$c.met_webname}" height="48">
                <else/>
                    <span style="font-size:20px; font-weight:700; color:#fff;">{$c.met_webname}</span>
                </if>
            </a>

            <!-- 导航切换按钮 -->
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                    aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation"
                    style="border-color:rgba(255,255,255,0.3);">
                <span class="navbar-toggler-icon" style="background-image:url('data:image/svg+xml;charset=utf-8,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2224%22 height=%2224%22%3E%3Cline x1=%225%22 y1=%227%22 x2=%2219%22 y2=%227%22 stroke=%22%23fff%22 stroke-width=%222%22/%3E%3Cline x1=%225%22 y1=%2212%22 x2=%2219%22 y2=%2212%22 stroke=%22%23fff%22 stroke-width=%222%22/%3E%3Cline x1=%225%22 y1=%2217%22 x2=%2219%22 y2=%2217%22 stroke=%22%23fff%22 stroke-width=%222%22/%3E%3C/svg%3E');"></span>
            </button>

            <!-- 导航菜单 -->
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ml-auto" style="align-items:center;">
                    <!-- 首页 -->
                    <li class="nav-item">
                        <a href="{$c.index_url}" class="nav-link"
                           style="color:#E0E7FF; font-size:15px; padding:8px 12px; border-bottom:3px solid transparent;
                                   <if value="$data['classnow'] eq 10001">border-bottom:3px solid #FFB81C; color:#fff;<else/>transition:all 0.3s;</if>">
                            {$word.home}
                        </a>
                    </li>

                    <!-- 一级栏目 -->
                    <tag action='category' type='head' class='active'>
                    <if value="$m['sub']">
                    <!-- 带下级菜单 -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="{$m.url}"
                           style="color:#E0E7FF; font-size:15px; padding:8px 12px; border-bottom:3px solid transparent;
                                   <if value="$m['class']">border-bottom:3px solid #FFB81C; color:#fff;<else/>transition:all 0.3s;</if>"
                           role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            {$m._name}
                        </a>
                        <div class="dropdown-menu" style="background:#fff; border:none; box-shadow:0 8px 16px rgba(0,0,0,0.15); border-radius:4px; padding:6px 0;">
                            <tag action='category' cid="$m['id']" type='son' class='active'>
                            <if value="$m['sub']">
                            <!-- 三级菜单 -->
                            <div class="dropdown-submenu" style="position:relative;">
                                <a class="dropdown-item" href="{$m.url}"
                                   style="color:#333; font-size:14px; padding:10px 16px; display:flex; justify-content:space-between;
                                          <if value="$m['class']">background:#f0f7ff; border-left:3px solid #1565C0;<else/>background:transparent; border-left:3px solid transparent;</if>
                                          transition:all 0.2s;">
                                    {$m._name}
                                    <i class="fa fa-angle-right" style="margin-left:8px;"></i>
                                </a>
                                <div class="dropdown-menu" style="position:absolute; left:100%; top:-6px; background:#fff; border:none;
                                                                   box-shadow:0 4px 12px rgba(0,0,0,0.1); border-radius:4px; min-width:160px; padding:6px 0;">
                                    <tag action='category' cid="$m['id']" type='son' class='active'>
                                        <a class="dropdown-item" href="{$m.url}"
                                           style="color:#333; font-size:13px; padding:8px 16px;
                                                  <if value="$m['class']">background:#E8F4FD; color:#1565C0;<else/>background:transparent;</if>
                                                  transition:all 0.2s;">
                                            {$m._name}
                                        </a>
                                    </tag>
                                </div>
                            </div>
                            <else/>
                            <!-- 二级菜单 -->
                            <a class="dropdown-item" href="{$m.url}"
                               style="color:#333; font-size:14px; padding:10px 16px;
                                      <if value="$m['class']">background:#f0f7ff; border-left:3px solid #1565C0;<else/>background:transparent; border-left:3px solid transparent;</if>
                                      transition:all 0.2s;">
                                {$m._name}
                            </a>
                            </if>
                            </tag>
                        </div>
                    </li>
                    <else/>
                    <!-- 无下级菜单 -->
                    <li class="nav-item">
                        <a class="nav-link" href="{$m.url}"
                           style="color:#E0E7FF; font-size:15px; padding:8px 12px; border-bottom:3px solid transparent;
                                  <if value="$m['class']">border-bottom:3px solid #FFB81C; color:#fff;<else/>transition:all 0.3s;</if>">
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
