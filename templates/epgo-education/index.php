<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<?php
/* ── Banner：从数据库读取，否则显示静态 fallback ── */
$_epgo_banners = array();
try {
    $_epgo_pdo = new PDO(
        'mysql:host=127.0.0.1;dbname=epgo_db;charset=utf8',
        'xiachaoqing', 'Xia@07090218',
        array(PDO::ATTR_ERRMODE => PDO::ERRMODE_SILENT)
    );
    $_epgo_stmt = $_epgo_pdo->query(
        "SELECT img_title,img_des,img_path,img_link FROM ep_flash ORDER BY no_order ASC LIMIT 6"
    );
    if ($_epgo_stmt) $_epgo_banners = $_epgo_stmt->fetchAll(PDO::FETCH_ASSOC);
} catch(Exception $_e) {}
?>

<!-- ════════════ BANNER ════════════ -->
<section class="epgo-banner-wrap" style="position:relative;overflow:hidden;background:#1e3a8a;line-height:0;">
<?php if (!empty($_epgo_banners)): ?>
    <?php foreach($_epgo_banners as $_bi => $_b): ?>
    <div class="epgo-slide" style="display:<?php echo $_bi===0?'block':'none'; ?>;position:relative;">
        <a href="<?php echo htmlspecialchars($_b['img_link']); ?>" title="<?php echo htmlspecialchars($_b['img_title']); ?>">
            <img src="<?php echo htmlspecialchars($_b['img_path']); ?>"
                 alt="<?php echo htmlspecialchars($_b['img_title']); ?>"
                 style="width:100%;height:480px;object-fit:cover;display:block;">
        </a>
        <?php if($_b['img_title']): ?>
        <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.6));padding:40px 60px 32px;line-height:1.4;">
            <h2 style="font-size:36px;font-weight:700;color:white;margin:0 0 10px;"><?php echo htmlspecialchars($_b['img_title']); ?></h2>
            <?php if($_b['img_des']): ?>
            <p style="font-size:17px;color:rgba(255,255,255,.9);margin:0 0 18px;"><?php echo htmlspecialchars($_b['img_des']); ?></p>
            <?php endif; ?>
            <a href="<?php echo htmlspecialchars($_b['img_link']); ?>" style="display:inline-block;background:white;color:#1e3a8a;font-weight:700;padding:11px 26px;border-radius:6px;text-decoration:none;font-size:15px;">立即查看 →</a>
        </div>
        <?php endif; ?>
    </div>
    <?php endforeach; ?>
<?php else: ?>
    <div class="epgo-slide" style="display:block;background:linear-gradient(135deg,#1e3a8a,#2563eb);padding:90px 0;text-align:center;">
        <h1 style="font-size:46px;font-weight:800;color:white;margin:0 0 14px;">英语陪跑GO</h1>
        <p style="font-size:19px;color:rgba(255,255,255,.9);margin:0 0 28px;">专业 KET / PET 备考平台，每天进步一点点</p>
        <a href="/ket/" style="display:inline-block;background:white;color:#1e3a8a;font-weight:700;padding:13px 30px;border-radius:8px;text-decoration:none;margin:0 8px;">KET备考 →</a>
        <a href="/pet/" style="display:inline-block;background:rgba(255,255,255,.18);color:white;font-weight:700;padding:13px 30px;border-radius:8px;text-decoration:none;border:2px solid white;margin:0 8px;">PET备考</a>
    </div>
<?php endif; ?>

    <div id="epgo-dots" style="position:absolute;bottom:14px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:10;"></div>
    <button onclick="epgoBannerPrev()" style="position:absolute;left:14px;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.22);border:none;color:white;width:42px;height:42px;border-radius:50%;font-size:22px;cursor:pointer;z-index:10;line-height:1;">‹</button>
    <button onclick="epgoBannerNext()" style="position:absolute;right:14px;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.22);border:none;color:white;width:42px;height:42px;border-radius:50%;font-size:22px;cursor:pointer;z-index:10;line-height:1;">›</button>
