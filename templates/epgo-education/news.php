<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<main>
    <!-- 页面标题区 -->
    <section style="background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); color: white; padding: 60px 20px; text-align: center;">
        <div class="container">
            <h1 style="color: white; margin-bottom: 10px;">{$data.classname}</h1>
            <nav aria-label="breadcrumb" style="text-align: center;">
                <ol class="breadcrumb" style="background: transparent; justify-content: center; margin-bottom: 0;">
                    <li class="breadcrumb-item"><a href="{$c.index_url}" style="color: rgba(255,255,255,0.8);">首页</a></li>
                    <li class="breadcrumb-item active" style="color: white;">{$data.classname}</li>
                </ol>
            </nav>
        </div>
    </section>

    <!-- 内容区 -->
    <section style="padding: 60px 20px;">
        <div class="container">
            <div style="display: grid; grid-template-columns: 1fr 320px; gap: 40px;">
                <!-- 左侧：文章列表 -->
                <div>
                    <div class="content-list" style="grid-template-columns: 1fr;">
                        <tag action='list' cid="$data['classid']" num='20' type='news' orderby='inputtime DESC'>
                        <div class="card" style="display: grid; grid-template-columns: 200px 1fr; gap: 20px; overflow: hidden;">
                            <!-- 文章图片 -->
                            <div style="overflow: hidden; border-radius: 8px;">
                                <if value="$v['imgurl']">
                                    <img src="{$v.imgurl|thumb:200,150}" alt="{$v.title}" style="width: 100%; height: 150px; object-fit: cover; transition: transform 0.3s ease;">
                                <else/>
                                    <div style="width: 100%; height: 150px; background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%); display: flex; align-items: center; justify-content: center;">
                                        <i class="icon wb-book" style="font-size: 48px; color: rgba(30, 136, 229, 0.3);"></i>
                                    </div>
                                </if>
                            </div>

                            <!-- 文章信息 -->
                            <div class="card-body" style="padding: 0;">
                                <div class="badge badge-primary mb-3" style="background-color: #1E88E5;">{$v.columnname}</div>
                                <h3 style="margin-bottom: 10px; font-size: 18px;">
                                    <a href="{$v.url}" title="{$v.title}" style="color: #1E1E1E; text-decoration: none;">
                                        {$v.title}
                                    </a>
                                </h3>
                                <div style="font-size: 13px; color: #999; margin-bottom: 12px;">
                                    <span><i class="icon wb-time"></i> {$v.inputtime|date_format:'%Y-%m-%d'}</span>
                                    <span style="margin-left: 15px;"><i class="icon wb-eye"></i> {$v.hits}</span>
                                </div>
                                <if value="$v['description']">
                                    <p style="color: #666; line-height: 1.6; margin-bottom: 12px; font-size: 14px;">
                                        {$v.description|htmlspecialchars|truncate:150}
                                    </p>
                                </if>
                                <a href="{$v.url}" class="btn btn-sm btn-primary" style="display: inline-block;">继续阅读</a>
                            </div>
                        </div>
                        </tag>
                    </div>

                    <!-- 分页 -->
                    <div style="margin-top: 40px; text-align: center;">
                        {$data.pagebar}
                    </div>
                </div>

                <!-- 右侧：侧边栏 -->
                <aside>
                    <!-- 搜索框 -->
                    <div class="card" style="margin-bottom: 30px;">
                        <div class="card-body">
                            <h5>搜索</h5>
                            <form action="{$url.search}" method="get" style="margin-top: 15px;">
                                <div class="input-group">
                                    <input type="text" name="searchword" class="form-control" placeholder="搜索文章..." required>
                                    <div class="input-group-append">
                                        <button class="btn btn-primary" type="submit">
                                            <i class="icon wb-search"></i>
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>

                    <!-- 热门文章 -->
                    <div class="card" style="margin-bottom: 30px;">
                        <div class="card-body">
                            <h5 style="margin-bottom: 20px;">热门文章</h5>
                            <ul style="list-style: none; padding: 0; margin: 0;">
                                <tag action='list' cid="$data['classid']" num='5' type='news' orderby='hits DESC'>
                                <li style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #EEEEEE;">
                                    <a href="{$v.url}" title="{$v.title}" style="color: #1E88E5; text-decoration: none; font-size: 14px; line-height: 1.6;">
                                        {$v.title|truncate:30}
                                    </a>
                                    <div style="font-size: 12px; color: #999; margin-top: 5px;">
                                        <i class="icon wb-eye"></i> {$v.hits}
                                    </div>
                                </li>
                                </tag>
                            </ul>
                        </div>
                    </div>

                    <!-- 分类标签 -->
                    <div class="card" style="margin-bottom: 30px;">
                        <div class="card-body">
                            <h5 style="margin-bottom: 20px;">分类</h5>
                            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                                <tag action='category' cid="$data['classid']" type='son'>
                                <a href="{$m.url}" class="badge badge-light" style="padding: 8px 12px; background-color: #E3F2FD; color: #1E88E5; text-decoration: none; border-radius: 20px; font-size: 13px;">
                                    {$m._name}
                                </a>
                                </tag>
                            </div>
                        </div>
                    </div>

                    <!-- Google AdSense广告 -->
                    <div class="card">
                        <div class="card-body">
                            <ins class="adsbygoogle"
                                 style="display:block"
                                 data-ad-client="ca-pub-2043497135383313"
                                 data-ad-slot="2043497135383313"
                                 data-ad-format="rectangle"
                                 data-full-width-responsive="true"></ins>
                            <script>
                                (adsbygoogle = window.adsbygoogle || []).push({});
                            </script>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    </section>
</main>

<include file="foot.php" />
