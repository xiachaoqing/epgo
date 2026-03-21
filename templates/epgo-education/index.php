<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<main>
    <!-- ========== Hero Banner ========== -->
    <section class="hero-banner">
        <div class="hero-banner-content">
            <h1>英语陪跑GO</h1>
            <p class="subtitle">让英语学习不再枯燥 • 专业KET/PET考试培训</p>
            <div class="hero-banner-buttons">
                <a href="#service-cards" class="btn btn-primary btn-lg">开始学习</a>
                <a href="javascript:void(0)" onclick="epgoEducation.showQRCode()" class="btn btn-outline-primary btn-lg">关注公众号</a>
            </div>
        </div>
    </section>

    <!-- ========== 核心服务卡片 ========== -->
    <section class="service-cards" id="service-cards">
        <div class="container">
            <div class="section-title">
                <h2>快速导航</h2>
            </div>

            <div class="service-cards-grid">
                <!-- KET教程 -->
                <tag action='category' cid='1' type='son' limit='1'>
                <a href="{$m.url}" style="text-decoration: none;">
                    <div class="service-card">
                        <div class="service-card-icon">
                            <i class="icon wb-book"></i>
                        </div>
                        <h3>KET考试教程</h3>
                        <p>KET真题解析、词汇教学、听力训练、写作技巧全套教程</p>
                    </div>
                </a>
                </tag>

                <!-- PET教程 -->
                <tag action='category' cid='2' type='son' limit='1'>
                <a href="{$m.url}" style="text-decoration: none;">
                    <div class="service-card success">
                        <div class="service-card-icon">
                            <i class="icon wb-book"></i>
                        </div>
                        <h3>PET考试教程</h3>
                        <p>PET完整学习路径，助力考试成功</p>
                    </div>
                </a>
                </tag>

                <!-- 学习资源 -->
                <tag action='category' cid='3' type='son' limit='1'>
                <a href="{$m.url}" style="text-decoration: none;">
                    <div class="service-card warning">
                        <div class="service-card-icon">
                            <i class="icon wb-download"></i>
                        </div>
                        <h3>学习资源</h3>
                        <p>词汇表、语法、真题、音频全免费下载</p>
                    </div>
                </a>
                </tag>

                <!-- 公众号推广 -->
                <a href="javascript:void(0)" onclick="epgoEducation.showQRCode()" style="text-decoration: none;">
                    <div class="service-card danger">
                        <div class="service-card-icon">
                            <i class="icon wb-share"></i>
                        </div>
                        <h3>关注公众号</h3>
                        <p>每日英语干货，考试技巧分享，免费答疑</p>
                    </div>
                </a>
            </div>
        </div>
    </section>

    <!-- ========== 最新课程内容 ========== -->
    <section class="section">
        <div class="container">
            <div class="section-title">
                <h2>最新课程</h2>
                <p class="text-muted">精选优质教学内容，助力你的英语之路</p>
            </div>

            <div class="content-list">
                <tag action='list' cid='1,2' num='8' type='news' orderby='id DESC'>
                <div class="content-item" data-animate>
                    <div class="content-item-image">
                        <if value="$v['imgurl']">
                            <img src="{$v.imgurl|thumb:400,250}" alt="{$v.title}" loading="lazy">
                        <else/>
                            <div style="width: 100%; height: 100%; background: linear-gradient(135deg, #E3F2FD 0%, #F3E5F5 100%); display: flex; align-items: center; justify-content: center;">
                                <i class="icon wb-book" style="font-size: 48px; color: rgba(30, 136, 229, 0.3);"></i>
                            </div>
                        </if>
                    </div>
                    <div class="content-item-body">
                        <span class="content-item-category">{$v.columnname}</span>
                        <h3 class="content-item-title"><a href="{$v.url}" title="{$v.title}" style="color: inherit; text-decoration: none;">{$v.title}</a></h3>
                        <div class="content-item-meta">
                            <span><i class="icon wb-time"></i> {$v.inputtime|date_format:'%Y-%m-%d'}</span>
                            <span><i class="icon wb-eye"></i> {$v.hits} 阅读</span>
                        </div>
                        <if value="$v['description']">
                            <p class="content-item-desc">{$v.description|htmlspecialchars|truncate:100}</p>
                        </if>
                        <a href="{$v.url}" class="btn btn-sm btn-primary">继续阅读</a>
                    </div>
                </div>
                </tag>
            </div>
        </div>
    </section>

    <!-- ========== 英文演讲&历史故事 ========== -->
    <section class="section" style="background-color: #F5F5F5;">
        <div class="container">
            <div class="section-title">
                <h2>英文演讲 & 历史故事</h2>
                <p class="text-muted">通过名人演讲和历史故事学习英语，增长见闻</p>
            </div>

            <div class="content-list">
                <tag action='list' cid='4' num='4' type='news' orderby='id DESC'>
                <div class="content-item" data-animate style="position: relative; overflow: hidden;">
                    <div class="content-item-image" style="position: relative;">
                        <if value="$v['imgurl']">
                            <img src="{$v.imgurl|thumb:400,250}" alt="{$v.title}" loading="lazy">
                        <else/>
                            <div style="width: 100%; height: 100%; background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); display: flex; align-items: center; justify-content: center;">
                                <i class="icon wb-play" style="font-size: 48px; color: rgba(251, 140, 0, 0.3);"></i>
                            </div>
                        </if>
                        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.3s ease;">
                            <i class="icon wb-play" style="font-size: 48px; color: white;"></i>
                        </div>
                    </div>
                    <div class="content-item-body">
                        <span class="content-item-category" style="background-color: #FFF3E0; color: #FB8C00;">{$v.columnname}</span>
                        <h3 class="content-item-title"><a href="{$v.url}" title="{$v.title}" style="color: inherit; text-decoration: none;">{$v.title}</a></h3>
                        <div class="content-item-meta">
                            <span><i class="icon wb-time"></i> {$v.inputtime|date_format:'%Y-%m-%d'}</span>
                        </div>
                    </div>
                </div>
                </tag>
            </div>
        </div>
    </section>

    <!-- ========== 学员成就 ========== -->
    <section class="section">
        <div class="container">
            <div class="section-title">
                <h2>学员成就</h2>
            </div>

            <!-- 数据统计 -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px; margin-bottom: 60px; text-align: center;">
                <div data-animate>
                    <h3 style="font-size: 36px; color: #1E88E5; margin-bottom: 10px; font-weight: bold;">5000+</h3>
                    <p class="text-muted">累计学员</p>
                </div>
                <div data-animate>
                    <h3 style="font-size: 36px; color: #43A047; margin-bottom: 10px; font-weight: bold;">87%</h3>
                    <p class="text-muted">考试通过率</p>
                </div>
                <div data-animate>
                    <h3 style="font-size: 36px; color: #FB8C00; margin-bottom: 10px; font-weight: bold;">4.8⭐</h3>
                    <p class="text-muted">平均评分</p>
                </div>
                <div data-animate>
                    <h3 style="font-size: 36px; color: #E53935; margin-bottom: 10px; font-weight: bold;">1000+</h3>
                    <p class="text-muted">小时教学</p>
                </div>
            </div>

            <!-- 学员案例 -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div class="card" data-animate style="text-align: center; padding: 30px 20px;">
                    <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%); margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; border: 3px solid #43A047;">
                        <i class="icon wb-user" style="font-size: 40px; color: white;"></i>
                    </div>
                    <h4>学员：小王</h4>
                    <p class="text-muted" style="margin-bottom: 15px;">KET 通过</p>
                    <p style="font-size: 14px; color: #FF9800; margin-bottom: 15px;">⭐⭐⭐⭐⭐</p>
                    <p style="font-size: 14px; color: var(--color-text); line-height: 1.6;">"3个月从零基础到KET通过，感谢老师的耐心指导！"</p>
                </div>

                <div class="card" data-animate style="text-align: center; padding: 30px 20px;">
                    <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #43A047 0%, #2E7D32 100%); margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; border: 3px solid #43A047;">
                        <i class="icon wb-user" style="font-size: 40px; color: white;"></i>
                    </div>
                    <h4>学员：小李</h4>
                    <p class="text-muted" style="margin-bottom: 15px;">PET 通过</p>
                    <p style="font-size: 14px; color: #FF9800; margin-bottom: 15px;">⭐⭐⭐⭐⭐</p>
                    <p style="font-size: 14px; color: var(--color-text); line-height: 1.6;">"系统的教学体系让我高效备考，PET顺利通过！"</p>
                </div>

                <div class="card" data-animate style="text-align: center; padding: 30px 20px;">
                    <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #FB8C00 0%, #F57C00 100%); margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; border: 3px solid #43A047;">
                        <i class="icon wb-user" style="font-size: 40px; color: white;"></i>
                    </div>
                    <h4>学员：小刘</h4>
                    <p class="text-muted" style="margin-bottom: 15px;">英语进阶</p>
                    <p style="font-size: 14px; color: #FF9800; margin-bottom: 15px;">⭐⭐⭐⭐⭐</p>
                    <p style="font-size: 14px; color: var(--color-text); line-height: 1.6;">"学到了真实有用的英语知识，现在能自信地说英语了！"</p>
                </div>
            </div>
        </div>
    </section>

    <!-- ========== Google AdSense 广告位 ========== -->
    <div class="adsense-container">
        <div class="adsense-label">赞助广告</div>
        <div style="margin: 0 auto; text-align: center;">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-2043497135383313"
                 data-ad-slot="2043497135383313"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                (adsbygoogle = window.adsbygoogle || []).push({});
            </script>
        </div>
    </div>

    <!-- ========== 公众号推广区 ========== -->
    <section class="promo-section">
        <div class="promo-container">
            <div class="promo-content">
                <h3>关注公众号 英语陪跑GO</h3>
                <p>坚持每日打卡，轻松提升英语水平</p>
                <ul class="promo-benefits">
                    <li>每日精选英语单词 (含发音)</li>
                    <li>KET/PET考试技巧分享</li>
                    <li>学习资料免费领取</li>
                    <li>专业老师在线答疑</li>
                </ul>
            </div>

            <div class="promo-qrcode">
                <div class="promo-qrcode-box">
                    <if value="$lang.wechat_qrcode">
                        <img src="{$lang.wechat_qrcode}" alt="微信公众号二维码">
                    <else/>
                        <div style="width: 180px; height: 180px; background: white; display: flex; align-items: center; justify-content: center;">
                            <p style="color: #999; text-align: center; font-size: 12px;">二维码配置中<br>(请在后台上传)</p>
                        </div>
                    </if>
                </div>
                <p class="promo-qrcode-text">长按扫码关注</p>
            </div>
        </div>
    </section>

</main>

<include file="foot.php" />
