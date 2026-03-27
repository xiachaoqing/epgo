# 🎨 首页优化与模板改进计划

**优先级**: 🔴 高优先级
**预计时间**: 1.5小时
**目标**: 优化首页结构，增加内容吸引力，改善用户体验

---

## 📊 首页优化清单

### 1️⃣ 新增"最新学习资讯"区域

**位置**: 在"精选英文演讲"和"学员评价"之间
**内容**: 显示最新5篇文章

```html
<!-- 最新学习资讯区域 -->
<section style="padding:60px 0; background:#f9fafb; border-top:1px solid #e5e7eb;">
    <div class="container">
        <div style="text-align:center; margin-bottom:50px;">
            <h2 style="font-size:36px; font-weight:800; color:#111827; margin:0 0 16px;">
                📰 最新学习资讯
            </h2>
            <p style="font-size:16px; color:#6b7280; margin:0;">
                每周更新的学习资讯 · 了解考试动态 · 获取备考建议
            </p>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:24px;">

            <!-- 资讯卡片 1 -->
            <div style="background:white; border-radius:12px; overflow:hidden; border-left:4px solid #2563eb; box-shadow:0 1px 3px rgba(0,0,0,0.08); transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.08)'">
                <div style="padding:24px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                        <span style="background:#eff6ff; color:#2563eb; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700;">考试资讯</span>
                        <span style="font-size:12px; color:#9ca3af;">2026-03-21</span>
                    </div>
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px; line-height:1.5;">
                        2026年KET考试时间安排已发布
                    </h3>
                    <p style="font-size:14px; color:#6b7280; margin:0 0 16px; line-height:1.6;">
                        官方最新发布2026年全年的KET考试日期安排，包括报名截止时间和成绩公布时间...
                    </p>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:12px; color:#9ca3af;">
                            <i class="icon wb-eye" style="margin-right:4px;"></i>1.2K次浏览
                        </span>
                        <a href="#" style="color:#2563eb; text-decoration:none; font-weight:700; font-size:14px;">
                            查看详情 →
                        </a>
                    </div>
                </div>
            </div>

            <!-- 资讯卡片 2 -->
            <div style="background:white; border-radius:12px; overflow:hidden; border-left:4px solid #16a34a; box-shadow:0 1px 3px rgba(0,0,0,0.08); transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.08)'">
                <div style="padding:24px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                        <span style="background:#f0fdf4; color:#16a34a; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700;">学习技巧</span>
                        <span style="font-size:12px; color:#9ca3af;">2026-03-19</span>
                    </div>
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px; line-height:1.5;">
                        KET听力快速提分的5个秘诀
                    </h3>
                    <p style="font-size:14px; color:#6b7280; margin:0 0 16px; line-height:1.6;">
                        学习英语老师多年总结的听力提分技巧，这些方法已被数千名学生验证...
                    </p>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:12px; color:#9ca3af;">
                            <i class="icon wb-eye" style="margin-right:4px;"></i>2.8K次浏览
                        </span>
                        <a href="#" style="color:#16a34a; text-decoration:none; font-weight:700; font-size:14px;">
                            查看详情 →
                        </a>
                    </div>
                </div>
            </div>

            <!-- 资讯卡片 3 -->
            <div style="background:white; border-radius:12px; overflow:hidden; border-left:4px solid #ea580c; box-shadow:0 1px 3px rgba(0,0,0,0.08); transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.08)'">
                <div style="padding:24px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                        <span style="background:#fef3c7; color:#ea580c; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700;">学员故事</span>
                        <span style="font-size:12px; color:#9ca3af;">2026-03-17</span>
                    </div>
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px; line-height:1.5;">
                        初二学生3个月通过KET的学习经验分享
                    </h3>
                    <p style="font-size:14px; color:#6b7280; margin:0 0 16px; line-height:1.6;">
                        李同学用亲身经历详细讲述如何在3个月内从零基础通过KET考试...
                    </p>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:12px; color:#9ca3af;">
                            <i class="icon wb-eye" style="margin-right:4px;"></i>3.5K次浏览
                        </span>
                        <a href="#" style="color:#ea580c; text-decoration:none; font-weight:700; font-size:14px;">
                            查看详情 →
                        </a>
                    </div>
                </div>
            </div>

        </div>

        <div style="text-align:center; margin-top:40px;">
            <a href="{$c.index_url}news/" class="btn btn-lg" style="background:#2563eb; color:white; font-weight:700; border-radius:8px; padding:14px 32px; text-decoration:none; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.3)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                查看全部资讯 →
            </a>
        </div>
    </div>
</section>
```

