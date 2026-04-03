<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<!-- 首页轮播 Banner（从 ep_flash 表读取，PHP直接查库） -->
<?php
$_epgo_banners = array();
try {
    $_epgo_pdo = new PDO(
        'mysql:host=127.0.0.1;dbname=epgo_db;charset=utf8',
        'xiachaoqing', '***REMOVED***',
        array(PDO::ATTR_ERRMODE => PDO::ERRMODE_SILENT)
    );
    $_epgo_stmt = $_epgo_pdo->query("SELECT img_title,img_des,img_path,img_link FROM ep_flash ORDER BY no_order ASC LIMIT 6");
    if ($_epgo_stmt) {
        $_epgo_banners = $_epgo_stmt->fetchAll(PDO::FETCH_ASSOC);
    }
} catch(Exception $_e) {}
?>
<section class="epgo-banner-wrap" style="position:relative;overflow:hidden;background:#1e3a8a;line-height:0;">
<?php if (!empty($_epgo_banners)): ?>
    <?php foreach($_epgo_banners as $_bi => $_b): ?>
    <div class="epgo-slide" style="display:<?php echo $_bi===0?'block':'none'; ?>;position:relative;">
        <a href="<?php echo htmlspecialchars($_b['img_link']); ?>" title="<?php echo htmlspecialchars($_b['img_title']); ?>">
            <img src="<?php echo htmlspecialchars($_b['img_path']); ?>"
                 alt="<?php echo htmlspecialchars($_b['img_title']); ?>"
                 style="width:100%;height:520px;object-fit:cover;display:block;">
        </a>
        <?php if($_b['img_title']): ?>
        <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.65));padding:50px 60px 36px;line-height:1.4;">
            <h2 style="font-size:38px;font-weight:700;color:white;margin:0 0 10px;text-shadow:0 2px 8px rgba(0,0,0,.4);"><?php echo htmlspecialchars($_b['img_title']); ?></h2>
            <?php if($_b['img_des']): ?>
            <p style="font-size:18px;color:rgba(255,255,255,.9);margin:0 0 20px;text-shadow:0 1px 4px rgba(0,0,0,.3);"><?php echo htmlspecialchars($_b['img_des']); ?></p>
            <?php endif; ?>
            <a href="<?php echo htmlspecialchars($_b['img_link']); ?>" style="display:inline-block;background:#FDB022;color:#1e3a8a;font-weight:700;padding:12px 28px;border-radius:6px;text-decoration:none;font-size:15px;">立即查看 →</a>
        </div>
        <?php endif; ?>
    </div>
    <?php endforeach; ?>
<?php else: ?>
    <!-- fallback: 没有banner数据时显示静态背景 -->
    <div class="epgo-slide" style="display:block;background:linear-gradient(135deg,#1e3a8a,#2563eb);padding:80px 0;text-align:center;">
        <h1 style="font-size:48px;font-weight:800;color:white;margin:0 0 16px;">英语陪跑GO</h1>
        <p style="font-size:20px;color:rgba(255,255,255,.9);margin:0 0 28px;">专业KET/PET英语备考平台 · 10000+学员</p>
        <a href="{$c.index_url}ket/" style="display:inline-block;background:#FDB022;color:#1e3a8a;font-weight:700;padding:14px 32px;border-radius:8px;text-decoration:none;margin:0 8px;">KET备考 →</a>
        <a href="{$c.index_url}pet/" style="display:inline-block;background:rgba(255,255,255,.2);color:white;font-weight:700;padding:14px 32px;border-radius:8px;text-decoration:none;border:2px solid white;margin:0 8px;">PET备考</a>
    </div>
<?php endif; ?>

    <!-- 指示点 -->
    <div id="epgo-dots" style="position:absolute;bottom:16px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:10;"></div>
    <button onclick="epgoBannerPrev()" style="position:absolute;left:16px;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.25);border:none;color:white;width:44px;height:44px;border-radius:50%;font-size:22px;cursor:pointer;z-index:10;line-height:1;">‹</button>
    <button onclick="epgoBannerNext()" style="position:absolute;right:16px;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.25);border:none;color:white;width:44px;height:44px;border-radius:50%;font-size:22px;cursor:pointer;z-index:10;line-height:1;">›</button>
