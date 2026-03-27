<?php defined('IN_MET') or exit('No permission'); ?>
<list data="$result" num="$c['met_news_list']" name="$v">
<li class="epgo-list-item" style="background:white; border-radius:12px; overflow:hidden; margin-bottom:24px; box-shadow:0 2px 8px rgba(0,0,0,0.08); transition:all 0.3s ease; display:flex; flex-direction:row; border:1px solid #E5E7EB;">
    <if value="$lang['news_imgok'] && $v['imgurl']">
    <div class="epgo-list-img" style="flex-shrink:0; width:220px; height:160px; overflow:hidden; position:relative; background:#F3F4F6;">
        <a href="{$v.url}" title="{$v.title}" {$g.urlnew} style="display:block; width:100%; height:100%; overflow:hidden;">
            <img <if value="$v['_index'] gt 3 || $data['page'] gt 1">data-original<else/>src</if>="{$v.imgurl|thumb:220,160}" alt="{$v.title}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.3s ease;">
        </a>
        <!-- 分类标签 -->
        <div style="position:absolute; top:12px; left:12px; background:rgba(0,0,0,0.6); color:white; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:700; text-transform:uppercase;">
            {$v.issue}
        </div>
    </div>
    </if>

    <div class="epgo-list-body" style="flex:1; padding:24px; display:flex; flex-direction:column; justify-content:space-between;">
        <!-- 标题 -->
        <div>
            <h3 class="epgo-list-title" style="font-size:18px; font-weight:700; color:#111827; margin:0 0 14px 0; line-height:1.4; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                <a href="{$v.url}" title="{$v.title}" {$g.urlnew} style="color:inherit; text-decoration:none; transition:color 0.3s;">
                    {$v._title}
                </a>
            </h3>

            <!-- 描述 -->
            <p class="epgo-list-desc" style="color:#6B7280; font-size:14px; line-height:1.6; margin:0 0 16px 0; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                {$v.description}
            </p>
        </div>

        <!-- 底部信息 -->
        <div class="epgo-list-footer" style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; gap:16px; font-size:12px; color:#9CA3AF;">
                <span style="display:flex; align-items:center; gap:4px;">
                    <i class="icon wb-calendar"></i>
                    {$v.updatetime}
                </span>
                <span style="display:flex; align-items:center; gap:4px;">
                    <i class="icon wb-eye"></i>
                    {$v.hits}次
                </span>
            </div>
            <a href="{$v.url}" title="{$v.title}" {$g.urlnew} class="epgo-list-readmore" style="color:#2563EB; font-size:13px; font-weight:600; text-decoration:none; display:flex; align-items:center; gap:6px; transition:all 0.3s;">
                继续阅读
                <i class="icon wb-chevron-right" style="font-size:12px;"></i>
            </a>
        </div>
    </div>
</li>

<style>
@media (max-width: 768px) {
    .epgo-list-item {
        flex-direction: column !important;
    }

    .epgo-list-img {
        width: 100% !important;
        height: 200px !important;
    }

    .epgo-list-title {
        font-size: 16px !important;
    }

    .epgo-list-footer {
        flex-direction: column;
        align-items: flex-start !important;
        gap: 12px;
    }
}

@media (max-width: 480px) {
    .epgo-list-body {
        padding: 16px !important;
    }

    .epgo-list-title {
        font-size: 14px !important;
    }

    .epgo-list-desc {
        font-size: 12px !important;
    }
}

/* 悬停效果 */
li.epgo-list-item:hover {
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12);
    border-color: #2563EB;
    transform: translateY(-2px);
}

li.epgo-list-item:hover .epgo-list-title a {
    color: #2563EB;
}

li.epgo-list-item:hover .epgo-list-img img {
    transform: scale(1.05);
}

li.epgo-list-item:hover .epgo-list-readmore {
    color: #1D4ED8;
    gap: 10px;
}
</style>
</list>