</section>

<style>
@media(max-width:768px){
  .epgo-banner-wrap img{height:220px !important;}
  .epgo-banner-wrap [style*="font-size:36px"]{font-size:20px !important;}
  .epgo-banner-wrap [style*="padding:40px"]{padding:16px 16px 14px !important;}
  .epgo-banner-wrap p{display:none !important;}
  .epgo-banner-wrap button{display:none;}
}
</style>

<script>
(function(){
    var slides=document.querySelectorAll('.epgo-slide');
    var dots=document.getElementById('epgo-dots');
    if(!slides||slides.length<=1)return;
    var cur=0,timer;
    slides.forEach(function(_,i){
        var d=document.createElement('div');
        d.style.cssText='width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,'+(i?'.4':'1')+');cursor:pointer;transition:all .3s;';
        d.onclick=function(){stop();go(i);start();};
        dots.appendChild(d);
    });
    function go(n){
        slides[cur].style.display='none';
        dots.children[cur].style.background='rgba(255,255,255,.4)';
        cur=(n+slides.length)%slides.length;
        slides[cur].style.display='block';
        dots.children[cur].style.background='rgba(255,255,255,1)';
    }
    function start(){timer=setInterval(function(){go(cur+1);},5000);}
    function stop(){clearInterval(timer);}
    start();
    var wrap=document.querySelector('.epgo-banner-wrap');
    wrap.addEventListener('mouseenter',stop);
    wrap.addEventListener('mouseleave',start);
    var tx=0;
    wrap.addEventListener('touchstart',function(e){tx=e.touches[0].clientX;},{passive:true});
    wrap.addEventListener('touchend',function(e){
        var d=e.changedTouches[0].clientX-tx;
        if(Math.abs(d)>50){stop();go(d<0?cur+1:cur-1);start();}
    });
    window.epgoBannerPrev=function(){stop();go(cur-1);start();};
    window.epgoBannerNext=function(){stop();go(cur+1);start();};
})();
</script>


<!-- ════════════ 数据统计 ════════════ -->
<section style="background:#fff;padding:40px 0;border-bottom:1px solid #E5E7EB;">
    <div class="container">
        <div class="epgo-stat-grid">
            <div class="epgo-stat-item">
                <div class="epgo-stat-num" style="color:#2563EB;">10000+</div>
                <div class="epgo-stat-label">学员已学</div>
            </div>
            <div class="epgo-stat-item">
                <div class="epgo-stat-num" style="color:#16A34A;">1000+</div>
                <div class="epgo-stat-label">精品课程</div>
            </div>
            <div class="epgo-stat-item">
                <div class="epgo-stat-num" style="color:#EA580C;">98%</div>
                <div class="epgo-stat-label">考试通过率</div>
            </div>
            <div class="epgo-stat-item">
                <div class="epgo-stat-num" style="color:#FDB022;">24H</div>
                <div class="epgo-stat-label">快速答疑</div>
            </div>
        </div>
    </div>
</section>

