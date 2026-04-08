<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<!-- 子栏目页面 Header - 升级版 -->
<section class="epgo-category-header" style="background:linear-gradient(135deg, #1E3A8A 0%, #2563EB 55%, #3B82F6 100%); color:white; padding:80px 0 60px; margin-bottom:50px; position:relative; overflow:hidden;">
    <div style="position:absolute; width:400px; height:400px; border-radius:50%; background:rgba(255,255,255,0.08); top:-100px; right:-100px; pointer-events:none; animation:float 20s infinite ease-in-out;"></div>
    <div style="position:absolute; width:200px; height:200px; border-radius:50%; background:rgba(255,255,255,0.05); bottom:-50px; left:-50px; pointer-events:none; animation:float-reverse 15s infinite ease-in-out;"></div>
    <div class="container" style="position:relative; z-index:1;">
        <div style="margin-bottom:20px; font-size:14px; color:rgba(255,255,255,0.9);">
            <a href="{$c.index_url}" style="color:rgba(255,255,255,0.9); text-decoration:none; transition:color 0.2s;">首页</a> <span style="margin:0 8px;">›</span> <span>{$data['name']}</span>
        </div>
        <h1 style="font-size:48px; font-weight:800; margin:0 0 20px 0; color:white; line-height:1.1; text-shadow:0 2px 8px rgba(0,0,0,0.2);">{$data['name']}</h1>
        <if value="$data['description']">
            <p style="font-size:17px; margin:0 0 0 0; color:rgba(255,255,255,0.9); line-height:1.6; max-width:600px;">{$data['description']}</p>
        </if>
    </div>
    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        @keyframes float-reverse {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(20px); }
        }
    </style>
</section>