---

### 2️⃣ 新增"热门下载资源"区域

**位置**: 在"学员评价"之后
**内容**: 显示最热门的5个资源

```html
<!-- 热门下载资源区域 -->
<section style="padding:60px 0; background:white; border-top:1px solid #e5e7eb;">
    <div class="container">
        <div style="text-align:center; margin-bottom:50px;">
            <h2 style="font-size:36px; font-weight:800; color:#111827; margin:0 0 16px;">
                📥 热门下载资源
            </h2>
            <p style="font-size:16px; color:#6b7280; margin:0;">
                精选教学资料 · 免费下载 · 提升学习效率
            </p>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:20px;">

            <!-- 资源卡片 1 -->
            <div style="background:#f9fafb; border-radius:12px; padding:24px; border:1px solid #e5e7eb; text-align:center; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                <div style="font-size:48px; margin-bottom:16px;">📄</div>
                <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px;">KET备考完全指南</h3>
                <p style="font-size:13px; color:#6b7280; margin:0 0 16px; line-height:1.6;">
                    系统介绍KET考试、题型分析、高分策略
                </p>
                <div style="background:white; padding:12px; border-radius:8px; margin-bottom:16px; font-size:12px; color:#9ca3af;">
                    <div style="margin-bottom:6px;">📊 5.2MB · 80页</div>
                    <div>⬇️ 1240次下载</div>
                </div>
                <a href="#" class="btn btn-sm btn-primary" style="width:100%; background:#2563eb; color:white; border:none; padding:10px; border-radius:6px; text-decoration:none; cursor:pointer;">
                    立即下载
                </a>
            </div>

            <!-- 资源卡片 2 -->
            <div style="background:#f9fafb; border-radius:12px; padding:24px; border:1px solid #e5e7eb; text-align:center; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                <div style="font-size:48px; margin-bottom:16px;">📚</div>
                <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px;">KET核心词汇表（1500词）</h3>
                <p style="font-size:13px; color:#6b7280; margin:0 0 16px; line-height:1.6;">
                    包含音标、例句、同义词、发音
                </p>
                <div style="background:white; padding:12px; border-radius:8px; margin-bottom:16px; font-size:12px; color:#9ca3af;">
                    <div style="margin-bottom:6px;">📊 3.5MB · Excel+PDF</div>
                    <div>⬇️ 3280次下载</div>
                </div>
                <a href="#" class="btn btn-sm btn-primary" style="width:100%; background:#2563eb; color:white; border:none; padding:10px; border-radius:6px; text-decoration:none; cursor:pointer;">
                    立即下载
                </a>
            </div>

            <!-- 资源卡片 3 -->
            <div style="background:#f9fafb; border-radius:12px; padding:24px; border:1px solid #e5e7eb; text-align:center; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                <div style="font-size:48px; margin-bottom:16px;">✍️</div>
                <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px;">写作范文精选（50篇）</h3>
                <p style="font-size:13px; color:#6b7280; margin:0 0 16px; line-height:1.6;">
                    各题材范文、详细分析、高分点讲解
                </p>
                <div style="background:white; padding:12px; border-radius:8px; margin-bottom:16px; font-size:12px; color:#9ca3af;">
                    <div style="margin-bottom:6px;">📊 4.9MB · PDF+Word</div>
                    <div>⬇️ 2560次下载</div>
                </div>
                <a href="#" class="btn btn-sm btn-primary" style="width:100%; background:#2563eb; color:white; border:none; padding:10px; border-radius:6px; text-decoration:none; cursor:pointer;">
                    立即下载
                </a>
            </div>

            <!-- 资源卡片 4 -->
            <div style="background:#f9fafb; border-radius:12px; padding:24px; border:1px solid #e5e7eb; text-align:center; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                <div style="font-size:48px; margin-bottom:16px;">🎧</div>
                <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px;">听力技巧秘籍</h3>
                <p style="font-size:13px; color:#6b7280; margin:0 0 16px; line-height:1.6;">
                    题型分析、技巧讲解、30个音频示范
                </p>
                <div style="background:white; padding:12px; border-radius:8px; margin-bottom:16px; font-size:12px; color:#9ca3af;">
                    <div style="margin-bottom:6px;">📊 8.5MB · PDF+音频</div>
                    <div>⬇️ 2890次下载</div>
                </div>
                <a href="#" class="btn btn-sm btn-primary" style="width:100%; background:#2563eb; color:white; border:none; padding:10px; border-radius:6px; text-decoration:none; cursor:pointer;">
                    立即下载
                </a>
            </div>

            <!-- 资源卡片 5 -->
            <div style="background:#f9fafb; border-radius:12px; padding:24px; border:1px solid #e5e7eb; text-align:center; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(37,99,235,0.12)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                <div style="font-size:48px; margin-bottom:16px;">📋</div>
                <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0 0 12px;">KET模拟试卷（5套）</h3>
                <p style="font-size:13px; color:#6b7280; margin:0 0 16px; line-height:1.6;">
                    5套完整模拟卷、详细答案、答题解析
                </p>
                <div style="background:white; padding:12px; border-radius:8px; margin-bottom:16px; font-size:12px; color:#9ca3af;">
                    <div style="margin-bottom:6px;">📊 7.2MB · PDF</div>
                    <div>⬇️ 3450次下载</div>
                </div>
                <a href="#" class="btn btn-sm btn-primary" style="width:100%; background:#2563eb; color:white; border:none; padding:10px; border-radius:6px; text-decoration:none; cursor:pointer;">
                    立即下载
                </a>
            </div>

        </div>

        <div style="text-align:center; margin-top:40px;">
            <a href="{$c.index_url}download/" class="btn btn-lg" style="background:#16a34a; color:white; font-weight:700; border-radius:8px; padding:14px 32px; text-decoration:none; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 16px rgba(22,163,74,0.3)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                查看全部资源 →
            </a>
        </div>
    </div>
</section>
```