</section>

<style>
@media(max-width:768px){
  .epgo-banner-wrap img{height:240px !important;}
  .epgo-banner-wrap [style*="font-size:38px"]{font-size:22px !important;}
  .epgo-banner-wrap [style*="padding:50px"]{padding:20px 20px 16px !important;}
  .epgo-banner-wrap p{display:none;}
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
        d.style.cssText='width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,'+(i?'.45':'1')+');cursor:pointer;transition:all .3s;';
        d.onclick=function(){stop();go(i);start();};
        dots.appendChild(d);
    });
    function go(n){
        slides[cur].style.display='none';
        dots.children[cur].style.background='rgba(255,255,255,.45)';
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

<!-- 数据统计 - 优化版 -->
<section style="background:linear-gradient(135deg, #ffffff 0%, #f9fafb 100%); padding:50px 0; border-bottom:1px solid #E5E7EB;">
    <div class="container">
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(160px, 1fr)); gap:40px; text-align:center;">
            <div style="transition:all 0.3s; transform:translateY(0);" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size:42px; font-weight:800; background:linear-gradient(135deg, #2563EB, #1d4ed8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">10000+</div>
                <div style="font-size:14px; color:#6B7280; margin-top:12px; font-weight:500;">学员已学</div>
                <div style="font-size:12px; color:#9CA3AF; margin-top:6px;">遍布全国各地</div>
            </div>
            <div style="transition:all 0.3s; transform:translateY(0);" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size:42px; font-weight:800; background:linear-gradient(135deg, #16A34A, #15803d); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">1000+</div>
                <div style="font-size:14px; color:#6B7280; margin-top:12px; font-weight:500;">精品课程</div>
                <div style="font-size:12px; color:#9CA3AF; margin-top:6px;">持续更新维护</div>
            </div>
            <div style="transition:all 0.3s; transform:translateY(0);" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size:42px; font-weight:800; background:linear-gradient(135deg, #EA580C, #c2410c); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">98%</div>
                <div style="font-size:14px; color:#6B7280; margin-top:12px; font-weight:500;">通过率</div>
                <div style="font-size:12px; color:#9CA3AF; margin-top:6px;">历史成绩统计</div>
            </div>
            <div style="transition:all 0.3s; transform:translateY(0);" onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size:42px; font-weight:800; background:linear-gradient(135deg, #FDB022, #d99e04); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">24H</div>
                <div style="font-size:14px; color:#6B7280; margin-top:12px; font-weight:500;">快速反馈</div>
                <div style="font-size:12px; color:#9CA3AF; margin-top:6px;">平均响应时间</div>
            </div>
        </div>
    </div>
</section>

<!-- 课程分类 -->
<section style="padding:60px 0; background:#f9fafb;">
    <div class="container">
        <h2 style="font-size:36px; font-weight:700; text-align:center; color:#111827; margin:0 0 50px 0;">
            精选课程体系
        </h2>
        <div class="row">
            <!-- KET备考 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div class="epgo-course-card" style="background:white; border-radius:12px; padding:40px 30px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; transition:all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); border-top:4px solid #2563EB; position:relative; overflow:hidden;" onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 12px 24px rgba(37,99,235,0.15)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)'">
                    <div style="font-size:56px; margin-bottom:20px; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.15) rotate(5deg)'" onmouseout="this.style.transform='scale(1) rotate(0)'">🎯</div>
                    <h3 style="font-size:24px; font-weight:700; margin:20px 0; color:#111827;">KET备考</h3>
                    <p style="color:#6B7280; line-height:1.8; margin-bottom:25px; font-size:15px;">
                        剑桥英语初级认证<br>
                        适合初中到高中学生<br>
                        全面覆盖听说读写<br>
                        从零基础到高分
                    </p>
                    <div style="display:flex; gap:8px; justify-content:center; flex-wrap:wrap;">
                        <a href="{$c.index_url}ket-exam/" class="btn btn-sm btn-primary" style="margin:5px; transition:all 0.3s;">真题解析</a>
                        <a href="{$c.index_url}ket-word/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">词汇速记</a>
                        <a href="{$c.index_url}ket-write/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">写作指导</a>
                        <a href="{$c.index_url}ket-listen/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">听力技巧</a>
                    </div>
                    <div style="position:absolute; top:0; left:0; width:100%; height:2px; background:linear-gradient(90deg, transparent, #2563EB, transparent); opacity:0; transition:opacity 0.3s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0'"></div>
                </div>
            </div>

            <!-- PET备考 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div class="epgo-course-card" style="background:white; border-radius:12px; padding:40px 30px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; transition:all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); border-top:4px solid #16A34A; position:relative; overflow:hidden;" onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 12px 24px rgba(22,163,74,0.15)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)'">
                    <div style="font-size:56px; margin-bottom:20px; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.15) rotate(-5deg)'" onmouseout="this.style.transform='scale(1) rotate(0)'">🚀</div>
                    <h3 style="font-size:24px; font-weight:700; margin:20px 0; color:#111827;">PET备考</h3>
                    <p style="color:#6B7280; line-height:1.8; margin-bottom:25px; font-size:15px;">
                        剑桥英语中级认证<br>
                        适合高中到大学学生<br>
                        国际认可资格证书<br>
                        提升竞争力必备
                    </p>
                    <div style="display:flex; gap:8px; justify-content:center; flex-wrap:wrap;">
                        <a href="{$c.index_url}pet-exam/" class="btn btn-sm btn-primary" style="margin:5px; transition:all 0.3s;">真题解析</a>
                        <a href="{$c.index_url}pet-word/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">词汇速记</a>
                        <a href="{$c.index_url}pet-write/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">写作指导</a>
                        <a href="{$c.index_url}pet-read/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">阅读技巧</a>
                    </div>
                    <div style="position:absolute; top:0; left:0; width:100%; height:2px; background:linear-gradient(90deg, transparent, #16A34A, transparent); opacity:0; transition:opacity 0.3s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0'"></div>
                </div>
            </div>

            <!-- 其他课程 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div class="epgo-course-card" style="background:white; border-radius:12px; padding:40px 30px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; transition:all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); border-top:4px solid #EA580C; position:relative; overflow:hidden;" onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 12px 24px rgba(234,88,12,0.15)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)'">
                    <div style="font-size:56px; margin-bottom:20px; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.15) rotate(5deg)'" onmouseout="this.style.transform='scale(1) rotate(0)'">📚</div>
                    <h3 style="font-size:24px; font-weight:700; margin:20px 0; color:#111827;">通用英语</h3>
                    <p style="color:#6B7280; line-height:1.8; margin-bottom:25px; font-size:15px;">
                        日常英语学习<br>
                        包括阅读演讲等<br>
                        提升英语综合能力<br>
                        适合各个年龄
                    </p>
                    <div style="display:flex; gap:8px; justify-content:center; flex-wrap:wrap;">
                        <a href="{$c.index_url}reading/" class="btn btn-sm btn-primary" style="margin:5px; transition:all 0.3s;">英语阅读</a>
                        <a href="{$c.index_url}speech/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">演讲训练</a>
                        <a href="{$c.index_url}daily/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">每日英语</a>
                        <a href="{$c.index_url}download/" class="btn btn-sm btn-default" style="margin:5px; transition:all 0.3s;">资料下载</a>
                    </div>
                    <div style="position:absolute; top:0; left:0; width:100%; height:2px; background:linear-gradient(90deg, transparent, #EA580C, transparent); opacity:0; transition:opacity 0.3s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0'"></div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- 最新文章推荐 -->
<section style="padding:80px 0; background:linear-gradient(180deg, #fafbfc 0%, #f3f4f6 100%);">
    <div class="container">
        <div style="text-align:center; margin-bottom:60px;">
            <h2 style="font-size:40px; font-weight:800; color:#111827; margin:0 0 16px;">
                最新学习资源
            </h2>
            <p style="font-size:16px; color:#6b7280; margin:0;">
                精选最新的英语学习内容，助力考试备考
            </p>
        </div>
        <div class="row">
            <tag action='list' type='news' num='12'>
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div class="epgo-article-card" style="background:white; border-radius:12px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.08); transition:all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); transform:translateY(0); border:1px solid #E5E7EB;" onmouseover="this.style.transform='translateY(-6px)'; this.style.boxShadow='0 12px 24px rgba(0,0,0,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 4px rgba(0,0,0,0.08)'">
                    <if value="$v['imgurl']">
                    <div style="height:200px; overflow:hidden; position:relative; background:#F3F4F6;">
                        <a href="{$v.url}" title="{$v.title}" {$g.urlnew} style="display:block; width:100%; height:100%;">
                            <img src="{$v.imgurl|thumb:400,200}" alt="{$v.title}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.4s ease; display:block;">
                        </a>
                        <div style="position:absolute; top:0; left:0; right:0; bottom:0; background:linear-gradient(135deg, rgba(37,99,235,0.1) 0%, rgba(37,99,235,0) 100%); opacity:0; transition:opacity 0.3s;" onmouseover="this.parentElement.style.opacity='1'" onmouseout="this.parentElement.style.opacity='0'"></div>
                    </div>
                    <else/>
                    <div style="height:200px; background:linear-gradient(135deg, #E5E7EB 0%, #D1D5DB 100%); display:flex; align-items:center; justify-content:center;">
                        <span style="color:#9CA3AF; font-size:14px;">📄 图片加载中</span>
                    </div>
                    </if>
                    <div style="padding:20px;">
                        <div style="font-size:11px; color:#2563EB; font-weight:700; margin-bottom:10px; text-transform:uppercase; letter-spacing:1px;">
                            📌 {$v.issue}
                        </div>
                        <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px 0; line-height:1.4; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                            <a href="{$v.url}" title="{$v.title}" style="color:inherit; text-decoration:none; transition:color 0.3s;" onmouseover="this.style.color='#2563EB'" onmouseout="this.style.color='inherit'" {$g.urlnew}>
                                {$v.title}
                            </a>
                        </h3>
                        <p style="color:#6B7280; font-size:13px; line-height:1.6; margin:0 0 15px 0; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                            {$v.description}
                        </p>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:#9CA3AF; padding-top:12px; border-top:1px solid #f3f4f6;">
                            <span>📅 {$v.updatetime}</span>
                            <span style="background:#f0fdf4; color:#16a34a; padding:2px 8px; border-radius:4px;"><i class="icon wb-eye" style="margin-right:4px;"></i>{$v.hits}</span>
                        </div>
                    </div>
                </div>
            </div>
            </tag>
        </div>
        <div style="text-align:center; margin-top:40px;">
            <a href="{$c.index_url}news/" class="btn btn-lg" style="background:#2563EB; color:white; font-weight:700; border-radius:8px; padding:14px 32px; text-decoration:none; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.3)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                查看全部文章 →
            </a>
        </div>
    </div>
</section>

<!-- 英文演讲推荐 -->
<section style="padding:80px 0; background:white; border-top:1px solid #e5e7eb;">
    <div class="container">
        <div style="text-align:center; margin-bottom:60px;">
            <h2 style="font-size:40px; font-weight:800; color:#111827; margin:0 0 16px;">
                精选英文演讲
            </h2>
            <p style="font-size:16px; color:#6b7280; margin:0;">
                世界名人演讲精选 · 提升听力和口语表达
            </p>
        </div>
        <div class="row">
            <!-- 演讲卡片1 - TED：What makes a good life -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:#f9fafb; border-radius:12px; overflow:hidden; border:1px solid #e5e7eb; transition:all 0.3s;" onmouseover="this.style.boxShadow='0 8px 24px rgba(37,99,235,0.12)'; this.style.transform='translateY(-4px)'" onmouseout="this.style.boxShadow='none'; this.style.transform='translateY(0)'">
                    <div style="position:relative; padding-top:56.25%; background:#000; overflow:hidden;">
                        <iframe src="//player.bilibili.com/player.html?bvid=BV1GW411Q7FX&page=1&high_quality=1&danmaku=0&autoplay=0"
                            style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
                            scrolling="no" frameborder="0" allowfullscreen="true"></iframe>
                    </div>
                    <div style="padding:20px;">
                        <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px;">TED：什么让生活变得美好</h3>
                        <p style="font-size:13px; color:#6b7280; margin:0 0 15px; line-height:1.6;">
                            哈佛大学75年研究揭示幸福的秘密，学习地道英语表达
                        </p>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:#9ca3af;">
                            <span><i class="icon wb-clock" style="margin-right:4px;"></i>12分钟</span>
                            <a href="{$c.index_url}speech/" style="color:#2563eb; text-decoration:none; font-weight:600;">更多演讲 →</a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 演讲卡片2 - 乔布斯斯坦福演讲 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:#f9fafb; border-radius:12px; overflow:hidden; border:1px solid #e5e7eb; transition:all 0.3s;" onmouseover="this.style.boxShadow='0 8px 24px rgba(37,99,235,0.12)'; this.style.transform='translateY(-4px)'" onmouseout="this.style.boxShadow='none'; this.style.transform='translateY(0)'">
                    <div style="position:relative; padding-top:56.25%; background:#000; overflow:hidden;">
                        <iframe src="//player.bilibili.com/player.html?bvid=BV1Ks411k7Ha&page=1&high_quality=1&danmaku=0&autoplay=0"
                            style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
                            scrolling="no" frameborder="0" allowfullscreen="true"></iframe>
                    </div>
                    <div style="padding:20px;">
                        <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px;">乔布斯斯坦福毕业演讲</h3>
                        <p style="font-size:13px; color:#6b7280; margin:0 0 15px; line-height:1.6;">
                            经典英文演讲，感受原版英语的力量与魅力
                        </p>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:#9ca3af;">
                            <span><i class="icon wb-clock" style="margin-right:4px;"></i>15分钟</span>
                            <a href="{$c.index_url}speech/" style="color:#16a34a; text-decoration:none; font-weight:600;">更多演讲 →</a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 演讲卡片3 - BBC英语 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:#f9fafb; border-radius:12px; overflow:hidden; border:1px solid #e5e7eb; transition:all 0.3s;" onmouseover="this.style.boxShadow='0 8px 24px rgba(37,99,235,0.12)'; this.style.transform='translateY(-4px)'" onmouseout="this.style.boxShadow='none'; this.style.transform='translateY(0)'">
                    <div style="position:relative; padding-top:56.25%; background:#000; overflow:hidden;">
                        <iframe src="//player.bilibili.com/player.html?bvid=BV1vb411n7nk&page=1&high_quality=1&danmaku=0&autoplay=0"
                            style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
                            scrolling="no" frameborder="0" allowfullscreen="true"></iframe>
                    </div>
                    <div style="padding:20px;">
                        <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px;">BBC 6 Minute English 合集</h3>
                        <p style="font-size:13px; color:#6b7280; margin:0 0 15px; line-height:1.6;">
                            BBC经典英语节目，每集6分钟学一个话题
                        </p>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:#9ca3af;">
                            <span><i class="icon wb-clock" style="margin-right:4px;"></i>6分钟</span>
                            <a href="{$c.index_url}speech/" style="color:#ea580c; text-decoration:none; font-weight:600;">更多演讲 →</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="text-align:center; margin-top:40px;">
            <a href="{$c.index_url}speech/" class="btn btn-lg" style="background:#ea580c; color:white; font-weight:700; border-radius:8px; padding:14px 32px; text-decoration:none; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 16px rgba(234,88,12,0.3)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                查看全部演讲 →
            </a>
        </div>
    </div>
</section>

<!-- 学员评价 - 大幅增加评论 -->
<section style="padding:60px 0; background:#EFF6FF;">
    <div class="container">
        <h2 style="font-size:36px; font-weight:700; text-align:center; color:#111827; margin:0 0 50px 0;">
            学员评价与反馈
        </h2>
        <div class="row">
            <!-- 评价1 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); border-left:4px solid #FDB022;">
                    <div style="color:#FDB022; margin-bottom:15px; font-size:18px;">★★★★★</div>
                    <p style="color:#6B7280; font-style:italic; margin-bottom:20px; line-height:1.8; font-size:15px;">
                        "非常棒的平台！KET课程讲得特别清楚，我从基础开始学，现在已经通过考试了。老师非常耐心，课后有任何问题都能及时回答。"
                    </p>
                    <div>
                        <div style="font-weight:700; color:#111827;">李同学</div>
                        <div style="font-size:13px; color:#9CA3AF;">北京 · KET高分通过 · 2026年3月</div>
                    </div>
                </div>
            </div>

            <!-- 评价2 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); border-left:4px solid #16A34A;">
                    <div style="color:#FDB022; margin-bottom:15px; font-size:18px;">★★★★★</div>
                    <p style="color:#6B7280; font-style:italic; margin-bottom:20px; line-height:1.8; font-size:15px;">
                        "PET备考课程非常系统，从词汇到写作都有详细讲解。真题解析部分让我掌握了出题规律，考试时信心十足！"
                    </p>
                    <div>
                        <div style="font-weight:700; color:#111827;">王同学</div>
                        <div style="font-size:13px; color:#9CA3AF;">上海 · PET高分通过 · 2026年2月</div>
                    </div>
                </div>
            </div>

            <!-- 评价3 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); border-left:4px solid #2563EB;">
                    <div style="color:#FDB022; margin-bottom:15px; font-size:18px;">★★★★★</div>
                    <p style="color:#6B7280; font-style:italic; margin-bottom:20px; line-height:1.8; font-size:15px;">
                        "课程安排特别合理，循序渐进。听力、阅读、写作都学到了实用技巧。比报线下班便宜多了，而且可以随时复习！"
                    </p>
                    <div>
                        <div style="font-weight:700; color:#111827;">陈同学</div>
                        <div style="font-size:13px; color:#9CA3AF;">广州 · KET通过 · 2026年1月</div>
                    </div>
                </div>
            </div>

            <!-- 评价4 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); border-left:4px solid #EA580C;">
                    <div style="color:#FDB022; margin-bottom:15px; font-size:18px;">★★★★★</div>
                    <p style="color:#6B7280; font-style:italic; margin-bottom:20px; line-height:1.8; font-size:15px;">
                        "最喜欢词汇速记部分，用各种方法帮我们记单词，再也不用死记硬背了。加油！推荐所有备考的同学来学！"
                    </p>
                    <div>
                        <div style="font-weight:700; color:#111827;">张同学</div>
                        <div style="font-size:13px; color:#9CA3AF;">深圳 · KET词汇高分 · 2026年3月</div>
                    </div>
                </div>
            </div>

            <!-- 评价5 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); border-left:4px solid #2563EB;">
                    <div style="color:#FDB022; margin-bottom:15px; font-size:18px;">★★★★★</div>
                    <p style="color:#6B7280; font-style:italic; margin-bottom:20px; line-height:1.8; font-size:15px;">
                        "老师讲课很细致，每个考点都讲到。特别是写作指导部分，让我的作文从及格线冲到了高分。现在正在准备FCE！"
                    </p>
                    <div>
                        <div style="font-weight:700; color:#111827;">刘同学</div>
                        <div style="font-size:13px; color:#9CA3AF;">杭州 · PET作文95+ · 2026年1月</div>
                    </div>
                </div>
            </div>

            <!-- 评价6 -->
            <div class="col-lg-4 col-md-6 col-xs-12" style="margin-bottom:30px;">
                <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05); border-left:4px solid #16A34A;">
                    <div style="color:#FDB022; margin-bottom:15px; font-size:18px;">★★★★★</div>
                    <p style="color:#6B7280; font-style:italic; margin-bottom:20px; line-height:1.8; font-size:15px;">
                        "物超所值！不仅学到了考试内容，还学到了实用的英语技能。现在我可以流畅地和外国友人交流，感谢陪跑GO！"
                    </p>
                    <div>
                        <div style="font-weight:700; color:#111827;">林同学</div>
                        <div style="font-size:13px; color:#9CA3AF;">福州 · PET高分+口语提升 · 2026年2月</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- 常见问题 -->
