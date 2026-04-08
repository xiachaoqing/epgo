<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />

<!-- 内页顶部标题栏 -->
<div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);padding:40px 0 36px;text-align:center;">
    <div class="container">
        <h1 style="font-size:28px;font-weight:800;color:white;margin:0 0 8px;">{$data.title}</h1>
        <!-- 面包屑 -->
        <div style="font-size:13px;color:rgba(255,255,255,.7);">
            <a href="/" style="color:rgba(255,255,255,.7);text-decoration:none;">首页</a>
            <span style="margin:0 8px;">›</span>
            <span style="color:white;">{$data.title}</span>
        </div>
    </div>
</div>

<section style="background:#F9FAFB;padding:40px 0 60px;min-height:400px;">
    <div class="container">
        <div style="max-width:860px;margin:0 auto;background:white;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.07);padding:40px;">
            <div class="met-editor epgo-show-content">
                {$data.content}
            </div>

            <if value="$data['class1'] eq 107 || $data['title'] eq '关于我们' || strstr($data['title'],'英语陪跑GO')">
            <div class="epgo-about-extra">
                <div class="epgo-about-grid">
                    <div class="epgo-about-card">
                        <h3>平台定位</h3>
                        <p>英语陪跑GO 聚焦 KET、PET、FCE 等剑桥英语考试，围绕词汇、阅读、写作、听力与真题解析，提供长期、系统、可执行的学习内容。</p>
                    </div>
                    <div class="epgo-about-card">
                        <h3>适合人群</h3>
                        <p>适合准备剑桥英语考试的学生、希望提升英语综合能力的学习者，以及需要清晰学习路径和日常练习内容的家长与老师。</p>
                    </div>
                    <div class="epgo-about-card">
                        <h3>内容体系</h3>
                        <p>平台涵盖 KET / PET 备考、英语阅读、英语演讲、每日英语与资料下载，帮助学习者在考试与实际应用之间建立稳定提升路径。</p>
                    </div>
                    <div class="epgo-about-card">
                        <h3>学习方式</h3>
                        <p>从高频词汇积累、真题精讲、写作模板，到每日练习和资料整理，我们坚持“小步积累、持续进步”的内容设计方式。</p>
                    </div>
                </div>

                <div class="epgo-about-path">
                    <h3>推荐学习路径</h3>
                    <div class="epgo-about-steps">
                        <div class="step"><span>1</span><strong>词汇打基础</strong><p>先用高频词汇与固定搭配构建基本输入。</p></div>
                        <div class="step"><span>2</span><strong>真题抓重点</strong><p>通过真题解析建立题型意识与答题框架。</p></div>
                        <div class="step"><span>3</span><strong>写作与表达</strong><p>积累句型模板，提高写作与口语组织能力。</p></div>
                        <div class="step"><span>4</span><strong>每日持续输入</strong><p>通过每日英语与阅读内容维持学习节奏。</p></div>
                    </div>
                </div>

                <div class="epgo-about-cta">
                    <a href="/ket/" class="btn-main">进入 KET 备考</a>
                    <a href="/pet/" class="btn-sub">进入 PET 备考</a>
                    <a href="/reading/" class="btn-sub">浏览最新文章</a>
                </div>
            </div>
            </if>
        </div>
    </div>
</section>

<style>
.epgo-show-content{line-height:1.9;font-size:15px;color:#374151;}
.epgo-show-content h1,.epgo-show-content h2,.epgo-show-content h3{color:#111827;font-weight:700;margin-top:2em;margin-bottom:.8em;}
.epgo-show-content h2{font-size:22px;}
.epgo-show-content h3{font-size:18px;}
.epgo-show-content p{margin-bottom:1.2em;}
.epgo-show-content img{max-width:100%;border-radius:8px;}
.epgo-show-content a{color:#2563EB;}
.epgo-show-content ul,.epgo-show-content ol{padding-left:24px;margin-bottom:1.2em;}
.epgo-show-content li{margin-bottom:.5em;}
.epgo-show-content blockquote{border-left:4px solid #2563EB;padding:12px 20px;background:#EFF6FF;border-radius:0 8px 8px 0;margin:1.5em 0;color:#1e40af;}
.epgo-about-extra{margin-top:36px;padding-top:28px;border-top:1px solid #E5E7EB;}
.epgo-about-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-bottom:28px;}
.epgo-about-card{background:#F8FAFC;border:1px solid #E5E7EB;border-radius:12px;padding:20px;}
.epgo-about-card h3{margin:0 0 10px;font-size:18px;color:#111827;}
.epgo-about-card p{margin:0;color:#6B7280;font-size:14px;line-height:1.8;}
.epgo-about-path{background:linear-gradient(135deg,#EFF6FF,#F8FAFC);border-radius:14px;padding:24px;margin-bottom:24px;}
.epgo-about-path h3{margin:0 0 18px;font-size:20px;color:#111827;}
.epgo-about-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;}
.epgo-about-steps .step{background:white;border-radius:12px;padding:18px;border:1px solid #DBEAFE;}
.epgo-about-steps .step span{display:inline-flex;width:28px;height:28px;align-items:center;justify-content:center;background:#2563EB;color:white;border-radius:50%;font-size:13px;font-weight:700;margin-bottom:12px;}
.epgo-about-steps .step strong{display:block;font-size:15px;color:#111827;margin-bottom:8px;}
.epgo-about-steps .step p{margin:0;font-size:13px;color:#6B7280;line-height:1.7;}
.epgo-about-cta{display:flex;gap:12px;flex-wrap:wrap;}
.epgo-about-cta a{text-decoration:none;border-radius:10px;padding:11px 20px;font-size:14px;font-weight:700;}
.epgo-about-cta .btn-main{background:#2563EB;color:white;}
.epgo-about-cta .btn-sub{background:#EFF6FF;color:#2563EB;}
@media(max-width:767px){
  .epgo-show-content{font-size:14px;}
  section .container > div{padding:20px !important;}
  .epgo-about-grid{grid-template-columns:1fr;}
  .epgo-about-steps{grid-template-columns:1fr;}
}
</style>

<include file="foot.php" />