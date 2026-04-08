<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />
<main class="met-shownews animsition">
    <div class="container">
        <div class="row">
            <div class="clearfix">

                <!-- ===== 主内容区 m-id="noset" 不可删 ===== -->
                <div class="col-md-9 met-shownews-body" m-id="noset">
                    <div class="row">

                        <!-- 标题 + 元信息 -->
                        <section class="details-title border-bottom1">
                            <h1 class="m-0">{$data.title}</h1>
                            <div class="info font-weight-300">
                                <span>{$data.updatetime}</span>
                                <if value="1">
                                    <span>{$data.issue}</span>
                                </if>
                                <if value="1">
                                    <span>
                                        <i class="icon wb-eye m-r-5" aria-hidden="true"></i>
                                        {$data.hits}
                                    </span>
                                </if>
                            </div>
                        </section>

                        <?php
                            $_detail_cover = trim($data['imgurl']);
                            $_detail_class = intval($data['class1']);
                            $_cover_map = array(
                                101 => '/upload/epgo-covers/ket.png',
                                102 => '/upload/epgo-covers/pet.png',
                                103 => '/upload/epgo-covers/reading.png',
                                104 => '/upload/epgo-covers/speech.png',
                                105 => '/upload/epgo-covers/daily.png',
                                106 => '/upload/epgo-covers/download.png',
                                107 => '/upload/epgo-covers/about.png',
                                111 => '/upload/epgo-covers/ket.png',
                                112 => '/upload/epgo-covers/ket.png',
                                113 => '/upload/epgo-covers/ket.png',
                                114 => '/upload/epgo-covers/ket.png',
                                121 => '/upload/epgo-covers/pet.png',
                                122 => '/upload/epgo-covers/pet.png',
                                123 => '/upload/epgo-covers/pet.png',
                                124 => '/upload/epgo-covers/pet.png',
                            );
                            if (!$_detail_cover && isset($_cover_map[$_detail_class])) {
                                $_detail_cover = $_cover_map[$_detail_class];
                            }
                            if (strpos($_detail_cover, '..//') === 0) $_detail_cover = '/' . ltrim(substr($_detail_cover, 4), '/');
                            if (strpos($_detail_cover, '../') === 0) $_detail_cover = '/' . ltrim(substr($_detail_cover, 3), '/');
                            if ($_detail_cover && strpos($_detail_cover, 'http') !== 0) $_detail_cover = 'https://xiachaoqing.com' . $_detail_cover;

                            $_prev = null;
                            $_next = null;
                            try {
                                $_raw  = file_get_contents(PATH_CONFIG . 'config_db.php');
                                preg_match('/con_db_host\s*=\s*"([^"]+)"/', $_raw, $_eh);
                                preg_match('/con_db_id\s*=\s*"([^"]+)"/',   $_raw, $_eu);
                                preg_match('/con_db_pass\s*=\s*"([^"]+)"/',  $_raw, $_ep);
                                preg_match('/con_db_name\s*=\s*"([^"]+)"/',  $_raw, $_en);
                                preg_match('/tablepre\s*=\s*"([^"]+)"/',     $_raw, $_et);
                                $_db = new mysqli($_eh[1]??'localhost', $_eu[1]??'', $_ep[1]??'', $_en[1]??'');
                                if (!$_db->connect_error) {
                                    $_db->set_charset('utf8mb4');
                                    $_pre = $_et[1] ?? 'ep_';
                                    $_id  = intval($data['id']);
                                    $_class1 = intval($data['class1']);
                                    $_prev_sql = 'SELECT id,title,filename,class1 FROM `'.$_pre.'news` WHERE recycle=0 AND class1=' . $_class1 . ' AND id>' . $_id . ' ORDER BY id ASC LIMIT 1';
                                    $_next_sql = 'SELECT id,title,filename,class1 FROM `'.$_pre.'news` WHERE recycle=0 AND class1=' . $_class1 . ' AND id<' . $_id . ' ORDER BY id DESC LIMIT 1';
                                    $_prev_res = $_db->query($_prev_sql);
                                    $_next_res = $_db->query($_next_sql);
                                    $_prev = $_prev_res ? $_prev_res->fetch_assoc() : null;
                                    $_next = $_next_res ? $_next_res->fetch_assoc() : null;
                                    $_db->close();
                                }
                            } catch (Exception $_ex) {}
                            $_folder_map = array(
                                101=>'ket',102=>'pet',103=>'reading',104=>'speech',105=>'daily',106=>'download',107=>'about',
                                111=>'ket-exam',112=>'ket-word',113=>'ket-write',114=>'ket-listen',121=>'pet-exam',122=>'pet-word',123=>'pet-write',124=>'pet-read'
                            );
                            if ($_prev && empty($_prev['filename']) && isset($_folder_map[intval($_prev['class1'])])) $_prev['url'] = '/' . $_folder_map[intval($_prev['class1'])] . '/' . intval($_prev['id']) . '.html';
                            if ($_next && empty($_next['filename']) && isset($_folder_map[intval($_next['class1'])])) $_next['url'] = '/' . $_folder_map[intval($_next['class1'])] . '/' . intval($_next['id']) . '.html';
                            if ($_prev && !empty($_prev['filename'])) $_prev['url'] = '/' . trim($_prev['filename']) . '.html';
                            if ($_next && !empty($_next['filename'])) $_next['url'] = '/' . trim($_next['filename']) . '.html';
                        ?>
                        <?php if($_detail_cover){ ?>
                        <section class="epgo-detail-cover">
                            <img src="<?php echo htmlspecialchars($_detail_cover); ?>" alt="<?php echo htmlspecialchars($data['title']); ?>">
                        </section>
                        <?php } ?>

                        <!-- 正文（视频由MetInfo富文本自动渲染） -->
                        <section class="met-editor clearfix">
                            {$data.content}
                        </section>

                        <!-- 标签 -->
                        <if value="1">
                            <list data="$data['taglist']" name="$tag" num="4"></list>
                            <if value="$sub">
                                <div class="tag detail_tag">
                                    <span>{$data.tagname}</span>
                                    <list data="$data['taglist']" name="$tag" num="5">
                                        <a href="{$tag.url}" title="{$tag.name}">{$tag.name}</a>
                                    </list>
                                </div>
                            </if>
                        </if>

                        <section class="epgo-prev-next">
                            <div class="epgo-prev-next-grid">
                                <div class="epgo-prev-next-item">
                                    <span class="label">更新的文章</span>
                                    <?php if($_prev){ ?>
                                    <a href="<?php echo htmlspecialchars($_prev['url']); ?>" title="<?php echo htmlspecialchars($_prev['title']); ?>"><?php echo htmlspecialchars($_prev['title']); ?></a>
                                    <?php } else { ?>
                                    <span class="empty">已经是最新一篇</span>
                                    <?php } ?>
                                </div>
                                <div class="epgo-prev-next-item align-right">
                                    <span class="label">更早的文章</span>
                                    <?php if($_next){ ?>
                                    <a href="<?php echo htmlspecialchars($_next['url']); ?>" title="<?php echo htmlspecialchars($_next['title']); ?>"><?php echo htmlspecialchars($_next['title']); ?></a>
                                    <?php } else { ?>
                                    <span class="empty">已经是最早一篇</span>
                                    <?php } ?>
                                </div>
                            </div>
                        </section>

                    </div>
                </div>

                <!-- ===== 右侧边栏 ===== -->
                <div class="col-md-3">
                    <div class="row">
                        <aside class="met-sidebar panel panel-body m-b-0" boxmh-h
                               m-id="news_bar" m-type="nocontent">

                            <!-- 搜索 -->
                            <div class="sidebar-search" data-placeholder="search">
                                <tag action="search.column"></tag>
                            </div>

                            <!-- 栏目导航 -->
                            <if value="$lang['bar_column_open']">
                            <ul class="sidebar-column list-icons">
                                <tag action='category' cid="$data['releclass1']">
                                <li>
                                    <a href="{$m.url}" title="{$m.name}"
                                       class="<if value='$data["classnow"] eq $m["id"]'>active</if>"
                                       {$m.urlnew}>{$m.name}</a>
                                </li>
                                <tag action='category' cid="$m['id']" type='son' class='active'>
                                <li>
                                    <if value="$m['sub'] && $lang['bar_column3_open']">
                                        <a href="javascript:;" title="{$m.name}" class="{$m.class}"
                                           {$m.urlnew} data-toggle="collapse"
                                           data-target=".sidebar-column3-{$m._index}">{$m.name}
                                            <i class="wb-chevron-right-mini"></i>
                                        </a>
                                        <div class="sidebar-column3-{$m._index} collapse" aria-expanded="false">
                                            <ul class="m-t-5 p-l-20">
                                                <li>
                                                    <a href="{$m.url}" {$m.urlnew} title="{$lang.all}"
                                                       class="{$m.class}">{$lang.all}</a>
                                                </li>
                                                <tag action='category' cid="$m['id']" type='son' class='active'>
                                                <li>
                                                    <a href="{$m.url}" {$m.urlnew} title="{$m.name}"
                                                       class="{$m.class}">{$m.name}</a>
                                                </li>
                                                </tag>
                                            </ul>
                                        </div>
                                    <else/>
                                        <a href="{$m.url}" title="{$m.name}" class="{$m.class}">{$m.name}</a>
                                    </if>
                                </li>
                                </tag>
                                </tag>
                            </ul>
                            </if>

                            <!-- 推荐文章列表 -->
                            <if value="$lang['news_bar_list_open']">
                            <div class="sidebar-news-list recommend">
                                <h3 class="font-size-16 m-0">{$lang.news_bar_list_title}</h3>
                                <ul class="list-group list-group-bordered m-t-10 m-b-0">
                                    <?php $id=$lang['sidebar_newslist_idid']
                                        ?$lang['sidebar_newslist_idid']:$data['class1']; ?>
                                    <tag action='list' type="$lang['news_bar_list_type']"
                                         cid="$id" num="$lang['sidebar_newslist_num']">
                                    <li class="list-group-item">
                                        <if value="1">
                                        <a class="imga" href="{$v.url}" title="{$v.title}" {$g.urlnew}>
                                            <img src="{$v.imgurl|thumb:800,500}" alt="{$v.title}"
                                                 style="max-width:100%">
                                        </a>
                                        </if>
                                        <a href="{$v.url}" title="{$v.title}" {$g.urlnew}>{$v.title}</a>
                                    </li>
                                    </tag>
                                </ul>
                            </div>
                            </if>

                        </aside>
                    </div>
                </div>

            </div>
        </div>
    </div>
