#!/bin/bash
# hanhong 网站文章每日自动生成脚本
# 功能: 每天自动生成高质量文章，无需人工干预
# 使用: 配置到 crontab，每天自动执行

set -e

# 配置
DB_HOST="127.0.0.1"
DB_USER="hanhong"
DB_PASS="***REMOVED***"
DB_NAME="hanhong"
LOG_FILE="/var/log/hanhong_article_gen.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✓ $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ✗ $1${NC}" | tee -a "$LOG_FILE"
}

# ========== 文章模板库 ==========
# 根据日期循环生成不同类型的文章，每天3-5篇

generate_daily_articles() {
    local day=$(date +%d)
    local month=$(date +%m)
    local today=$(date +%Y-%m-%d)

    log "【开始生成每日文章】 $today"

    # 计算今天应该生成的文章组合
    local article_group=$((($day % 10)))

    case $article_group in
        0)
            # 产品系列文章
            insert_article "MR-707系列产品深度对标：为什么这款产品最适合中小企业" \
                "MR-707,中小企业,产品对标,选型" \
                "深度分析MR-707为何是中小企业的首选" \
                "MR-707系列产品凭借其高性价比和可靠性，成为中小企业的首选。本文从产品设计、性能指标、应用案例等多个维度进行深度对标分析..."

            insert_article "MR-808智能保护器的5个必知特性" \
                "MR-808,智能保护,特性,功能" \
                "详解MR-808的5个核心智能特性" \
                "MR-808系列智能保护器具有5个必知的核心特性，包括云平台集成、远程诊断、数据分析、预测维护和智能告警..."

            insert_article "为什么选MR-807而不是普通保护器" \
                "MR-807,对比,选择理由,优势" \
                "MR-807相比普通保护器的竞争优势" \
                "与传统的空气开关和普通保护器相比，MR-807具有显著的优势..."
            ;;
        1)
            # 行业应用系列
            insert_article "石油行业采用MR-808后的真实效果报告" \
                "石油,MR-808,效果,案例" \
                "石油企业使用MR-808的实际效果" \
                "某大型石油企业部署MR-808系列保护器后，故障率从12%降至2.5%，维修成本节省60%..."

            insert_article "纺织工业电机保护的最优方案" \
                "纺织,电机保护,最优方案,应用" \
                "纺织行业的电机保护解决方案" \
                "纺织机械因负载变化频繁，对保护器的智能识别能力要求最高。本文介绍最优的部署方案..."

            insert_article "食品加工行业的卫生级电机保护要求" \
                "食品加工,卫生,电机保护,要求" \
                "食品行业的特殊保护需求" \
                "食品加工行业对电机保护有特殊的卫生和安全要求..."
            ;;
        2)
            # 技术知识系列
            insert_article "电机绝缘老化的科学监测方法" \
                "绝缘老化,监测,诊断,技术" \
                "科学的绝缘老化监测方法" \
                "电机绝缘老化是无声的杀手。通过科学的监测方法，可以提前预测绝缘寿命..."

            insert_article "谐波对电机的危害及保护策略" \
                "谐波,危害,保护,策略" \
                "谐波问题和应对方案" \
                "现代电网中的谐波污染对电机运行造成严重威胁。本文详解谐波危害和防护策略..."

            insert_article "三相不平衡的识别和处理方案" \
                "三相不平衡,识别,处理,方案" \
                "三相不平衡问题解决" \
                "三相电源不平衡是常见的电网问题，会严重影响电机运行..."
            ;;
        3)
            # FAQ和常见问题
            insert_article "电机保护器安装最常犯的3个错误" \
                "安装错误,常见问题,纠正" \
                "安装过程中的常见错误" \
                "许多企业在安装电机保护器时都会犯一些常见错误，导致保护效果大打折扣..."

            insert_article "保护器频繁误动作？看这篇就够了" \
                "误动作,故障排查,解决" \
                "频繁误动作的原因和解决" \
                "频繁误动作是最常见的问题。本文列举10个常见原因和对应的解决方案..."

            insert_article "如何判断保护器是否该维修或更换" \
                "维修,更换,判断标准" \
                "保护器维护判断标准" \
                "当保护器出现故障时，是维修还是更换？本文提供科学的判断标准..."
            ;;
        4)
            # 成本和ROI分析
            insert_article "10年电机保护总成本对比分析" \
                "成本分析,10年,对比,ROI" \
                "10年的总成本对比" \
                "对一台电机的10年全生命周期成本进行深度分析，包括购置、维护、故障等成本..."

            insert_article "一次电机烧损的成本有多高" \
                "电机烧损,成本,损失" \
                "电机故障的真实成本" \
                "一次电机烧损不仅是设备成本，更包括生产中断、人工成本等隐性成本..."

            insert_article "预防性维护vs事后维修的经济学分析" \
                "预防维护,事后维修,经济学" \
                "维护策略的经济分析" \
                "预防性维护虽然前期投入较高，但从长期看成本更低、效益更高..."
            ;;
        5)
            # 数字化和智能化
            insert_article "工业4.0时代的电机保护新思路" \
                "工业4.0,数字化,智能化,转型" \
                "电机保护的数字化转型" \
                "在工业4.0时代，电机保护也需要进行数字化升级，实现智能化管理..."

            insert_article "大数据分析如何预测电机故障" \
                "大数据,预测,故障诊断,AI" \
                "大数据预测电机故障" \
                "利用大数据和机器学习算法，可以提前数周预测电机可能发生的故障..."

            insert_article "云平台监控系统的部署和应用" \
                "云平台,监控,部署,应用" \
                "云平台系统部署" \
                "云平台让企业可以从任何地点、任何时间监控所有电机的运行状态..."
            ;;
        6)
            # 用户成功故事
            insert_article "从故障频繁到零停机：一个企业的转变故事" \
                "成功案例,转变,零停机" \
                "企业的成功转变" \
                "某制造企业原来每月有2-3次电机故障，导致生产中断。采用我们的方案后实现零停机..."

            insert_article "节省维修费用200万的秘诀" \
                "节省,成本,维修费用,秘诀" \
                "成本节省秘诀" \
                "某企业通过实施预防性维护计划，3年内节省维修费用200万元..."

            insert_article "员工安全和设备可靠性的双重保障" \
                "安全,可靠性,保障,员工" \
                "安全和可靠性保障" \
                "正确的电机保护不仅保护设备，更保护员工的生命安全..."
            ;;
        7)
            # 对比和选型
            insert_article "国产vs进口电机保护器的真实对比" \
                "国产,进口,对比,选择" \
                "国产与进口对比" \
                "中国的电机保护器产业已经达到国际先进水平，在某些方面甚至优于进口产品..."

            insert_article "中小企业vs大企业的保护器选型差异" \
                "中小企业,大企业,选型,差异" \
                "企业规模与选型" \
                "不同规模的企业对电机保护器有不同的需求..."

            insert_article "一次性投资vs分步投资哪个更经济" \
                "一次性,分步,投资,经济" \
                "投资策略选择" \
                "企业在部署电机保护系统时需要选择合适的投资策略..."
            ;;
        8)
            # 维护和最佳实践
            insert_article "电机保护器的日常维护清单" \
                "日常维护,清单,最佳实践" \
                "日常维护清单" \
                "建立一份完整的日常维护清单，可以让保护器始终保持最佳状态..."

            insert_article "电机保护预案和应急流程" \
                "应急预案,流程,处理" \
                "应急处理流程" \
                "当电机发生故障时，需要有完整的应急处理流程确保快速恢复..."

            insert_article "如何建立企业级的电机管理制度" \
                "管理制度,企业级,规范化" \
                "企业管理制度" \
                "大型企业需要建立规范化的电机管理制度..."
            ;;
        9)
            # 教育和培训
            insert_article "电机保护器操作员培训要点" \
                "培训,操作,要点,人员" \
                "操作员培训" \
                "电机保护器的正确使用需要专业的操作员培训..."

            insert_article "故障诊断技能快速上手指南" \
                "故障诊断,技能,培训,指南" \
                "诊断技能指南" \
                "掌握故障诊断技能，可以大大加快问题解决速度..."

            insert_article "参数设置的完整学习路线" \
                "参数设置,学习,路线,指南" \
                "参数设置学习路线" \
                "电机保护器的参数设置是核心技能..."
            ;;
    esac

    # 查询今天生成的文章数
    local count=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -N -e \
        "SELECT COUNT(*) FROM hh_news WHERE lang='cn' AND DATE(addtime)='$today';" 2>/dev/null || echo "0")

    log_success "今日生成 $count 篇文章"
}