<style>
.epgo-stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;text-align:center;}
.epgo-stat-num{font-size:38px;font-weight:800;line-height:1.1;}
.epgo-stat-label{font-size:13px;color:#6B7280;margin-top:8px;}
@media(max-width:576px){
  .epgo-stat-grid{grid-template-columns:repeat(2,1fr);gap:24px 16px;}
  .epgo-stat-num{font-size:28px;}
}
</style>


<!-- ════════════ 每日英语打卡 ════════════ -->
<section style="padding:60px 0;background:linear-gradient(135deg,#EFF6FF,#F0FDF4);">
    <div class="container">
        <div style="text-align:center;margin-bottom:40px;">
            <h2 style="font-size:32px;font-weight:800;color:#111827;margin:0 0 10px;">每日英语打卡</h2>
            <p style="font-size:15px;color:#6B7280;margin:0;">坚持每天学一句，量变引发质变</p>
        </div>
        <div class="epgo-daily-grid">
            <!-- 今日金句 -->
            <div class="epgo-daily-card" style="background:linear-gradient(135deg,#1e3a8a,#2563eb);color:white;border-radius:16px;padding:32px;position:relative;overflow:hidden;">
                <div style="font-size:11px;font-weight:700;letter-spacing:2px;opacity:.7;margin-bottom:16px;text-transform:uppercase;">TODAY'S SENTENCE</div>
                <blockquote style="font-size:20px;font-weight:700;line-height:1.5;margin:0 0 14px;font-style:italic;">
                    "The secret of getting ahead is getting started."
                </blockquote>
                <p style="font-size:14px;opacity:.85;margin:0 0 20px;">万事开头难，迈出第一步才是关键。— Mark Twain</p>
                <a href="/daily/" style="display:inline-block;background:rgba(255,255,255,.2);color:white;padding:8px 20px;border-radius:6px;text-decoration:none;font-size:13px;font-weight:600;border:1px solid rgba(255,255,255,.4);">查看更多金句 →</a>
                <div style="position:absolute;right:-20px;bottom:-20px;font-size:120px;opacity:.06;line-height:1;">❝</div>
            </div>

            <!-- KET / PET 学习路径 -->
            <div style="background:white;border-radius:16px;padding:28px;box-shadow:0 2px 12px rgba(0,0,0,.07);">
                <div style="font-size:13px;font-weight:700;color:#16A34A;margin-bottom:16px;">学习路径指南</div>
                <div class="epgo-path-list">
                    <a href="/ket/" class="epgo-path-item" style="--c:#2563EB;">
                        <span class="epgo-path-badge" style="background:#EFF6FF;color:#2563EB;">KET</span>
                        <span>初级认证 · 适合初高中生</span>
                        <span class="epgo-path-arrow">→</span>
                    </a>
                    <a href="/pet/" class="epgo-path-item" style="--c:#16A34A;">
                        <span class="epgo-path-badge" style="background:#F0FDF4;color:#16A34A;">PET</span>
                        <span>中级认证 · 适合高中大学</span>
                        <span class="epgo-path-arrow">→</span>
                    </a>
                    <a href="/reading/" class="epgo-path-item" style="--c:#EA580C;">
                        <span class="epgo-path-badge" style="background:#FFF7ED;color:#EA580C;">阅读</span>
                        <span>英语阅读 · 精读泛读技巧</span>
                        <span class="epgo-path-arrow">→</span>
                    </a>
                    <a href="/download/" class="epgo-path-item" style="--c:#7C3AED;">
                        <span class="epgo-path-badge" style="background:#F5F3FF;color:#7C3AED;">资料</span>
                        <span>免费下载 · 历年真题资料</span>
                        <span class="epgo-path-arrow">→</span>
                    </a>
                </div>
            </div>

            <!-- 关注公众号获取每日推送 -->
            <div style="background:white;border-radius:16px;padding:28px;box-shadow:0 2px 12px rgba(0,0,0,.07);text-align:center;">
                <div style="font-size:13px;font-weight:700;color:#EA580C;margin-bottom:16px;">关注公众号</div>
                <div style="width:130px;height:130px;margin:0 auto 16px;background:#f3f4f6;border-radius:12px;overflow:hidden;display:flex;align-items:center;justify-content:center;">
                    <if value="$c['footinfo_wx']">
                        <img src="{$c.footinfo_wx|thumb:130,130}" alt="英语陪跑GO公众号" style="width:100%;height:100%;object-fit:cover;">
                    <else/>
                        <span style="font-size:12px;color:#9CA3AF;text-align:center;padding:10px;">扫码关注<br>每日推送</span>
                    </if>
                </div>
                <p style="font-size:13px;color:#6B7280;margin:0 0 14px;line-height:1.6;">每日备考干货<br>词汇 / 真题 / 写作技巧</p>
                <a href="/about/" style="display:inline-block;background:#07C160;color:white;padding:9px 22px;border-radius:6px;text-decoration:none;font-size:13px;font-weight:600;">微信扫码关注</a>
            </div>
        </div>
    </div>
</section>

<style>
.epgo-daily-grid{display:grid;grid-template-columns:1fr 1fr 280px;gap:20px;align-items:start;}
.epgo-path-list{display:flex;flex-direction:column;gap:10px;}
.epgo-path-item{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;background:#F9FAFB;text-decoration:none;color:#374151;font-size:13px;transition:background .2s;}
.epgo-path-item:hover{background:#EFF6FF;color:#2563EB;text-decoration:none;}
.epgo-path-item:hover .epgo-path-arrow{opacity:1;transform:translateX(4px);}
.epgo-path-badge{font-size:11px;font-weight:800;padding:2px 8px;border-radius:4px;white-space:nowrap;}
.epgo-path-arrow{margin-left:auto;opacity:.3;transition:all .2s;}
@media(max-width:992px){
  .epgo-daily-grid{grid-template-columns:1fr 1fr;}
  .epgo-daily-grid>:last-child{grid-column:1/-1;}
}
@media(max-width:576px){
  .epgo-daily-grid{grid-template-columns:1fr;}
}
</style>


<!-- ════════════ 课程体系 ════════════ -->
<section style="padding:60px 0;background:#F9FAFB;">
    <div class="container">
        <div style="text-align:center;margin-bottom:40px;">
            <h2 style="font-size:32px;font-weight:800;color:#111827;margin:0 0 10px;">精选课程体系</h2>
            <p style="font-size:15px;color:#6B7280;margin:0;">从入门到进阶，全覆盖 KET / PET 备考需求</p>
        </div>
        <div class="row">
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:24px;">
                <div class="epgo-course-card" style="border-top-color:#2563EB;">
                    <div class="epgo-course-icon" style="background:#EFF6FF;color:#2563EB;">K</div>
                    <h3 class="epgo-course-title">KET 备考</h3>
                    <p class="epgo-course-desc">剑桥英语初级认证，适合初中到高中学生，全面覆盖听说读写，从零基础到高分通过。</p>
                    <div class="epgo-course-links">
                        <a href="/ket-exam/list-111.html">真题解析</a>
                        <a href="/ket-word/list-112.html">词汇速记</a>
                        <a href="/ket-write/list-113.html">写作指导</a>
                        <a href="/ket-listen/list-114.html">听力技巧</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:24px;">
                <div class="epgo-course-card" style="border-top-color:#16A34A;">
                    <div class="epgo-course-icon" style="background:#F0FDF4;color:#16A34A;">P</div>
                    <h3 class="epgo-course-title">PET 备考</h3>
                    <p class="epgo-course-desc">剑桥英语中级认证，适合高中到大学学生，国际认可资格证书，提升竞争力必备选择。</p>
                    <div class="epgo-course-links">
                        <a href="/pet-exam/list-121.html">真题解析</a>
                        <a href="/pet-word/list-122.html">词汇速记</a>
                        <a href="/pet-write/list-123.html">写作指导</a>
                        <a href="/pet-read/list-124.html">阅读技巧</a>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:24px;">
                <div class="epgo-course-card" style="border-top-color:#EA580C;">
                    <div class="epgo-course-icon" style="background:#FFF7ED;color:#EA580C;">英</div>
                    <h3 class="epgo-course-title">通用英语</h3>
                    <p class="epgo-course-desc">日常英语综合学习，涵盖阅读、写作和演讲等，提升综合语言能力，适合各个年龄段。</p>
                    <div class="epgo-course-links">
                        <a href="/reading/">英语阅读</a>
                        <a href="/daily/">每日英语</a>
                        <a href="/download/">资料下载</a>
                        <a href="/reading/">学习资讯</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<style>
.epgo-course-card{background:white;border-radius:12px;padding:32px 28px;box-shadow:0 2px 8px rgba(0,0,0,.07);border-top:4px solid #eee;height:100%;transition:box-shadow .3s,transform .3s;}
.epgo-course-card:hover{box-shadow:0 8px 24px rgba(0,0,0,.12);transform:translateY(-4px);}
.epgo-course-icon{width:52px;height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;margin-bottom:18px;}
.epgo-course-title{font-size:20px;font-weight:700;color:#111827;margin:0 0 10px;}
.epgo-course-desc{color:#6B7280;font-size:14px;line-height:1.7;margin:0 0 20px;}
.epgo-course-links{display:flex;flex-wrap:wrap;gap:8px;}
.epgo-course-links a{background:#F3F4F6;color:#374151;padding:5px 12px;border-radius:6px;font-size:12px;font-weight:600;text-decoration:none;transition:background .2s,color .2s;}
.epgo-course-links a:hover{background:#2563EB;color:white;text-decoration:none;}
</style>


<!-- ════════════ 最新文章 ════════════ -->
<section style="padding:60px 0;background:white;">
    <div class="container">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:36px;flex-wrap:wrap;gap:12px;">
            <div>
                <h2 style="font-size:32px;font-weight:800;color:#111827;margin:0 0 6px;">最新学习资源</h2>
                <p style="font-size:14px;color:#6B7280;margin:0;">精选英语学习内容，每日更新</p>
            </div>
            <a href="/reading/" style="background:#EFF6FF;color:#2563EB;padding:9px 20px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:700;white-space:nowrap;">查看全部 →</a>
        </div>
        <div class="row">
            <?php
            $_epgo_home_articles = array();
            try {
                $_epgo_article_pdo = new PDO(
                    'mysql:host=127.0.0.1;dbname=epgo_db;charset=utf8',
                    'xiachaoqing',
                    'Xia@07090218',
                    array(PDO::ATTR_ERRMODE => PDO::ERRMODE_SILENT)
                );
                $_epgo_article_sql = "
                    SELECT id,title,description,imgurl,updatetime,hits,class1,class2,class3
                    FROM ep_news
                    WHERE recycle=0 AND lang='cn' AND class1 IN (103,104,105,111,112,113,114,121,122,123,124)
                    ORDER BY id DESC
                    LIMIT 9
                ";
                $_epgo_article_stmt = $_epgo_article_pdo->query($_epgo_article_sql);
                if ($_epgo_article_stmt) {
                    $_epgo_home_articles = $_epgo_article_stmt->fetchAll(PDO::FETCH_ASSOC);
                }
            } catch(Exception $_e) {}

            $_epgo_issue_map = array(
                103 => '英语阅读',
                104 => '英语演讲',
                105 => '每日英语',
                111 => 'KET真题解析',
                112 => 'KET词汇速记',
                113 => 'KET写作指导',
                114 => 'KET听力技巧',
                121 => 'PET真题解析',
                122 => 'PET词汇速记',
                123 => 'PET写作指导',
                124 => 'PET阅读技巧'
            );

            $_epgo_url_map = array(
                103 => '/reading/',
                104 => '/speech/',
                105 => '/daily/',
                111 => '/ket-exam/',
                112 => '/ket-word/',
                113 => '/ket-write/',
                114 => '/ket-listen/',
                121 => '/pet-exam/',
                122 => '/pet-word/',
                123 => '/pet-write/',
                124 => '/pet-read/'
            );
            ?>
            <?php foreach($_epgo_home_articles as $_v): ?>
            <?php
                $_classid = intval($_v['class1']);
                $_issue = isset($_epgo_issue_map[$_classid]) ? $_epgo_issue_map[$_classid] : '学习资源';
                $_base = isset($_epgo_url_map[$_classid]) ? $_epgo_url_map[$_classid] : '/reading/';
                $_url = rtrim($_base, '/') . '/' . intval($_v['id']) . '.html';
                $_img = trim($_v['imgurl']);
                if (!$_img) {
                    if (in_array($_classid, array(101,111,112,113,114))) $_img = '../upload/epgo-defaults/ket.png';
                    if (in_array($_classid, array(102,121,122,123,124))) $_img = '../upload/epgo-defaults/pet.png';
                    if (in_array($_classid, array(103,104))) $_img = '../upload/epgo-defaults/reading.png';
                    if (in_array($_classid, array(105))) $_img = '../upload/epgo-defaults/daily.png';
                }
                $_desc = trim(strip_tags($_v['description']));
                if (!$_desc) $_desc = '精选英语学习内容，帮助你更高效地完成日常学习与考试备考。';
                $_time = $_v['updatetime'] ? date('Y-m-d', strtotime($_v['updatetime'])) : '';
            ?>
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:24px;">
                <div class="epgo-article-card">
                    <?php if($_img): ?>
                    <div class="epgo-article-img">
                        <a href="<?php echo $_url; ?>" title="<?php echo htmlspecialchars($_v['title']); ?>">
                            <img src="<?php echo htmlspecialchars($_img); ?>" alt="<?php echo htmlspecialchars($_v['title']); ?>">
                        </a>
                    </div>
                    <?php else: ?>
                    <div class="epgo-article-img epgo-article-img-fallback">
                        <span><?php echo htmlspecialchars($_issue); ?></span>
                    </div>
                    <?php endif; ?>
                    <div class="epgo-article-body">
                        <div class="epgo-article-cat"><?php echo htmlspecialchars($_issue); ?></div>
                        <h3 class="epgo-article-title">
                            <a href="<?php echo $_url; ?>" title="<?php echo htmlspecialchars($_v['title']); ?>"><?php echo htmlspecialchars($_v['title']); ?></a>
                        </h3>
                        <p class="epgo-article-desc"><?php echo htmlspecialchars(mb_substr($_desc, 0, 90)); ?></p>
                        <div class="epgo-article-meta">
                            <span><?php echo $_time; ?></span>
                            <span><?php echo intval($_v['hits']); ?> 阅读</span>
                        </div>
                    </div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<style>
.epgo-article-card{background:white;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08);border:1px solid #E5E7EB;transition:box-shadow .3s,transform .3s;height:100%;}
.epgo-article-card:hover{box-shadow:0 8px 20px rgba(0,0,0,.11);transform:translateY(-4px);}
.epgo-article-img{height:180px;overflow:hidden;background:#F3F4F6;}
.epgo-article-img a{display:block;width:100%;height:100%;}
.epgo-article-img img{width:100%;height:100%;object-fit:cover;transition:transform .4s;}
.epgo-article-card:hover .epgo-article-img img{transform:scale(1.04);}
.epgo-article-img-fallback{display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#EFF6FF,#DBEAFE);}
.epgo-article-img-fallback span{font-size:13px;color:#3B82F6;font-weight:700;}
.epgo-article-body{padding:18px;}
.epgo-article-cat{font-size:11px;color:#2563EB;font-weight:700;margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px;}
.epgo-article-title{font-size:15px;font-weight:700;color:#111827;margin:0 0 10px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.epgo-article-title a{color:inherit;text-decoration:none;}
.epgo-article-title a:hover{color:#2563EB;}
.epgo-article-desc{color:#6B7280;font-size:13px;line-height:1.6;margin:0 0 12px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.epgo-article-meta{display:flex;justify-content:space-between;font-size:11px;color:#9CA3AF;padding-top:10px;border-top:1px solid #F3F4F6;}
</style>


<!-- ════════════ 学员评价 ════════════ -->
<section style="padding:60px 0;background:#EFF6FF;">
    <div class="container">
        <div style="text-align:center;margin-bottom:36px;">
            <h2 style="font-size:32px;font-weight:800;color:#111827;margin:0 0 10px;">学员评价</h2>
            <p style="font-size:15px;color:#6B7280;margin:0;">真实学员反馈，见证每一次进步</p>
        </div>
        <div class="row">
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:24px;">
                <div class="epgo-review-card" style="border-left-color:#FDB022;">
                    <div class="epgo-review-stars">★★★★★</div>
                    <p class="epgo-review-text">"非常棒的平台！KET课程讲得特别清楚，从基础开始学，现在已经通过考试了。老师非常耐心，课后问题都能及时回答。"</p>
                    <div class="epgo-review-author">
                        <strong>李同学</strong>
                        <span>北京 · KET高分通过</span>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:24px;">
                <div class="epgo-review-card" style="border-left-color:#16A34A;">
                    <div class="epgo-review-stars">★★★★★</div>
                    <p class="epgo-review-text">"PET备考课程非常系统，从词汇到写作都有详细讲解。真题解析让我掌握了出题规律，考试时信心十足！"</p>
                    <div class="epgo-review-author">
                        <strong>王同学</strong>
                        <span>上海 · PET高分通过</span>
                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:24px;">
                <div class="epgo-review-card" style="border-left-color:#2563EB;">
                    <div class="epgo-review-stars">★★★★★</div>
                    <p class="epgo-review-text">"物超所值！学到了考试内容，还能学到实用英语技能。现在可以流畅地和外国友人交流，感谢英语陪跑GO！"</p>
                    <div class="epgo-review-author">
                        <strong>林同学</strong>
                        <span>福州 · PET高分+口语提升</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<style>
.epgo-review-card{background:white;padding:28px;border-radius:12px;box-shadow:0 1px 4px rgba(0,0,0,.06);border-left:4px solid #eee;height:100%;}
.epgo-review-stars{color:#FDB022;font-size:16px;margin-bottom:14px;}
.epgo-review-text{color:#6B7280;font-style:italic;font-size:14px;line-height:1.8;margin:0 0 18px;}
.epgo-review-author strong{display:block;color:#111827;font-size:14px;}
.epgo-review-author span{font-size:12px;color:#9CA3AF;}
</style>


<!-- ════════════ 常见问题 ════════════ -->
<section style="padding:60px 0;background:white;">
    <div class="container">
        <div style="text-align:center;margin-bottom:36px;">
            <h2 style="font-size:32px;font-weight:800;color:#111827;margin:0 0 10px;">常见问题</h2>
            <p style="font-size:15px;color:#6B7280;margin:0;">有疑问？这里有答案</p>
        </div>
        <div style="max-width:760px;margin:0 auto;" class="epgo-faq">
            <div class="epgo-faq-item">
                <div class="epgo-faq-q" onclick="epgoToggleFaq(this)">KET 和 PET 有什么区别？<span class="epgo-faq-icon">+</span></div>
                <div class="epgo-faq-a">KET（初级）适合初中到高中学生，难度相对较低。PET（中级）是KET的进阶版本，适合高中到大学学生，我们提供两个级别的完整课程，可根据英语水平选择。</div>
            </div>
            <div class="epgo-faq-item">
                <div class="epgo-faq-q" onclick="epgoToggleFaq(this)">课程有效期是多久？<span class="epgo-faq-icon">+</span></div>
                <div class="epgo-faq-a">课程永久有效，可随时学习和复习。我们会定期更新内容，确保你学到最新的考试信息和技巧。</div>
            </div>
            <div class="epgo-faq-item">
                <div class="epgo-faq-q" onclick="epgoToggleFaq(this)">如何获得每日备考内容推送？<span class="epgo-faq-icon">+</span></div>
                <div class="epgo-faq-a">关注我们的微信公众号"英语陪跑GO"，每日推送备考词汇、真题解析和写作技巧，坚持跟读效果显著。可扫描页面底部二维码关注。</div>
            </div>
            <div class="epgo-faq-item">
                <div class="epgo-faq-q" onclick="epgoToggleFaq(this)">如果没通过考试怎么办？<span class="epgo-faq-icon">+</span></div>
                <div class="epgo-faq-a">我们有完善的反馈机制。如果学习了全部课程还没通过，可以联系我们获得额外指导和支持。帮你成功通过考试是我们的目标！</div>
            </div>
        </div>
    </div>
</section>

<style>
.epgo-faq-item{border-bottom:1px solid #E5E7EB;padding:0;}
.epgo-faq-q{padding:18px 0;font-size:15px;font-weight:600;color:#111827;cursor:pointer;display:flex;justify-content:space-between;align-items:center;user-select:none;}
.epgo-faq-q:hover{color:#2563EB;}
.epgo-faq-icon{font-size:20px;color:#9CA3AF;transition:transform .25s;flex-shrink:0;margin-left:12px;}
.epgo-faq-a{display:none;padding:0 0 18px;font-size:14px;color:#6B7280;line-height:1.8;}
.epgo-faq-item.open .epgo-faq-a{display:block;}
.epgo-faq-item.open .epgo-faq-icon{transform:rotate(45deg);}
</style>

<script>
function epgoToggleFaq(el){
    var item=el.parentElement;
    var wasOpen=item.classList.contains('open');
    document.querySelectorAll('.epgo-faq-item').forEach(function(i){i.classList.remove('open');});
    if(!wasOpen) item.classList.add('open');
}
</script>


<!-- ════════════ 关注我们 CTA ════════════ -->
<section style="padding:56px 0;background:linear-gradient(135deg,#1e3a8a,#2563eb);">
    <div class="container" style="text-align:center;">
        <h2 style="font-size:30px;font-weight:800;color:white;margin:0 0 12px;">关注公众号，每天进步一点点</h2>
        <p style="font-size:15px;color:rgba(255,255,255,.85);margin:0 0 28px;">扫码关注"英语陪跑GO"，每日推送 KET/PET 备考干货、词汇和真题解析</p>
        <div style="display:flex;justify-content:center;align-items:center;gap:16px;flex-wrap:wrap;">
            <a href="/about/" style="background:white;color:#1e3a8a;padding:12px 28px;border-radius:8px;font-weight:700;text-decoration:none;font-size:14px;">了解更多 →</a>
            <a href="/reading/" style="background:rgba(255,255,255,.15);color:white;padding:12px 28px;border-radius:8px;font-weight:700;text-decoration:none;font-size:14px;border:1px solid rgba(255,255,255,.4);">浏览文章</a>
        </div>
    </div>
</section>


<!-- 二维码弹窗 -->
<div id="epgo-qr-modal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center;">
    <div style="background:white;border-radius:16px;padding:36px;text-align:center;max-width:320px;width:90%;position:relative;">
        <button onclick="epgoCloseQR()" style="position:absolute;top:12px;right:14px;background:none;border:none;font-size:22px;cursor:pointer;color:#9CA3AF;">×</button>
        <h3 style="font-size:18px;font-weight:700;margin:0 0 6px;color:#111827;">英语陪跑GO</h3>
        <p style="font-size:13px;color:#6B7280;margin:0 0 18px;">扫码关注，每天备考干货</p>
        <div style="width:160px;height:160px;margin:0 auto 14px;background:#f3f4f6;border-radius:8px;overflow:hidden;">
            <if value="$c['footinfo_wx']">
                <img src="{$c.footinfo_wx|thumb:160,160}" alt="公众号二维码" style="width:100%;height:100%;object-fit:cover;">
            <else/>
                <div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;color:#9CA3AF;font-size:12px;">二维码配置中</div>
            </if>
        </div>
        <p style="font-size:12px;color:#9CA3AF;margin:0;">长按识别二维码关注</p>
    </div>
</div>

<script>
(function(){
    var scrollY=0;
    window.epgoShowQR=function(){
        scrollY=window.scrollY;
        document.body.style.overflow='hidden';
        document.getElementById('epgo-qr-modal').style.display='flex';
    };
    window.epgoCloseQR=function(){
        document.body.style.overflow='';
        window.scrollTo(0,scrollY);
        document.getElementById('epgo-qr-modal').style.display='none';
    };
})();
</script>

<include file="foot.php" />
