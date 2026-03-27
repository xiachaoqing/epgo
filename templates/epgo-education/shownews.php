<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<style>
/* 详情页专属样式 */
.epgo-article-header { margin-bottom:28px; padding-bottom:20px; border-bottom:1px solid #e5e7eb; }
.epgo-article-title { font-size:28px; font-weight:700; color:#111827; margin:0 0 16px; line-height:1.4; }
.epgo-article-meta { display:flex; align-items:center; gap:16px; flex-wrap:wrap; color:#6b7280; font-size:14px; }
.epgo-article-meta span { display:flex; align-items:center; gap:5px; }

/* 文章内容排版 */
.met-editor { line-height:1.9; font-size:16px; color:#374151; }
.met-editor h2 { font-size:22px; font-weight:700; color:#111827; margin:28px 0 14px; border-left:4px solid #2563eb; padding-left:12px; }
.met-editor h3 { font-size:18px; font-weight:600; color:#1e40af; margin:22px 0 10px; }
.met-editor p  { margin:14px 0; }
.met-editor img { max-width:100%; border-radius:8px; margin:16px 0; box-shadow:0 2px 8px rgba(0,0,0,.1); }
.met-editor ul, .met-editor ol { margin:12px 0; padding-left:28px; }
.met-editor li { margin:6px 0; }
.met-editor blockquote { border-left:4px solid #2563eb; margin:20px 0; padding:12px 20px; background:#eff6ff; border-radius:0 6px 6px 0; color:#374151; font-style:italic; }
.met-editor strong { color:#111827; }
.met-editor a { color:#2563eb; text-decoration:underline; }
.met-editor a:hover { color:#1d4ed8; }

/* 分享按钮 */
.epgo-share-bar { display:flex; gap:10px; margin-top:14px; flex-wrap:wrap; }
.epgo-share-bar button { border:1px solid #e5e7eb; background:#fff; color:#374151; border-radius:6px; padding:7px 16px; font-size:13px; cursor:pointer; transition:all .2s; }
.epgo-share-bar button:hover { border-color:#2563eb; color:#2563eb; background:#eff6ff; }

/* 相关推荐 */
.epgo-related { margin:36px 0 0; padding:24px 0 0; border-top:2px solid #e5e7eb; }
.epgo-related h3 { font-size:18px; font-weight:700; color:#111827; margin:0 0 18px; }
.epgo-related-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:16px; }
.epgo-related-card { border:1px solid #e5e7eb; border-radius:8px; overflow:hidden; transition:all .3s; }
.epgo-related-card:hover { border-color:#2563eb; box-shadow:0 4px 12px rgba(37,99,235,.12); transform:translateY(-2px); }
.epgo-related-card img { width:100%; height:110px; object-fit:cover; display:block; }
.epgo-related-card .rc-body { padding:10px 12px; }
.epgo-related-card a { color:#111827; font-size:13px; font-weight:600; text-decoration:none; line-height:1.4;
    display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.epgo-related-card a:hover { color:#2563eb; }

/* 标签 */
.epgo-tags-bar { margin:24px 0; }
.epgo-tags-bar a { display:inline-block; background:#eff6ff; color:#2563eb; padding:5px 12px; border-radius:4px; margin:4px 4px 4px 0; font-size:13px; text-decoration:none; transition:all .2s; }
.epgo-tags-bar a:hover { background:#2563eb; color:#fff; }

/* 侧栏 */
.epgo-sidebar-box { background:#fff; border:1px solid #e5e7eb; border-radius:8px; padding:18px; margin-bottom:20px; }
.epgo-sidebar-box h4 { font-size:15px; font-weight:700; color:#111827; margin:0 0 14px; padding-bottom:10px; border-bottom:2px solid #2563eb; }
.epgo-sidebar-box ul { list-style:none; padding:0; margin:0; }
.epgo-sidebar-box ul li { border-bottom:1px solid #f3f4f6; }
.epgo-sidebar-box ul li:last-child { border-bottom:none; }
.epgo-sidebar-box ul li a { display:block; padding:9px 4px; color:#374151; font-size:14px; text-decoration:none; transition:color .2s; line-height:1.5;
    display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.epgo-sidebar-box ul li a:hover { color:#2563eb; }
.epgo-sidebar-box ul li .li-date { font-size:12px; color:#9ca3af; margin-top:3px; }

/* 面包屑 */
.epgo-breadcrumb { font-size:13px; color:#9ca3af; margin-bottom:18px; }
.epgo-breadcrumb a { color:#6b7280; text-decoration:none; }
.epgo-breadcrumb a:hover { color:#2563eb; }

@media(max-width:768px){
  .epgo-article-title { font-size:22px; }
  .epgo-article-meta { font-size:12px; gap:10px; }
  .met-editor { font-size:15px; }
  .epgo-related-grid { grid-template-columns:1fr 1fr; }
}
@media(max-width:480px){
  .epgo-article-title { font-size:20px; }
  .epgo-related-grid { grid-template-columns:1fr; }
  .epgo-share-bar { flex-direction:column; }
  .epgo-share-bar button { width:100%; }
}
</style>

<main class="met-shownews animsition">
    <div class="container">
        <div class="row">
            <div class="clearfix">

                <!-- 主内容区 — m-id="noset" 是MetInfo识别文章区域的关键 -->
                <div class="col-md-9 met-shownews-body" m-id="noset">
                    <div class="row">

                        <!-- 面包屑 -->
                        <div class="epgo-breadcrumb">
                            <a href="{$c.index_url}">首页</a>
                            <span style="margin:0 6px;">›</span>
                            <a href="{$data.classurl}">{$data.issue}</a>
                            <span style="margin:0 6px;">›</span>
                            <span style="color:#374151;">{$data.title}</span>
                        </div>

                        <!-- 标题区 -->
                        <section class="details-title border-bottom1 epgo-article-header">
                            <h1 class="epgo-article-title m-0">{$data.title}</h1>
                            <div class="epgo-article-meta info font-weight-300">
                                <span><i class="icon wb-calendar m-r-5" aria-hidden="true"></i>{$data.updatetime}</span>
                                <if value="1">
                                    <span><i class="icon wb-folder m-r-5" aria-hidden="true"></i>{$data.issue}</span>
                                </if>
                                <if value="1">
                                    <span><i class="icon wb-eye m-r-5" aria-hidden="true"></i>{$data.hits} 次阅读</span>
                                </if>
                            </div>
                            <!-- 分享按钮 -->
                            <div class="epgo-share-bar">
                                <button onclick="epgoShareWeChat()"><i class="icon wb-share m-r-5"></i>微信分享</button>
                                <button onclick="epgoShareQQ()"><i class="icon wb-share m-r-5"></i>QQ分享</button>
                                <button onclick="epgoCopyLink()"><i class="icon wb-link m-r-5"></i>复制链接</button>
                            </div>
                        </section>

                        <!-- 文章正文 -->
                        <section class="met-editor clearfix">
                            {$data.content}
                        </section>

                        <!-- 标签 -->
                        <if value="1">
                            <list data="$data['taglist']" name="$tag" num="4"></list>
                            <if value="$sub">
                                <div class="epgo-tags-bar">
                                    <strong style="color:#374151;font-size:14px;margin-right:6px;">标签：</strong>
                                    <list data="$data['taglist']" name="$tag" num="5">
                                        <a href="{$tag.url}" title="{$tag.name}">{$tag.name}</a>
                                    </list>
                                </div>
                            </if>
                        </if>

                        <!-- 分页 - 下一篇/上一篇 -->
                        <div class="epgo-pagination" style="display:flex; justify-content:space-between; align-items:center; padding:24px 0; border-top:1px solid #e5e7eb; border-bottom:1px solid #e5e7eb; margin:30px 0;">
                            <div style="flex:1;">
                                <tag action="list" type="news" cid="$data['class1']" num="1" orderby="id" orderby_type="asc" pagenum="1" pagesize="1" curdate="{$data['id']}">
                                    <if value="$v['id'] lt $data['id']">
                                        <a href="{$v.url}" title="上一篇: {$v.title}" style="display:inline-block; padding:10px 16px; background:#eff6ff; color:#2563eb; border-radius:6px; text-decoration:none; font-weight:500; transition:all 0.3s;">
                                            <i class="icon wb-chevron-left" style="margin-right:6px;"></i>上一篇
                                        </a>
                                    </if>
                                </tag>
                            </div>
                            <div style="text-align:center; flex:0 0 auto; color:#9ca3af; font-size:14px;">
                                文章 {$data['id']}
                            </div>
                            <div style="flex:1; text-align:right;">
                                <tag action="list" type="news" cid="$data['class1']" num="1" orderby="id" orderby_type="desc" pagenum="1" pagesize="1" curdate="{$data['id']}">
                                    <if value="$v['id'] gt $data['id']">
                                        <a href="{$v.url}" title="下一篇: {$v.title}" style="display:inline-block; padding:10px 16px; background:#eff6ff; color:#2563eb; border-radius:6px; text-decoration:none; font-weight:500; transition:all 0.3s;">
                                            下一篇<i class="icon wb-chevron-right" style="margin-left:6px;"></i>
                                        </a>
                                    </if>
                                </tag>
                            </div>
                        </div>

                        <!-- 相关推荐 -->
                        <div class="epgo-related" style="margin:40px 0 0; padding:30px 0 0; border-top:2px solid #e5e7eb;">
                            <h3 style="font-size:18px; font-weight:700; color:#111827; margin:0 0 24px; padding-bottom:12px; border-bottom:2px solid #2563eb;">🔗 相关推荐文章</h3>
                            <div class="epgo-related-grid" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:20px;">
                                <tag action='list' type="news" cid="$data['class1']" num="6">
                                    <div class="epgo-related-card" style="border:1px solid #e5e7eb; border-radius:8px; overflow:hidden; transition:all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); cursor:pointer;" onmouseover="this.style.transform='translateY(-6px)'; this.style.boxShadow='0 12px 24px rgba(37,99,235,0.12); this.style.borderColor='#2563eb'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.08)'; this.style.borderColor='#e5e7eb'">
                                        <if value="$v['imgurl']">
                                            <a href="{$v.url}" title="{$v.title}" {$g.urlnew} style="display:block; overflow:hidden; height:120px; background:#f3f4f6;">
                                                <img src="{$v.imgurl|thumb:280,120}" alt="{$v.title}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.4s ease; display:block;">
                                            </a>
                                        <else/>
                                            <div style="height:120px; background:linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%); display:flex; align-items:center; justify-content:center;">
                                                <span style="color:#9ca3af; font-size:13px;">📝 暂无封面</span>
                                            </div>
                                        </if>
                                        <div class="rc-body" style="padding:12px;">
                                            <a href="{$v.url}" title="{$v.title}" {$g.urlnew} style="color:#111827; font-size:13px; font-weight:600; text-decoration:none; line-height:1.5; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; transition:color 0.3s;" onmouseover="this.style.color='#2563eb'" onmouseout="this.style.color='#111827'">{$v.title}</a>
                                            <div style="font-size:11px; color:#9ca3af; margin-top:8px; padding-top:8px; border-top:1px solid #f3f4f6;">
                                                <span style="margin-right:8px;">📅 {$v.updatetime}</span>
                                                <span>👁️ {$v.hits}</span>
                                            </div>
                                        </div>
                                    </div>
                                </tag>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- 右侧边栏 -->
                <div class="col-md-3">
                    <div class="row">

                        <!-- 搜索 -->
                        <div class="epgo-sidebar-box">
                            <tag action="search.column"></tag>
                        </div>

                        <!-- 栏目导航 -->
                        <aside class="met-sidebar panel panel-body m-b-0 epgo-sidebar-box" boxmh-h m-id="news_bar" m-type="nocontent">
                            <h4>栏目导航</h4>
                            <if value="$lang['bar_column_open']">
                                <ul class="sidebar-column">
                                    <tag action='category' cid="$data['releclass1']">
                                    <li>
                                        <a href="{$m.url}" title="{$m.name}" class="<if value='$data["classnow"] eq $m["id"]'>active</if>" {$m.urlnew}>{$m.name}</a>
                                    </li>
                                    <tag action='category' cid="$m['id']" type='son' class='active'>
                                    <li style="padding-left:8px;">
                                        <if value="$m['sub'] && $lang['bar_column3_open']">
                                            <a href="javascript:;" title="{$m.name}" class="{$m.class}" data-toggle="collapse" data-target=".sidebar-column3-{$m._index}">{$m.name} <i class="wb-chevron-right-mini"></i></a>
                                            <div class="sidebar-column3-{$m._index} collapse">
                                                <ul style="padding-left:12px;">
                                                    <li><a href="{$m.url}" {$m.urlnew} title="{$lang.all}" class="{$m.class}">{$lang.all}</a></li>
                                                    <tag action='category' cid="$m['id']" type='son' class='active'>
                                                    <li><a href="{$m.url}" {$m.urlnew} title="{$m.name}" class="{$m.class}">{$m.name}</a></li>
                                                    </tag>
                                                </ul>
                                            </div>
                                        <else/>
                                            <a href="{$m.url}" title="{$m.name}" class="{$m.class}" {$m.urlnew}>{$m.name}</a>
                                        </if>
                                    </li>
                                    </tag>
                                    </tag>
                                </ul>
                            </if>

                            <!-- 推荐列表 -->
                            <if value="$lang['news_bar_list_open']">
                                <div class="sidebar-news-list recommend" style="margin-top:18px;">
                                    <h4 style="border-top:1px solid #e5e7eb; padding-top:14px;">{$lang.news_bar_list_title}</h4>
                                    <ul>
                                        <?php $id=$lang['sidebar_newslist_idid']?$lang['sidebar_newslist_idid']:$data['class1']; ?>
                                        <tag action='list' type="$lang['news_bar_list_type']" cid="$id" num="$lang['sidebar_newslist_num']">
                                            <li>
                                                <a href="{$v.url}" title="{$v.title}" {$g.urlnew}>{$v.title}</a>
                                                <div class="li-date">{$v.updatetime}</div>
                                            </li>
                                        </tag>
                                    </ul>
                                </div>
                            </if>
                        </aside>

                    </div>
                </div>

            </div>
        </div>
    </div>
</main>

<script>
(function(){
    var url   = window.location.href;
    var title = (document.querySelector('.epgo-article-title')||{}).innerText || '英语陪跑GO';
    var desc  = '专业的KET/PET英语备考平台';
    var img   = (document.querySelector('.met-editor img')||{}).src || '';

    window.epgoShareWeChat = function(){
        var text = '微信中打开此页面后，点右上角「…」→「分享到朋友圈」\n\n' + url;
        alert(text);
    };
    window.epgoShareQQ = function(){
        var u = 'https://connect.qq.com/widget/shareqq/index.html?url='+encodeURIComponent(url)+'&title='+encodeURIComponent(title)+'&desc='+encodeURIComponent(desc)+'&pics='+encodeURIComponent(img);
        window.open(u,'_blank','width=560,height=480');
    };
    window.epgoCopyLink = function(){
        if(navigator.clipboard){
            navigator.clipboard.writeText(url).then(function(){ alert('链接已复制！'); });
        } else {
            var t = document.createElement('textarea');
            t.value = url; document.body.appendChild(t); t.select();
            document.execCommand('copy'); document.body.removeChild(t);
            alert('链接已复制！');
        }
    };
})();
</script>

<include file="foot.php" />