---

### 3️⃣ 新增"常见问题"(FAQ)区域

**位置**: 在页脚之前
**内容**: 6-8个常见问题的展开收起式设计

```html
<!-- 常见问题区域 -->
<section style="padding:60px 0; background:#f9fafb; border-top:1px solid #e5e7eb;">
    <div class="container" style="max-width:700px;">
        <div style="text-align:center; margin-bottom:50px;">
            <h2 style="font-size:36px; font-weight:800; color:#111827; margin:0 0 16px;">
                ❓ 常见问题解答
            </h2>
            <p style="font-size:16px; color:#6b7280; margin:0;">
                快速找到您想了解的问题答案
            </p>
        </div>

        <!-- FAQ 展开收起组件 -->
        <div style="display:flex; flex-direction:column; gap:16px;">

            <!-- FAQ Item 1 -->
            <div style="background:white; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden;">
                <div style="padding:20px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:#f9fafb;" onclick="this.parentElement.querySelector('.faq-answer').style.display = this.parentElement.querySelector('.faq-answer').style.display === 'none' ? 'block' : 'none'; this.querySelector('.toggle-icon').style.transform = this.querySelector('.toggle-icon').style.transform === 'rotate(0deg)' ? 'rotate(180deg)' : 'rotate(0deg)'">
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0;">KET和PET有什么区别？</h3>
                    <span class="toggle-icon" style="font-size:20px; transition:transform 0.3s; transform:rotate(0deg);">▼</span>
                </div>
                <div class="faq-answer" style="padding:20px; display:none; background:white;">
                    <p style="color:#6b7280; line-height:1.8; margin:0;">
                        <strong>KET (Key English Test)</strong> 是剑桥通用英语等级考试中的初级水平，适合初中学生；
                        <strong>PET (Preliminary English Test)</strong> 是中级水平，适合有一定英语基础的学生。
                        PET的难度和词汇量都比KET要高。
                    </p>
                </div>
            </div>

            <!-- FAQ Item 2 -->
            <div style="background:white; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden;">
                <div style="padding:20px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:#f9fafb;" onclick="this.parentElement.querySelector('.faq-answer').style.display = this.parentElement.querySelector('.faq-answer').style.display === 'none' ? 'block' : 'none'; this.querySelector('.toggle-icon').style.transform = this.querySelector('.toggle-icon').style.transform === 'rotate(0deg)' ? 'rotate(180deg)' : 'rotate(0deg)'">
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0;">EPGO的课程需要多长时间完成？</h3>
                    <span class="toggle-icon" style="font-size:20px; transition:transform 0.3s; transform:rotate(0deg);">▼</span>
                </div>
                <div class="faq-answer" style="padding:20px; display:none; background:white;">
                    <p style="color:#6b7280; line-height:1.8; margin:0;">
                        根据学生的英语基础不同，完成时间也不同。通常来说：
                        <br/>• 零基础学生：3-6个月完成KET课程
                        <br/>• 基础一般学生：2-3个月完成KET课程
                        <br/>• PET课程：4-6个月
                        <br/>课程可以灵活安排，学生可以根据自己的进度调整学习速度。
                    </p>
                </div>
            </div>

            <!-- FAQ Item 3 -->
            <div style="background:white; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden;">
                <div style="padding:20px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:#f9fafb;" onclick="this.parentElement.querySelector('.faq-answer').style.display = this.parentElement.querySelector('.faq-answer').style.display === 'none' ? 'block' : 'none'; this.querySelector('.toggle-icon').style.transform = this.querySelector('.toggle-icon').style.transform === 'rotate(0deg)' ? 'rotate(180deg)' : 'rotate(0deg)'">
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0;">有免费试听课程吗？</h3>
                    <span class="toggle-icon" style="font-size:20px; transition:transform 0.3s; transform:rotate(0deg);">▼</span>
                </div>
                <div class="faq-answer" style="padding:20px; display:none; background:white;">
                    <p style="color:#6b7280; line-height:1.8; margin:0;">
                        有的！每位新学员都可以获得1节（50分钟）的免费试听课程。
                        <br/>通过试听课，您可以：
                        <br/>• 了解我们的教学风格
                        <br/>• 体验真实的课堂氛围
                        <br/>• 获得个性化的学习评估
                        <br/>联系客服预约即可。
                    </p>
                </div>
            </div>

            <!-- FAQ Item 4 -->
            <div style="background:white; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden;">
                <div style="padding:20px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:#f9fafb;" onclick="this.parentElement.querySelector('.faq-answer').style.display = this.parentElement.querySelector('.faq-answer').style.display === 'none' ? 'block' : 'none'; this.querySelector('.toggle-icon').style.transform = this.querySelector('.toggle-icon').style.transform === 'rotate(0deg)' ? 'rotate(180deg)' : 'rotate(0deg)'">
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0;">EPGO的通过率真的这么高吗？</h3>
                    <span class="toggle-icon" style="font-size:20px; transition:transform 0.3s; transform:rotate(0deg);">▼</span>
                </div>
                <div class="faq-answer" style="padding:20px; display:none; background:white;">
                    <p style="color:#6b7280; line-height:1.8; margin:0;">
                        我们的98%首次通过率是基于真实学员数据统计的。这个高通过率源于：
                        <br/>• 专业的师资团队和科学的教学方法
                        <br/>• 个性化的学习方案和完整的课程体系
                        <br/>• 贴心的课后支持和答疑服务
                        <br/>• 学生的自律和坚持
                        <br/>当然，学生的主动配合也很重要！
                    </p>
                </div>
            </div>

            <!-- FAQ Item 5 -->
            <div style="background:white; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden;">
                <div style="padding:20px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:#f9fafb;" onclick="this.parentElement.querySelector('.faq-answer').style.display = this.parentElement.querySelector('.faq-answer').style.display === 'none' ? 'block' : 'none'; this.querySelector('.toggle-icon').style.transform = this.querySelector('.toggle-icon').style.transform === 'rotate(0deg)' ? 'rotate(180deg)' : 'rotate(0deg)'">
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0;">如果不满意可以退款吗？</h3>
                    <span class="toggle-icon" style="font-size:20px; transition:transform 0.3s; transform:rotate(0deg);">▼</span>
                </div>
                <div class="faq-answer" style="padding:20px; display:none; background:white;">
                    <p style="color:#6b7280; line-height:1.8; margin:0;">
                        可以的。如果您在学习过程中不满意我们的服务，可以在7天内无条件申请退款。
                        <br/>这是我们对教学质量的承诺。我们相信通过EPGO的学习，您一定能看到明显的进步。
                    </p>
                </div>
            </div>

            <!-- FAQ Item 6 -->
            <div style="background:white; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden;">
                <div style="padding:20px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:#f9fafb;" onclick="this.parentElement.querySelector('.faq-answer').style.display = this.parentElement.querySelector('.faq-answer').style.display === 'none' ? 'block' : 'none'; this.querySelector('.toggle-icon').style.transform = this.querySelector('.toggle-icon').style.transform === 'rotate(0deg)' ? 'rotate(180deg)' : 'rotate(0deg)'">
                    <h3 style="font-size:16px; font-weight:700; color:#111827; margin:0;">如何报名参加课程？</h3>
                    <span class="toggle-icon" style="font-size:20px; transition:transform 0.3s; transform:rotate(0deg);">▼</span>
                </div>
                <div class="faq-answer" style="padding:20px; display:none; background:white;">
                    <p style="color:#6b7280; line-height:1.8; margin:0;">
                        报名很简单：
                        <br/>1. 点击网站上的"立即报名"按钮
                        <br/>2. 填写基本信息和英语基础评估
                        <br/>3. 选择合适的课程套餐
                        <br/>4. 完成支付
                        <br/>5. 预约试听课或正式课程
                        <br/>您也可以直接联系客服，我们会为您一步步指导。
                    </p>
                </div>
            </div>

        </div>

        <div style="text-align:center; margin-top:40px;">
            <p style="color:#6b7280; margin:0;">
                还有其他问题？
                <a href="#" style="color:#2563eb; text-decoration:none; font-weight:700;">
                    联系客服 →
                </a>
            </p>
        </div>
    </div>
</section>
```