<section style="padding:60px 0; background:white;">
    <div class="container">
        <h2 style="font-size:36px; font-weight:700; text-align:center; color:#111827; margin:0 0 50px 0;">
            常见问题解答
        </h2>
        <div style="max-width:800px; margin:0 auto;">
            <div style="margin-bottom:25px;">
                <h4 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px 0; cursor:pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none';">
                    <i class="icon wb-plus" style="margin-right:8px;"></i> KET和PET有什么区别？
                </h4>
                <p style="color:#6B7280; line-height:1.8; margin:0; display:none;">
                    KET（初级）适合初中到高中学生，难度相对较低。PET（中级）适合高中到大学学生，是KET的进阶版本。我们提供两个级别的完整课程，你可以根据自己的英语水平选择。
                </p>
            </div>
            <div style="margin-bottom:25px;">
                <h4 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px 0; cursor:pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none';">
                    <i class="icon wb-plus" style="margin-right:8px;"></i> 课程有效期是多久？
                </h4>
                <p style="color:#6B7280; line-height:1.8; margin:0; display:none;">
                    课程为永久有效，你可以随时学习、复习内容。我们会定期更新课程内容，确保你学到最新的考试信息和技巧。
                </p>
            </div>
            <div style="margin-bottom:25px;">
                <h4 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px 0; cursor:pointer;" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none';">
                    <i class="icon wb-plus" style="margin-right:8px;"></i> 如果没通过考试怎么办？
                </h4>
                <p style="color:#6B7280; line-height:1.8; margin:0; display:none;">
                    我们有完善的反馈机制。如果你学习了我们的全部课程还没通过，可以联系我们获得额外的指导和支持。我们的目标就是帮助你成功通过考试！
                </p>
            </div>
        </div>
    </div>