</main>
<style>
.epgo-detail-cover{margin:18px 0 24px;border-radius:16px;overflow:hidden;background:#F3F4F6;box-shadow:0 4px 18px rgba(0,0,0,.08);}
.epgo-detail-cover img{display:block;width:100%;height:clamp(220px,34vw,360px);object-fit:cover;object-position:center center;}
.epgo-prev-next{margin-top:26px;padding-top:24px;border-top:1px solid #E5E7EB;}
.epgo-prev-next-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.epgo-prev-next-item{background:#F8FAFC;border:1px solid #E5E7EB;border-radius:12px;padding:16px 18px;min-height:92px;display:flex;flex-direction:column;justify-content:center;}
.epgo-prev-next-item .label{font-size:12px;color:#6B7280;margin-bottom:8px;font-weight:700;letter-spacing:.02em;}
.epgo-prev-next-item a{color:#111827;text-decoration:none;line-height:1.7;font-weight:600;}
.epgo-prev-next-item a:hover{color:#2563EB;}
.epgo-prev-next-item .empty{color:#9CA3AF;line-height:1.7;}
.epgo-prev-next-item.align-right{text-align:right;}
@media(max-width:767px){
  .epgo-detail-cover img{height:220px;}
  .epgo-prev-next-grid{grid-template-columns:1fr;}
  .epgo-prev-next-item.align-right{text-align:left;}
}
</style>
<include file="foot.php" />
