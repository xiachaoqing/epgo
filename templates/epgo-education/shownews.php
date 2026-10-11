<?php defined('IN_MET') or exit('No permission'); ?>
<include file="head.php" />
<?php
$_epgo_author_name = trim((string)($data['publisher'] ?? ''));
if ($_epgo_author_name === '' || strtolower($_epgo_author_name) === 'system') {
    $_epgo_author_name = '英语陪跑GO';
}
$_epgo_author_schema = $_epgo_author_name === 'Cathy'
    ? array('@type' => 'Person', 'name' => 'Cathy', 'url' => 'https://xiachaoqing.com/about/')
    : array('@type' => 'Organization', 'name' => $_epgo_author_name);
$_epgo_article_schema = array(
    '@context' => 'https://schema.org',
    '@type' => 'Article',
    'headline' => trim(strip_tags($data['title'] ?? '英语学习文章')),
    'description' => trim(strip_tags($data['description'] ?? '英语学习与 KET/PET 备考内容')),
    'dateModified' => !empty($data['updatetime']) ? date('c', strtotime($data['updatetime'])) : date('c'),
    'author' => $_epgo_author_schema,
    'publisher' => array('@type' => 'Organization', 'name' => '英语陪跑GO', 'logo' => array('@type' => 'ImageObject', 'url' => 'https://xiachaoqing.com/epgo/logo.png')),
    'mainEntityOfPage' => array('@type' => 'WebPage', '@id' => 'https://xiachaoqing.com' . (parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/'))
);
echo '<script type="application/ld+json">' . json_encode($_epgo_article_schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . '</script>';
unset($_epgo_article_schema, $_epgo_author_schema);

$_epgo_article_class_id = intval($data['class1'] ?? 0);
$_epgo_article_audience = '英语学习者和家长，可根据文章主题选择适合自己的练习方式。';
$_epgo_article_method = '先通读文章，再完成其中的例句或练习；把不确定的词句记录下来，隔天复习一次。';
if (in_array($_epgo_article_class_id, array(101, 111, 112, 113, 114), true)) {
    $_epgo_article_audience = '正在准备 KET，或需要系统补充基础词汇、阅读、听力和写作能力的学习者。';
    $_epgo_article_method = '先明确题型或知识点，再做文中的例题；把错题按“为什么错、依据在哪、下次怎么判断”记录下来。';
} elseif (in_array($_epgo_article_class_id, array(102, 121, 122, 123, 124), true)) {
    $_epgo_article_audience = '已经具备一定英语基础，正在准备 PET 或希望提高综合运用能力的学习者。';
    $_epgo_article_method = '先读懂题目要求，再定位文章或句子中的证据；完成练习后，用自己的话复述判断过程。';
} elseif ($_epgo_article_class_id === 103) {
    $_epgo_article_audience = '希望通过分级阅读、精读和泛读逐步提高理解能力的英语学习者。';
    $_epgo_article_method = '第一遍先理解大意，第二遍圈出影响理解的词句，最后用一两句话复述文章主旨。';
} elseif ($_epgo_article_class_id === 104) {
    $_epgo_article_audience = '希望练习英语表达、演讲结构和口语组织能力的学习者。';
    $_epgo_article_method = '先模仿文章中的表达，再替换成自己的经历或观点，录音后检查信息是否完整、语速是否自然。';
} elseif ($_epgo_article_class_id === 105) {
    $_epgo_article_audience = '希望用短时间保持英语输入和输出习惯的学习者，适合安排在日常碎片时间完成。';
    $_epgo_article_method = '先听或朗读一遍，再理解关键词和句型，最后不看原文复述或造一个自己的句子。';
}
?>
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
                                <span class="epgo-article-author">作者：<?php echo htmlspecialchars($_epgo_author_name, ENT_QUOTES, 'UTF-8'); ?></span>
                                <span>{$data.updatetime}</span>
                                <if value="1">
                                    <span>{$data.issue}</span>
                                </if>
                            </div>
                        </section>

                        <aside class="epgo-article-context" aria-label="文章学习说明">
                            <div class="epgo-article-context-item">
                                <strong>作者与编辑</strong>
                                <span>Cathy｜英语陪跑GO</span>
                            </div>
                            <div class="epgo-article-context-item">
                                <strong>适合人群</strong>
                                <span><?php echo htmlspecialchars($_epgo_article_audience, ENT_QUOTES, 'UTF-8'); ?></span>
                            </div>
                            <div class="epgo-article-context-item">
                                <strong>建议用法</strong>
                                <span><?php echo htmlspecialchars($_epgo_article_method, ENT_QUOTES, 'UTF-8'); ?></span>
                            </div>
                        </aside>

                        <?php
                            $_detail_cover = trim($data['imgurl']);
                            $_detail_class = intval($data['class1']);
                            if (!$_detail_cover) {
                                if (in_array($_detail_class, array(111,112,113,114))) $_detail_cover = '/upload/epgo-covers/ket.png';
                                if (in_array($_detail_class, array(121,122,123,124))) $_detail_cover = '/upload/epgo-covers/pet.png';
                                if ($_detail_class == 103) $_detail_cover = '/upload/epgo-covers/reading.png';
                                if ($_detail_class == 104) $_detail_cover = '/upload/epgo-covers/speech.png';
                                if ($_detail_class == 105) $_detail_cover = '/upload/epgo-covers/daily.png';
                            }
                            if (strpos($_detail_cover, '..//') === 0) $_detail_cover = '/' . ltrim(substr($_detail_cover, 4), '/');
                            if (strpos($_detail_cover, '../') === 0) $_detail_cover = '/' . ltrim(substr($_detail_cover, 3), '/');
                            if ($_detail_cover && strpos($_detail_cover, 'http') !== 0) $_detail_cover = 'https://xiachaoqing.com' . $_detail_cover;
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

                        <section class="epgo-article-next" aria-label="学习路径入口">
                            <div>
                                <strong>想知道孩子现在适合从哪里开始？</strong>
                                <p>用一套基础入学测评了解阅读、听力、词汇和表达情况，再把结果交给老师安排下一步练习。</p>
                            </div>
                            <a href="/epgo/assessment.html">免费做入学测评 →</a>
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

                        <!-- 上一篇/下一篇 -->
                        <pagination/>

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
.epgo-detail-cover{margin:22px 0 28px;border-radius:16px;overflow:hidden;background:#F3F4F6;box-shadow:0 4px 18px rgba(0,0,0,.08);}
.epgo-detail-cover img{display:block;width:100%;height:auto;min-height:220px;object-fit:cover;}
.epgo-article-author{color:#1565C0;font-weight:500;}
.epgo-article-context{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:22px 0 28px;padding:16px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;}
.epgo-article-context-item{min-width:0;}
.epgo-article-context-item strong{display:block;margin-bottom:6px;color:#15356F;font-size:13px;}
.epgo-article-context-item span{display:block;color:#52627A;font-size:13px;line-height:1.7;}
.epgo-article-next{display:flex;align-items:center;justify-content:space-between;gap:20px;margin:30px 0;padding:20px 22px;border:1px solid #dbeafe;border-radius:14px;background:#eff6ff;}
.epgo-article-next strong{display:block;color:#15356f;font-size:17px;margin-bottom:5px;}
.epgo-article-next p{margin:0;color:#52627a;font-size:14px;line-height:1.7;}
.epgo-article-next a{flex:none;padding:10px 16px;border-radius:8px;background:#1565c0;color:#fff;text-decoration:none;font-size:14px;}
@media(max-width:600px){.epgo-article-next{display:block}.epgo-article-next a{display:inline-block;margin-top:12px;}}
@media(max-width:767px){.epgo-article-context{grid-template-columns:1fr;padding:14px;gap:14px;}.epgo-article-context-item{padding-bottom:12px;border-bottom:1px solid #E2E8F0;}.epgo-article-context-item:last-child{padding-bottom:0;border-bottom:0;}}
</style>
<include file="foot.php" />
