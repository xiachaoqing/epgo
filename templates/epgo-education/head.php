<met_meta page="$met_page" />

<!-- 微信分享SDK和样式优化 -->
<script src="https://res.wx.qq.com/open/js/jweixin-1.6.0.js"></script>
<style>
/* 快速响应式修复 */
html { font-size: 16px; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; }

/* Logo修复 - 彻底去掉四个角的黑点/边框 */
.met-logo,
.met-logo .vertical-align,
.met-logo .vertical-align-middle {
  outline: none !important;
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  text-decoration: none !important;
}
.met-logo img {
  max-height: 48px;
  width: auto;
  outline: none !important;
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  display: block;
}
/* MetInfo框架有时给 .vertical-align 加outline */
.vertical-align:focus,
.met-logo:focus { outline: none !important; }
/* 去掉图片自带的尖角控制点（浏览器selection handle） */
img::selection { background: transparent; }

/* 导航栏优化 */
.met-nav {
  background: linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%);
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 10px 0 !important;
}

/* 导航链接样式 */
.nav-link {
  color: white !important;
  font-weight: 500;
  padding: 8px 16px !important;
  margin: 0 2px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: rgba(255,255,255,0.2);
  color: white !important;
}

.nav-link.active {
  background: rgba(255,255,255,0.3);
  color: white !important;
}

/* 下拉菜单现代化 */
.dropdown-menu {
  background: white;
  border: none;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  padding: 8px 0 !important;
  min-width: 200px;
  animation: dropdownSlideDown 0.2s ease;
}

@keyframes dropdownSlideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-menu li {
  padding: 0 !important;
}

.dropdown-menu a {
  color: #374151 !important;
  padding: 10px 20px !important;
  transition: all 0.2s ease;
  font-weight: 500;
  display: block;
}

.dropdown-menu a:hover {
  background: #eff6ff;
  color: #1e40af !important;
  padding-left: 24px !important;
}

/* 移动端响应式处理 */
@media (max-width: 768px) {
  html { font-size: 14px; }
  .navbar { padding: 10px 0; }
  .met-nav-btn .navbar-header { width: 80%; }
  .container { padding: 0 15px; }

  .nav-link {
    padding: 6px 12px !important;
  }
}

/* 内容安全策略 */
img { max-width: 100%; height: auto; }
</style>
<header class='met-head' m-id='met_head' m-type="head_nav">
    <nav class="navbar navbar-default met-nav">
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
                        <a href="{$c.index_url}" class="met-logo vertical-align block pull-xs-left" title="{$c.met_logo_keyword}">
                            <div class="vertical-align-middle">
                                <if value="$c['met_mobile_logo']">
                                    <img src="{$c.met_mobile_logo}" alt="{$c.met_logo_keyword}" class="mblogo" />
                                    <img src="{$c.met_logo}" alt="{$c.met_logo_keyword}" class="pclogo" />
                                    <else/>
                                    <img src="{$c.met_logo}" alt="{$c.met_logo_keyword}" class="mblogo" />
                                    <img src="{$c.met_logo}" alt="{$c.met_logo_keyword}" class="pclogo" />
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
                            <a href="{$c.index_url}" title="网站首页" class="nav-link <if value="$data['classnow'] eq 10001">
                            active
                            </if>">网站首页</a>
                        </li>

                        <!-- KET备考 -->
                        <li class="nav-item dropdown">
                            <a href="{$c.index_url}ket/" title="KET备考" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">KET备考</a>
                            <ul class="dropdown-menu">
                                <li><a href="{$c.index_url}ket-exam/" title="KET真题解析">KET真题解析</a></li>
                                <li><a href="{$c.index_url}ket-word/" title="KET词汇速记">KET词汇速记</a></li>
                                <li><a href="{$c.index_url}ket-write/" title="KET写作指导">KET写作指导</a></li>
                                <li><a href="{$c.index_url}ket-listen/" title="KET听力技巧">KET听力技巧</a></li>
                            </ul>
                        </li>

                        <!-- PET备考 -->
                        <li class="nav-item dropdown">
                            <a href="{$c.index_url}pet/" title="PET备考" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">PET备考</a>
                            <ul class="dropdown-menu">
                                <li><a href="{$c.index_url}pet-exam/" title="PET真题解析">PET真题解析</a></li>
                                <li><a href="{$c.index_url}pet-word/" title="PET词汇速记">PET词汇速记</a></li>
                                <li><a href="{$c.index_url}pet-write/" title="PET写作指导">PET写作指导</a></li>
                                <li><a href="{$c.index_url}pet-read/" title="PET阅读技巧">PET阅读技巧</a></li>
                            </ul>
                        </li>

                        <!-- 其他栏目 -->
                        <li class="nav-item">
                            <a href="{$c.index_url}reading/" title="英语阅读" class="nav-link">英语阅读</a>
                        </li>
                        <li class="nav-item">
                            <a href="{$c.index_url}speech/" title="英语演讲" class="nav-link">英语演讲</a>
                        </li>
                        <li class="nav-item">
                            <a href="{$c.index_url}daily/" title="每日英语" class="nav-link">每日英语</a>
                        </li>
                        <li class="nav-item">
                            <a href="{$c.index_url}download/" title="资料下载" class="nav-link">资料下载</a>
                        </li>
                        <li class="nav-item">
                            <a href="{$c.index_url}about/" title="关于我们" class="nav-link">关于我们</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</header>
