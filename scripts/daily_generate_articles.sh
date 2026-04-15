#!/bin/bash
# epgo 网站文章每日自动生成脚本
# 数据库: epgo_db, 表前缀: ep_
# crontab: 0 8 * * * /www/wwwroot/go.xiachaoqing.com/scripts/daily_generate_articles.sh

DB_HOST="127.0.0.1"
DB_USER="xiachaoqing"
DB_PASS="Xia@07090218"
DB_NAME="epgo_db"
LOG_FILE="/var/log/epgo_article_gen.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

# 栏目 ID 映射
# 101=KET备考  102=PET备考  103=英语阅读  104=英语演讲  105=每日英语
# 111=KET真题  112=KET词汇  113=KET写作  114=KET听力
# 121=PET真题  122=PET词汇  123=PET写作  124=PET阅读

insert_article() {
    local title="$1"
    local keywords="$2"
    local description="$3"
    local content="$4"
    local class1="$5"
    local class2="${6:-0}"

    # 转义单引号，避免 SQL 注入
    local t=$(echo "$title"      | sed "s/'/''/g")
    local k=$(echo "$keywords"   | sed "s/'/''/g")
    local d=$(echo "$description"| sed "s/'/''/g")
    local ct=$(echo "$content"   | sed "s/'/''/g")
    local sql="INSERT INTO ep_news (title,keywords,description,content,class1,class2,wap_ok,img_ok,lang,addtime,hits) VALUES ('$t','$k','$d','$ct',$class1,$class2,1,0,'cn',NOW(),FLOOR(RAND()*500+50))"
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" 2>/dev/null -Ne "$sql"
    [ $? -eq 0 ] && log "  ✓ 插入: ${title:0:40}" || log "  ✗ 失败: ${title:0:40}"
}

