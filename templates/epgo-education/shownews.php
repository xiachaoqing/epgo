<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<main>
    <!-- 文章标题区 -->
    <section style="background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); color: white; padding: 50px 20px;">
        <div class="container">
            <nav aria-label="breadcrumb" style="margin-bottom: 20px;">
                <ol class="breadcrumb" style="background: transparent;">
                    <li class="breadcrumb-item"><a href="{$c.index_url}" style="color: rgba(255,255,255,0.8);">首页</a></li>
                    <li class="breadcrumb-item"><a href="{$data.classurl}" style="color: rgba(255,255,255,0.8);">{$data.classname}</a></li>
                    <li class="breadcrumb-item active" style="color: white;">{$data.title|truncate:50}</li>
                </ol>
            </nav>
            <h1 style="color: white; margin: 0;">{$data.title}</h1>
        </div>
    </section>

    <!-- 文章内容区 -->
    <section style="padding: 60px 20px;">
        <div class="container">
            <div style="display: grid; grid-template-columns: 1fr 320px; gap: 40px;">
                <!-- 左侧：文章内容 -->
                <article>
                    <!-- 文章元信息 -->
                    <div style="padding: 20px; background-color: #F5F5F5; border-radius: 8px; margin-bottom: 40px; display: flex; gap: 30px; flex-wrap: wrap;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 12px; color: #666;">分类:</span>
                            <span class="badge badge-primary" style="background-color: #1E88E5;">
                                <a href="{$data.classurl}" style="color: white; text-decoration: none;">
                                    {$data.classname}
                                </a>
                            </span>
                        </div>
                        <div style="font-size: 13px; color: #999;">
                            <i class="icon wb-time"></i> {$data.inputtime|date_format:'%Y-%m-%d %H:%M'}
                        </div>
                        <div style="font-size: 13px; color: #999;">
                            <i class="icon wb-eye"></i> 浏览: {$data.hits}
                        </div>
                    </div>

                    <!-- 文章图片 -->
                    <if value="$data['imgurl']">
                    <div style="margin-bottom: 40px; border-radius: 8px; overflow: hidden;">
                        <img src="{$data.imgurl}" alt="{$data.title}" style="width: 100%; height: auto; display: block;">
                    </div>
                    </if>

                    <!-- 文章正文 -->
                    <div class="met-editor" style="font-size: 16px; line-height: 1.8; color: #424242; margin-bottom: 40px;">
                        {$data.content}
                    </div>

                    <!-- 文章标签 -->
                    <if value="$data['tags']">
                    <div style="padding-top: 20px; border-top: 1px solid #EEEEEE; margin-bottom: 40px;">
                        <strong style="display: block; margin-bottom: 15px;">标签:</strong>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                            <tag action='tags' id="$data['id']" type='news'>
                            <a href="{$m.url}" class="badge badge-light" style="padding: 8px 12px; background-color: #E3F2FD; color: #1E88E5; text-decoration: none; border-radius: 20px; font-size: 13px;">
                                {$m.name}
                            </a>
                            </tag>
                        </div>
                    </div>
                    </if>

                    <!-- 点赞和分享 -->
                    <div style="padding: 20px; background-color: #F5F5F5; border-radius: 8px; margin-bottom: 40px; display: flex; gap: 20px;">
                        <a href="javascript:void(0)" class="btn btn-sm btn-outline-primary" style="border-color: #1E88E5; color: #1E88E5;">
                            <i class="icon wb-heart"></i> 点赞
                        </a>
                        <a href="javascript:void(0)" class="btn btn-sm btn-outline-primary" style="border-color: #1E88E5; color: #1E88E5;">
                            <i class="icon wb-share"></i> 分享
                        </a>
                    </div>

                    <!-- 相关推荐 -->
                    <section style="padding-top: 40px; border-top: 2px solid #EEEEEE;">
                        <h3 style="margin-bottom: 30px;">相关推荐</h3>
                        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px;">
                            <tag action='list' cid="$data['classid']" num='3' type='news' orderby='inputtime DESC'>
                            <div class="card">
                                <div style="overflow: hidden; height: 150px; background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%);">
                                    <if value="$v['imgurl']">
                                        <img src="{$v.imgurl|thumb:300,150}" alt="{$v.title}" style="width: 100%; height: 100%; object-fit: cover;">
                                    <else/>
                                        <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                                            <i class="icon wb-book" style="font-size: 48px; color: rgba(30, 136, 229, 0.3);"></i>
                                        </div>
                                    </if>
                                </div>
                                <div class="card-body">
                                    <h5 style="font-size: 14px; margin-bottom: 10px;">
                                        <a href="{$v.url}" title="{$v.title}" style="color: #1E1E1E; text-decoration: none;">
                                            {$v.title|truncate:40}
                                        </a>
                                    </h5>
                                    <p style="font-size: 12px; color: #999; margin-bottom: 10px;">
                                        {$v.inputtime|date_format:'%Y-%m-%d'}
                                    </p>
                                    <a href="{$v.url}" class="btn btn-sm btn-primary" style="width: 100%;">查看详情</a>
                                </div>
                            </div>
                            </tag>
                        </div>
                    </section>
                </article>

                <!-- 右侧：侧边栏 -->
                <aside>
                    <!-- 作者信息卡片 -->
                    <div class="card" style="margin-bottom: 30px; text-align: center; padding: 30px 20px;">
                        <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;">
                            <i class="icon wb-user" style="font-size: 40px; color: white;"></i>
                        </div>
                        <h5>编辑部</h5>
                        <p style="font-size: 13px; color: #999; margin-bottom: 15px;">英语教学专家团队</p>
                        <p style="font-size: 13px; color: #666; line-height: 1.6; margin-bottom: 15px;">
                            致力于为英语学习者提供优质的教学资源和考试指导。
                        </p>
                    </div>

                    <!-- 热门文章 -->
                    <div class="card" style="margin-bottom: 30px;">
                        <div class="card-body">
                            <h5 style="margin-bottom: 20px;">热门文章</h5>
                            <ul style="list-style: none; padding: 0; margin: 0;">
                                <tag action='list' cid="$data['classid']" num='5' type='news' orderby='hits DESC'>
                                <li style="margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #EEEEEE;">
                                    <a href="{$v.url}" title="{$v.title}" style="color: #1E88E5; text-decoration: none; font-size: 13px; line-height: 1.6; display: block;">
                                        {$v.title|truncate:35}
                                    </a>
                                </li>
                                </tag>
                            </ul>
                        </div>
                    </div>

                    <!-- Google AdSense广告 -->
                    <div class="card" style="margin-bottom: 30px;">
                        <div class="card-body" style="padding: 0; overflow: hidden;">
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

                    <!-- 公众号推广卡片 -->
                    <div class="card">
                        <div class="card-body" style="text-align: center;">
                            <h5 style="margin-bottom: 15px;">关注公众号</h5>
                            <if value="$lang.wechat_qrcode">
                                <img src="{$lang.wechat_qrcode}" alt="微信公众号二维码" style="width: 100%; max-width: 150px; margin-bottom: 10px;">
                            <else/>
                                <div style="width: 100%; max-width: 150px; height: 150px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; border-radius: 8px;">
                                    <p style="color: #999; text-align: center; font-size: 12px;">二维码<br>配置中</p>
                                </div>
                            </if>
                            <p style="font-size: 12px; color: #999;">长按识别二维码</p>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    </section>
</main>

<include file="foot.php" />