</section>

<!-- 二维码弹窗 -->
<div id="epgo-qr-modal">
    <div class="epgo-modal-box">
        <button class="epgo-modal-close" onclick="epgoCloseQR()">×</button>
        <h3>英语陪跑GO</h3>
        <p class="epgo-modal-sub">扫码关注，每天备考干货</p>
        <div class="epgo-modal-qr">
            <if value="$c['footinfo_wx']">
                <img src="{$c.footinfo_wx|thumb:170,170}" alt="公众号二维码">
            <else/>
                <div style="width:170px;height:170px;display:flex;align-items:center;justify-content:center;color:#9CA3AF;font-size:13px;">二维码配置中</div>
            </if>
        </div>
        <p class="epgo-modal-hint">长按识别二维码关注</p>
    </div>
</div>

<script>
(function(){
    var scrollY = 0;
    function show(){
        scrollY = window.scrollY;
        document.body.style.overflow = 'hidden';
        document.getElementById('epgo-qr-modal').style.display='flex';
        document.querySelector('header').style.position = 'fixed';
    }
    function hide(){
        document.body.style.overflow = 'auto';
        window.scrollTo(0, scrollY);
        document.getElementById('epgo-qr-modal').style.display='none';
        document.querySelector('header').style.position = 'relative';
    }
    window.epgoShowQR = show;
    window.epgoCloseQR = hide;
})();
</script>

<include file="foot.php" />