main() {
    local day=$((10#$(date +%d)))
    local group=$(( day % 7 ))
    local today=$(date +%Y-%m-%d)
    log "===== epgo 每日文章生成 [$today group=$group] ====="

    case $group in
      0)
        insert_article \
          "KET真题精讲：2024年最新真题阅读Part3解题思路" \
          "KET真题,阅读,Part3,解题" \
          "详解KET阅读Part3的题型特点和高分解题策略" \
          "<p>KET阅读Part3是配对题，要求考生将人物与描述进行匹配。本文结合2024年最新真题，详细讲解做题思路和注意事项。</p><p>解题步骤：1. 先读问题，圈出关键词；2. 扫读文本，定位信息；3. 注意同义替换，避免原词匹配陷阱。</p>" \
          111 101

        insert_article \
          "KET词汇速记：交通出行类100个必考单词" \
          "KET词汇,交通,单词记忆" \
          "KET考试交通出行类核心词汇汇总与记忆方法" \
          "<p>交通出行类词汇是KET考试的高频考点，本文整理100个必考单词，配合例句帮助记忆。</p><p>核心词汇：airport, station, platform, departure, arrival, ticket, boarding pass...</p>" \
          112 101
        ;;
      1)
        insert_article \
          "PET写作Part1邮件写作：5个高分模板句型" \
          "PET写作,邮件,模板,高分" \
          "PET邮件写作的万能模板句型，覆盖开头、正文、结尾" \
          "<p>PET写作Part1要求在35-45词内完成邮件写作。掌握以下5个模板句型，轻松拿高分。</p><p>开头：Thank you for your email about... / I am writing to tell you about...</p><p>正文：I would like to... / Could you please...</p><p>结尾：I hope to hear from you soon. / Best wishes,</p>" \
          123 102

        insert_article \
          "PET阅读Part5词汇填空：高频考点分类整理" \
          "PET阅读,词汇,填空,考点" \
          "PET阅读Part5的词汇考点分类，包含介词、连词、动词短语" \
          "<p>PET阅读Part5考查词汇和语法，本文按考点类型分类整理高频题目。</p><p>介词搭配：interested in, good at, famous for, rely on...</p>" \
          124 102
        ;;
      2)
        insert_article \
          "英语阅读技巧：如何快速定位细节题答案" \
          "英语阅读,细节题,技巧,速读" \
          "细节题是英语阅读的必考题型，掌握定位技巧事半功倍" \
          "<p>细节题要求考生在文章中找到具体信息。关键是学会扫读（scanning）技术，快速锁定答案区域。</p><p>方法：1. 提取问题关键词（时间、地点、数字、人名）；2. 在文章中定位相同或相近词汇；3. 阅读该句上下文验证答案。</p>" \
          103

        insert_article \
          "适合中学生的英文原著推荐：从简单到挑战" \
          "英语阅读,原著,推荐,中学生" \
          "精选适合KET/PET水平的英文读物，培养阅读兴趣" \
          "<p>大量阅读是提高英语能力的最有效方式。以下书单根据难度分级，适合KET/PET阶段的同学。</p><p>入门级：《Charlotte's Web》《The Very Hungry Caterpillar》；进阶级：《The BFG》《Charlie and the Chocolate Factory》。</p>" \
          103
        ;;
      3)
        insert_article \
          "每日英语 | 今日表达：描述天气的10个地道说法" \
          "每日英语,天气,表达,口语" \
          "日常英语中描述天气的地道表达，从简单到丰富" \
          "<p>天气是日常英语对话中最常见的话题。今天学10个地道表达，告别只会说 'It's sunny'。</p><p>1. It's boiling hot! 热死了！2. It's freezing! 冷死了！3. It's drizzling. 在下毛毛雨。4. There's a light breeze. 有微风。</p>" \
          105

        insert_article \
          "每日英语 | 情绪表达：生气、开心、难过怎么说" \
          "每日英语,情绪,表达,口语" \
          "英语中描述各种情绪的地道表达方式" \
          "<p>学好情绪词汇，让你的英语表达更丰富。今天整理常见情绪的地道说法。</p><p>开心：I'm thrilled! / I'm over the moon! 生气：I'm furious. / I'm steaming. 难过：I'm heartbroken. / I'm gutted.</p>" \
          105
        ;;
      4)
        insert_article \
          "英语演讲入门：克服上台紧张的5个实用方法" \
          "英语演讲,紧张,技巧,入门" \
          "针对初学者的英语演讲紧张感克服方法" \
          "<p>上台演讲感到紧张是完全正常的。本文介绍5个经过验证的方法，帮助你在英语演讲时更加自信。</p><p>1. 充分准备：熟背开头和结尾；2. 深呼吸：台上先做3次深呼吸；3. 视线技巧：选择几个友善的听众目光接触。</p>" \
          104

        insert_article \
          "英语演讲结构：三段式框架让演讲更有条理" \
          "英语演讲,结构,框架,三段式" \
          "掌握三段式演讲框架，快速组织英语演讲内容" \
          "<p>好的演讲结构是成功的一半。最经典的是「告诉他们三次」法则：开头告诉听众你要说什么，中间说，结尾再总结。</p><p>开头：Today I'd like to talk about... First, I'll explain... Then... Finally...</p>" \
          104
        ;;
      5)
        insert_article \
          "KET听力Part1图片题：这3类图片差异最容易混淆" \
          "KET听力,图片题,技巧" \
          "KET听力Part1图片选择题的易混淆类型和应对方法" \
          "<p>KET听力Part1要从三张图片中选择正确答案。最容易混淆的三类是：时间类、地点类、物品类。</p><p>应对技巧：听音频前先看图找差异；听到的信息逐一排除；注意否定词（not, don't, can't）。</p>" \
          114 101

        insert_article \
          "KET写作Part9小作文：20个万能衔接词" \
          "KET写作,衔接词,小作文,技巧" \
          "KET写作Part9使用衔接词，让文章结构更清晰" \
          "<p>衔接词能让你的KET作文更有逻辑感，是拿高分的关键。以下20个衔接词覆盖所有写作场景。</p><p>顺序：First, Then, After that, Finally; 转折：However, But, Although; 原因：Because, Since, As</p>" \
          113 101
        ;;
      6)
        insert_article \
          "PET词汇：B1级别必知的100个动词短语" \
          "PET词汇,动词短语,B1,必备" \
          "PET考试B1级别核心动词短语汇总，附例句" \
          "<p>动词短语（phrasal verbs）是PET词汇的重点和难点。本文整理100个B1级必知动词短语。</p><p>高频词：carry out（执行）、find out（发现）、give up（放弃）、look after（照顾）、pick up（捡起/学会）</p>" \
          122 102

        insert_article \
          "PET真题解析：阅读Part4长文章如何快速找主旨" \
          "PET真题,阅读,主旨题,技巧" \
          "PET阅读Part4主旨题解题方法详解" \
          "<p>PET阅读Part4是500词左右的长文章，主旨题是必考题型。掌握以下方法，30秒找到答案。</p><p>方法：1. 先读第一段和最后一段；2. 注意每段第一句（主题句）；3. 归纳共同主题即为文章主旨。</p>" \
          121 102
        ;;
    esac

    # 统计
    local total=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -Ne \
        "SELECT COUNT(*) FROM ep_news WHERE lang='cn'" 2>/dev/null)
    local today_count=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -Ne \
        "SELECT COUNT(*) FROM ep_news WHERE lang='cn' AND DATE(addtime)=CURDATE()" 2>/dev/null)
    log "总文章: $total 篇 | 今日新增: $today_count 篇"
    log "===== 完成 ====="
}

main