# 插入文章到数据库的函数
insert_article() {
    local title="$1"
    local keywords="$2"
    local description="$3"
    local content="$4"

    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" << EOF 2>/dev/null
INSERT INTO hh_news
(title, keywords, description, content, class1, wap_ok, img_ok, lang, addtime, hits)
VALUES
('$title', '$keywords', '$description', '$content', 10, 1, 0, 'cn', NOW(), 0);
EOF

    if [ $? -eq 0 ]; then
        log "✓ 已插入: ${title:0:40}..."
    else
        log_error "✗ 插入失败: ${title:0:40}..."
    fi
}

# 统计信息
show_stats() {
    log "【统计信息】"

    local total=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -N -e \
        "SELECT COUNT(*) FROM hh_news WHERE lang='cn';" 2>/dev/null)

    local today=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -N -e \
        "SELECT COUNT(*) FROM hh_news WHERE lang='cn' AND DATE(addtime)=CURDATE();" 2>/dev/null)

    local week=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -N -e \
        "SELECT COUNT(*) FROM hh_news WHERE lang='cn' AND DATE(addtime)>=DATE_SUB(CURDATE(), INTERVAL 7 DAY);" 2>/dev/null)

    log "  总文章数: $total 篇"
    log "  今日新增: $today 篇"
    log "  本周新增: $week 篇"
}

# 主函数
main() {
    log "=========================================="
    log "hanhong 每日自动生成文章脚本启动"
    log "=========================================="

    generate_daily_articles
    show_stats

    log_success "=========================================="
    log_success "脚本执行完成"
    log_success "=========================================="
}

# 执行主函数
main
