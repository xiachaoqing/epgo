<?php defined('IN_MET') or exit('No permission');
$data['page_title'] = '联系我们｜英语陪跑GO';
$data['page_description'] = '联系英语陪跑GO，咨询 KET/PET 学习内容、入学测评、学习工具和陪跑 App 服务。';
$data['page_keywords'] = '英语陪跑GO,联系我们,KET,PET,英语学习';
?>
<include file="head.php" />
<section class="met-feedback animsition" m-id="feedback" m-type='noset'>
    <div class="container">
        <div class="row">
            <div class="met-feedback-body">
                <div class="epgo-feedback-intro">
                    <h1>联系我们</h1>
                    <p>如果你需要了解 KET/PET 学习内容、入学测评、学习工具或英语陪跑GO App，可以通过电话或公众号联系我们，我们会根据内容回复。</p>
                    <p class="epgo-feedback-note">服务时间：周一至周日 08:00–20:00 · 电话：<a href="tel:17610721765">17610721765</a> · <a href="/#follow">关注公众号</a></p>
                </div>
                <tag action='feedback.form'></tag>
                </div>
        </div>
    </div>
</section>
<style>
.epgo-feedback-intro{max-width:760px;margin:0 auto 28px;padding:28px 30px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;}
.epgo-feedback-intro h1{margin:0 0 10px;color:#15356F;font-size:28px;}
.epgo-feedback-intro p{margin:0 0 10px;color:#52627A;line-height:1.8;font-size:14px;}
.epgo-feedback-intro .epgo-feedback-note{margin-bottom:0;color:#64748B;font-size:13px;}
.epgo-feedback-intro a{color:#1565C0;}
@media(max-width:767px){.epgo-feedback-intro{margin:0 10px 20px;padding:20px;}.epgo-feedback-intro h1{font-size:24px;}}
</style>
<include file="foot.php" />