---

## 🎨 CSS样式改进建议

### 1. 颜色搭配优化

```css
/* 保持当前配色不变，但优化饱和度 */
--epgo-blue:     #2563EB;    /* 主色 - 稳重蓝 */
--epgo-green:    #16A34A;    /* 成功色 - 明亮绿 */
--epgo-orange:   #EA580C;    /* 警告色 - 温暖橙 */
--epgo-bg-light: #F9FAFB;    /* 浅色背景 */
--epgo-border:   #E5E7EB;    /* 边框颜色 */
```

### 2. 间距和排版优化

```css
/* 增加垂直间距 */
section {
    padding: 60px 0;  /* 从 50px 改为 60px */
}

/* 优化卡片间距 */
.card {
    margin-bottom: 24px;  /* 统一为24px */
    gap: 24px;  /* 卡片间距 */
}

/* 改进标题间距 */
h2 {
    margin-bottom: 50px;  /* 从 40px 改为 50px */
}
```

### 3. 阴影效果优化

```css
/* 增加微妙的阴影效果 */
--shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
--shadow-md: 0 4px 12px rgba(0,0,0,0.1);
--shadow-lg: 0 8px 24px rgba(37,99,235,0.12);
--shadow-hover: 0 12px 32px rgba(0,0,0,0.15);
```

---

## 📱 响应式优化

### 移动端优化建议

```css
@media (max-width: 768px) {
    /* 首页部分优化 */
    h2 { font-size: 28px !important; }
    p { font-size: 14px !important; }

    /* 卡片网格调整 */
    .card-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    /* 按钮优化 */
    .btn { padding: 12px 20px !important; }

    /* 间距优化 */
    section { padding: 40px 0 !important; }
}
```

---

## ✅ 实施检查清单

- [ ] 添加"最新学习资讯"区域到index.php
- [ ] 添加"热门下载资源"区域到index.php
- [ ] 添加"常见问题"(FAQ)区域到index.php
- [ ] 优化CSS颜色和间距
- [ ] 改进移动端响应式效果
- [ ] 测试所有链接是否正常
- [ ] 验证SEO标签和描述
- [ ] 测试页面加载速度
- [ ] 在手机上测试显示效果
- [ ] 最终确认用户体验

---

完成首页优化计划！
