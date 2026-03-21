<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />
<main>
<div class="container" style="padding-top:40px; padding-bottom:60px;">
    <div class="news-layout">

        <!-- 文章主体 -->
        <div>
            <tag action='content' type='news'>
            <article class="article-wrap">
                <!-- 标题 -->
                <h1 class="article-title">{$v.title}</h1>

                <!-- 元信息 -->
                <div class="article-meta">
                    <span><i class="icon wb-folder"></i> <a href="{$v.column_url}">{$v.columnname}</a></span>
                    <span><i class="icon wb-time"></i> {$v.inputtime|date_format:'%Y-%m-%d'}</span>
                    <span><i class="icon wb-eye"></i> {$v.hits} 阅读</span>
                </div>

                <!-- 正文 -->
                <div class="article-body met-editor">
                    {$v.content}
                </div>

                <!-- 标签 -->
                <if value="$v['tag']">
                <div class="article-tags">
                    <i class="icon wb-tag"></i>
                    <tag action='tags' type='content'>
                    <a href="{$v.url}" class="article-tag">{$v.name}</a>
                    </tag>
                </div>
                </if>

                <!-- 上下篇 -->
                <div class="article-nav">
                    <if value="$v['pre_url']">
                    <a href="{$v.pre_url}" class="article-nav-item">
                        <span class="article-nav-label">上一篇</span>
                        <span class="article-nav-title">{$v.pre_title|met_substr:0,30}</span>
                    </a>
                    </if>
                    <if value="$v['next_url']">
                    <a href="{$v.next_url}" class="article-nav-item" style="text-align:right;">
                        <span class="article-nav-label">下一篇</span>
                        <span class="article-nav-title">{$v.next_title|met_substr:0,30}</span>
                    </a>
                    </if>
                </div>
            </article>
            </tag>

            <!-- 相关文章 -->
            <div class="related-articles">
                <h3 class="sidebar-card-title">相关文章</h3>
                <div class="content-list" style="grid-template-columns: repeat(auto-fill, minmax(220px,1fr));">
                    <tag action='list' cid='$data["classnow"]' num='4' type='news' orderby='rand'>
                    <div class="content-item" data-animate>
                        <a href="{$v.url}" title="{$v.title}" class="content-item-link">
                            <div class="content-item-image" style="height:140px;">
                                <if value="$v['imgurl']">
                                    <img src="{$v.imgurl|thumb:300,140}" alt="{$v.title}" loading="lazy">
                                <else/>
                                    <div class="content-item-placeholder"><i class="icon wb-book"></i></div>
                                </if>
                            </div>
                            <div class="content-item-body">
                                <h3 class="content-item-title" style="font-size:14px;">{$v.title}</h3>
                                <div class="content-item-meta">
                                    <span><i class="icon wb-time"></i> {$v.inputtime|date_format:'%m-%d'}</span>
                                </div>
                            </div>
                        </a>
                    </div>
                    </tag>
                </div>
            </div>
        </div>

        <!-- 侧边栏 -->
        <aside>
            <!-- 公众号推广 -->
            <div class="sidebar-card" style="background:linear-gradient(135deg,#1E88E5,#1565C0); color:#fff; text-align:center;">
                <div style="font-size:16px; font-weight:700; margin-bottom:8px;">关注公众号</div>
                <p style="font-size:13px; color:rgba(255,255,255,0.85); margin-bottom:16px;">每日KET/PET干货，免费备考资料</p>
                <if value="$lang['wechat_qrcode']">
                    <img src="{$lang.wechat_qrcode}" alt="英语陪跑GO" style="width:120px; height:120px; border-radius:8px; background:#fff; padding:4px;">
                <else/>
                    <div onclick="epgoEducation.showQRCode()" style="cursor:pointer; background:rgba(255,255,255,0.2); border-radius:8px; padding:20px; font-size:13px;">
                        点击查看二维码
                    </div>
                </if>
            </div>

            <!-- 热门文章 -->
            <div class="sidebar-card">
                <div class="sidebar-card-title">热门文章</div>
                <tag action='list' cid='$data["classnow"]' num='6' type='news' orderby='hits DESC'>
                <a href="{$v.url}" title="{$v.title}" class="sidebar-news-item">
                    <span class="sidebar-news-num">{$v._index}</span>
                    <span class="sidebar-news-title">{$v.title|met_substr:0,24}</span>
                </a>
                </tag>
            </div>

            <!-- AdSense 侧栏 -->
            <div class="sidebar-card" style="padding:8px;">
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-2043497135383313"
                     data-ad-slot="auto"
                     data-ad-format="rectangle"
                     data-full-width-responsive="true"></ins>
                <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
            </div>
        </aside>
    </div>
</div>
</main>

<style>
.article-wrap { background:#fff; border-radius:12px; padding:40px; box-shadow:0 2px 12px rgba(0,0,0,0.06); }
.article-title { font-size:26px; font-weight:700; color:#1A1A1A; line-height:1.4; margin-bottom:16px; }
.article-meta { display:flex; gap:20px; font-size:13px; color:#999; padding-bottom:20px; border-bottom:1px solid #eee; margin-bottom:30px; flex-wrap:wrap; }
.article-meta a { color:#999; text-decoration:none; }
.article-meta a:hover { color:var(--color-primary); }
.article-body { font-size:16px; line-height:1.85; color:#333; }
.article-body img { max-width:100%; border-radius:8px; }
.article-body h2 { font-size:20px; font-weight:700; color:#2c3e50; border-left:4px solid #3498db; padding-left:12px; margin:30px 0 16px; }
.article-tags { margin-top:30px; padding-top:20px; border-top:1px solid #eee; }
.article-tag { display:inline-block; padding:4px 12px; background:var(--color-primary-light); color:var(--color-primary); border-radius:20px; font-size:12px; margin:4px; text-decoration:none; }
.article-nav { display:flex; gap:16px; margin-top:30px; }
.article-nav-item { flex:1; padding:16px; background:#f7f8fa; border-radius:10px; text-decoration:none; display:flex; flex-direction:column; gap:6px; transition:.3s; }
.article-nav-item:hover { background:var(--color-primary-light); }
.article-nav-label { font-size:12px; color:#999; }
.article-nav-title { font-size:14px; color:#333; font-weight:500; }
.related-articles { margin-top:40px; }
.sidebar-news-item { display:flex; align-items:center; gap:10px; padding:10px 0; border-bottom:1px solid #f0f0f0; text-decoration:none; }
.sidebar-news-item:last-child { border-bottom:none; }
.sidebar-news-num { width:22px; height:22px; border-radius:50%; background:var(--color-primary); color:#fff; font-size:12px; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.sidebar-news-title { font-size:13px; color:#333; line-height:1.5; }
.sidebar-news-title:hover { color:var(--color-primary); }
.content-item-link { text-decoration:none; color:inherit; display:block; }
.content-item-placeholder { width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,#E3F2FD,#F3E5F5); font-size:40px; color:rgba(30,136,229,0.3); }
@media (max-width:768px) {
    .article-wrap { padding:20px; }
    .article-title { font-size:20px; }
    .article-nav { flex-direction:column; }
}
</style>
<include file="foot.php" />
