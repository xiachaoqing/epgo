<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />
<main>

<!-- ========== Hero Banner ========== -->
<section class="hero-banner">
    <div class="hero-banner-content">
        <div class="hero-tags">
            <span class="hero-tag">KET备考</span>
            <span class="hero-tag">PET备考</span>
            <span class="hero-tag">FCE进阶</span>
            <span class="hero-tag">每日英语</span>
        </div>
        <h1>英语陪跑GO</h1>
        <p class="subtitle">专业剑桥英语备考 · 每日干货不断更 · KET/PET高效冲关</p>
        <div class="hero-banner-buttons">
            <a href="{$c.index_url}news/" class="btn btn-primary">免费开始学习</a>
            <a href="javascript:void(0)" onclick="epgoEducation.showQRCode()" class="btn btn-outline-primary">关注公众号</a>
        </div>
        <div class="hero-stats">
            <div class="hero-stat-item">
                <span class="hero-stat-num" data-countup="5000" data-suffix="+">5000+</span>
                <span class="hero-stat-label">学习人次</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-num" data-countup="87" data-suffix="%">87%</span>
                <span class="hero-stat-label">考试通过率</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-num" data-countup="300" data-suffix="+">300+</span>
                <span class="hero-stat-label">精品文章</span>
            </div>
            <div class="hero-stat-item">
                <span class="hero-stat-num" data-countup="755" data-suffix="">755</span>
                <span class="hero-stat-label">核心词汇</span>
            </div>
        </div>
    </div>
</section>

<!-- ========== 核心导航卡片 ========== -->
<section class="service-cards">
    <div class="container">
        <div class="section-title">
            <h2>选择你的学习方向</h2>
            <p>KET / PET / FCE 全阶段覆盖，找到最适合你的内容</p>
        </div>
        <div class="service-cards-grid">
            <tag action='category' type='head' class='active'>
            <if value="$m['_index'] lt 3">
            <a href="{$m.url}" style="text-decoration:none; display:block;">
                <div class="service-card <if value="$m['_index'] eq 1">success<elseif value="$m['_index'] eq 2"/>warning</if>">
                    <div class="service-card-icon">
                        <i class="icon wb-book"></i>
                    </div>
                    <h3>{$m.name}</h3>
                    <p>{$m.description|met_substr:0,40}</p>
                </div>
            </a>
            </if>
            </tag>
            <a href="javascript:void(0)" onclick="epgoEducation.showQRCode()" style="text-decoration:none; display:block;">
                <div class="service-card danger">
                    <div class="service-card-icon">
                        <i class="icon wb-chat"></i>
                    </div>
                    <h3>关注公众号</h3>
                    <p>每日英语干货推送，考试技巧免费领取</p>
                </div>
            </a>
        </div>
    </div>
</section>

<!-- ========== 最新文章 ========== -->
<section class="section">
    <div class="container">
        <div class="section-title">
            <h2>最新学习内容</h2>
            <p>持续更新 KET/PET 备考干货，每篇都是精选</p>
        </div>
        <div class="content-list">
            <tag action='list' cid='$lang["home_news1"]' num='$lang["home_news_num"]' type='news' orderby='id DESC'>
            <div class="content-item" data-animate>
                <a href="{$v.url}" title="{$v.title}" class="content-item-link">
                    <div class="content-item-image">
                        <if value="$v['imgurl']">
                            <img src="{$v.imgurl|thumb:400,250}" alt="{$v.title}" loading="lazy">
                        <else/>
                            <div class="content-item-placeholder">
                                <i class="icon wb-book"></i>
                            </div>
                        </if>
                    </div>
                    <div class="content-item-body">
                        <span class="content-item-category">{$v.columnname}</span>
                        <h3 class="content-item-title">{$v.title}</h3>
                        <div class="content-item-meta">
                            <span><i class="icon wb-time"></i> {$v.inputtime|date_format:'%Y-%m-%d'}</span>
                            <span><i class="icon wb-eye"></i> {$v.hits}</span>
                        </div>
                        <if value="$v['description']">
                        <p class="content-item-desc">{$v.description|met_substr:0,60}</p>
                        </if>
                    </div>
                </a>
            </div>
            </tag>
        </div>
        <div style="text-align:center; margin-top:40px;">
            <a href="{$c.index_url}news/" class="btn btn-outline">查看全部文章 →</a>
        </div>
    </div>
</section>

<!-- ========== AdSense 广告位 ========== -->
<div class="adsense-wrap">
    <div class="adsense-label">广告</div>
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-2043497135383313"
         data-ad-slot="auto"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<!-- ========== 学员成就 ========== -->
<section class="section bg-light">
    <div class="container">
        <div class="section-title">
            <h2>学员真实反馈</h2>
            <p>他们用英语陪跑GO拿下了剑桥英语证书</p>
        </div>
        <div class="testimonial-grid">
            <div class="testimonial-card" data-animate>
                <div class="testimonial-avatar" style="background:linear-gradient(135deg,#1E88E5,#1565C0);">
                    <i class="icon wb-user" style="font-size:28px; color:#fff;"></i>
                </div>
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"跟着陪跑GO备考3个月，KET顺利通过！每天的单词推送真的很有用，错题分析也很到位。"</p>
                <div>
                    <span class="testimonial-author">小王同学</span>
                    <span class="testimonial-tag">KET 通过</span>
                </div>
            </div>
            <div class="testimonial-card" data-animate>
                <div class="testimonial-avatar" style="background:linear-gradient(135deg,#43A047,#2E7D32);">
                    <i class="icon wb-user" style="font-size:28px; color:#fff;"></i>
                </div>
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"PET写作一直是弱项，看了这里的连接词专题文章之后突然开窍了，最后写作部分超常发挥！"</p>
                <div>
                    <span class="testimonial-author">晓晓妈妈</span>
                    <span class="testimonial-tag">PET 通过</span>
                </div>
            </div>
            <div class="testimonial-card" data-animate>
                <div class="testimonial-avatar" style="background:linear-gradient(135deg,#FB8C00,#F57C00);">
                    <i class="icon wb-user" style="font-size:28px; color:#fff;"></i>
                </div>
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"公众号每天推送的真题解析质量很高，比报班便宜多了，而且可以随时刷！强烈推荐给备考的孩子。"</p>
                <div>
                    <span class="testimonial-author">李爸爸</span>
                    <span class="testimonial-tag">FCE 备考中</span>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ========== 公众号推广 ========== -->
<section class="promo-section">
    <div class="promo-container">
        <div class="promo-content">
            <h3>关注公众号 · 免费领备考资料</h3>
            <p>每天5分钟，KET/PET单词不用愁</p>
            <ul class="promo-benefits">
                <li>每日精选KET/PET核心词汇（含音频）</li>
                <li>真题解析·写作模板·听力技巧</li>
                <li>考试时间表·报名提醒</li>
                <li>备考群·专属答疑服务</li>
            </ul>
        </div>
        <div class="promo-qrcode">
            <div class="promo-qrcode-box">
                <if value="$lang['wechat_qrcode']">
                    <img src="{$lang.wechat_qrcode}" alt="英语陪跑GO公众号二维码">
                <else/>
                    <div style="width:160px; height:160px; display:flex; align-items:center; justify-content:center; background:#f0f0f0; color:#999; font-size:12px; text-align:center;">
                        请在后台<br>配置二维码
                    </div>
                </if>
            </div>
            <p class="promo-qrcode-text">长按扫码关注</p>
        </div>
    </div>
</section>

</main>
<include file="foot.php" />