<include file="para_search.php" />
<section class="epgo-section" style="padding:40px 0;">
    <div class="container">
        <div class="row">
            <!-- 左侧文章列表 -->
            <div class="col-md-9 met-news-body">
                <div class="met-news-list met-news" m-id="noset">
                    <?php
                    // 修复子栏目列表查询 - 优先使用 class2
                    $_fix_cid = intval($data['classnow'] ?? 0);
                    $_fix_page = intval($_REQUEST['page'] ?? 1);
                    $_fix_pagesize = intval($c['met_news_list'] ?? 10);

                    // 如果 classnow 是二级栏目（111-114, 121-124等），用 class2=classnow 查询
                    if ($_fix_cid >= 111 && $_fix_cid <= 124) {
                        $_mysqli = new mysqli('127.0.0.1', 'xiachaoqing', '***REMOVED***', 'epgo_db');
                        if (!$_mysqli->connect_error) {
                            $_mysqli->set_charset('utf8mb4');
                            $_offset = ($_fix_page - 1) * $_fix_pagesize;

                            // 查询总数
                            $_cnt_res = $_mysqli->query("SELECT COUNT(*) FROM ep_news WHERE recycle=0 AND class2=$_fix_cid");
                            $result_count = $_cnt_res->fetch_row()[0];

                            // 查询数据
                            $_sql = "SELECT id, title, filename, imgurl, description, updatetime, hits, issue, class1, class2
                                    FROM ep_news
                                    WHERE recycle=0 AND class2=$_fix_cid
                                    ORDER BY id DESC
                                    LIMIT $_offset, $_fix_pagesize";
                            $_res = $_mysqli->query($_sql);
                            $result = $_res ? $_res->fetch_all(MYSQLI_ASSOC) : [];
                            $_mysqli->close();

                            // 处理 URL 和其他字段
                            foreach ($result as &$_item) {
                                $_item['url'] = '/' . trim($_item['filename'] ?? '') . '.html';
                                $_item['_title'] = htmlspecialchars($_item['title']);
                                $_item['_index'] = 0; // placeholder
                            }
                            $sub = !empty($result); // 用于判断是否有数据
                        }
                    }
                    ?>
                    <tag action='news.list' num="$c['met_news_list']" cid="$data['classnow']"></tag>
                    <if value="$sub">
                        <div class="ulstyle met-pager-ajax imagesize" data-scale='{$c.met_newsimg_y}x{$c.met_newsimg_x}'>
                            <include file='ajax/news'/>
                        </div>
                    <else/>
                        <div class='text-xs-center font-size-20 p-y-40' style="color:var(--color-muted);">{$c.met_data_null}</div>
                    </if>
                    <div class='m-t-20 text-xs-center hidden-sm-down' m-type="nosysdata">
                        <pager/>
                    </div>
                    <div class="met_pager met-pager-ajax-link hidden-md-up" m-type="nosysdata">
                        <button type="button" class="btn btn-primary btn-block btn-squared ladda-button"
                            id="met-pager-btn" data-plugin="ladda" data-style="slide-left" data-url="" data-page="1">
                            <i class="icon wb-chevron-down m-r-5"></i> 加载更多
                        </button>
                    </div>
                </div>
            </div>

            <!-- 右侧边栏 -->
            <div class="col-md-3">
                <aside class="met-sidebar panel panel-body m-b-0" boxmh-h m-id='news_bar' m-type='nocontent' style="border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.08); border:1px solid #e5e7eb;">
                    <div class="sidebar-search" data-placeholder="search" style="margin-bottom:16px;">
                        <tag action="search.column"></tag>
                    </div>
                    <if value="$lang['bar_column_open']">
                        <div style="padding-bottom:16px; border-bottom:1px solid #e5e7eb; margin-bottom:16px;">
                            <h4 style="font-size:14px; font-weight:700; color:#111827; margin:0 0 12px 0; padding-bottom:8px; border-bottom:2px solid #2563eb;">📂 栏目导航</h4>
                            <ul class="sidebar-column list-icons" style="list-style:none;padding:0;margin:0;">
                                <tag action='category' cid="$data['releclass1']">
                                <li style="margin-bottom:8px;">
                                    <a href="{$m.url}" title="{$m.name}" class="<if value='$data["classnow"] eq $m["id"]'>active</if>" {$m.urlnew} style="color:#6b7280; text-decoration:none; transition:all 0.3s; display:inline-block; padding-bottom:2px; border-bottom:2px solid transparent;" onmouseover="this.style.color='#2563eb'; this.style.borderColor='#2563eb'" onmouseout="this.style.color='#6b7280'; this.style.borderColor='transparent'">{$m.name}</a>
                                </li>
                                <tag action='category' cid="$m['id']" type='son' class='active'>
                                <li style="padding-left:16px; margin-bottom:6px;">
                                    <a href="{$m.url}" title="{$m.name}" class='{$m.class}' {$m.urlnew} style="color:#9ca3af; font-size:14px; text-decoration:none; transition:color 0.3s;" onmouseover="this.style.color='#2563eb'" onmouseout="this.style.color='#9ca3af'">└ {$m.name}</a>
                                </li>
                                </tag>
                                </tag>
                            </ul>
                        </div>
                    </if>
                    <if value="$lang['news_bar_list_open']">
                        <div class="sidebar-news-list recommend">
                            <h4 style="font-size:14px; font-weight:700; color:#111827; margin:0 0 12px 0; padding-bottom:8px; border-bottom:2px solid #2563eb;">⭐ {$lang.news_bar_list_title}</h4>
                            <ul class="list-group list-group-bordered m-b-0" style="list-style:none;padding:0;margin:0;">
                                <?php $id=$lang['sidebar_newslist_idid']?$lang['sidebar_newslist_idid']:$data['class1']; ?>
                                <tag action='list' type="$lang['news_bar_list_type']" cid="$id" num="$lang['sidebar_newslist_num']">
                                    <li class="list-group-item" style="border:none; border-bottom:1px solid #f3f4f6; padding:8px 0; margin:0;">
                                        <a href="{$v.url}" title="{$v.title}" {$g.urlnew} style="color:#374151; text-decoration:none; font-size:13px; line-height:1.5; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; transition:color 0.3s;" onmouseover="this.style.color='#2563eb'" onmouseout="this.style.color='#374151'">{$v.title}</a>
                                    </li>
                                </tag>
                            </ul>
                        </div>
                    </if>
                </aside>
            </div>
        </div>
    </div>
</section>
<include file="foot.php" />
