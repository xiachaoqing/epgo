#!/bin/bash
# 为所有文章随机生成时间戳 (最近30天内)

set -e

DB_HOST="127.0.0.1"
DB_USER="hanhong"
DB_PASS="***REMOVED***"
DB_NAME="hanhong"

echo "【生成随机时间戳】"

# 获取所有文章的ID
article_ids=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -N -e \
    "SELECT id FROM hh_news WHERE lang='cn' ORDER BY id;" 2>/dev/null)

total_count=$(echo "$article_ids" | wc -l)
current=0

# 为每篇文章生成随机时间
for id in $article_ids; do
    current=$((current + 1))

    # 生成随机天数 (0-29天前)
    random_days=$((RANDOM % 30))

    # 生成随机小时 (0-23)
    random_hour=$((RANDOM % 24))

    # 生成随机分钟 (0-59)
    random_minute=$((RANDOM % 60))

    # 生成随机秒数 (0-59)
    random_second=$((RANDOM % 60))

    # 计算具体日期 (使用MySQL的DATE_SUB)
    # 构建随机时间
    random_time="DATE_SUB(NOW(), INTERVAL $random_days DAY) + INTERVAL $random_hour HOUR + INTERVAL $random_minute MINUTE + INTERVAL $random_second SECOND"

    # 更新数据库
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e \
        "UPDATE hh_news SET addtime = DATE_SUB(CURDATE(), INTERVAL $random_days DAY) + INTERVAL $random_hour HOUR + INTERVAL $random_minute MINUTE + INTERVAL $random_second SECOND WHERE id = $id;" 2>/dev/null

    # 同步updatetime
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e \
        "UPDATE hh_news SET updatetime = addtime WHERE id = $id;" 2>/dev/null

    # 显示进度
    if [ $((current % 5)) -eq 0 ]; then
        echo "  已处理: $current/$total_count"
    fi
done

echo ""
echo "✅ 所有文章已随机生成时间戳"
echo ""
echo "【随机时间验证】"
mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e \
    "SELECT '最新发布' as 时间段, COUNT(*) as 篇数 FROM hh_news WHERE lang='cn' AND DATE(addtime) = CURDATE()
    UNION ALL
    SELECT '1天前', COUNT(*) FROM hh_news WHERE lang='cn' AND DATE(addtime) = CURDATE() - INTERVAL 1 DAY
    UNION ALL
    SELECT '2-7天前', COUNT(*) FROM hh_news WHERE lang='cn' AND DATE(addtime) BETWEEN CURDATE() - INTERVAL 7 DAY AND CURDATE() - INTERVAL 2 DAY
    UNION ALL
    SELECT '8-30天前', COUNT(*) FROM hh_news WHERE lang='cn' AND DATE(addtime) BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE() - INTERVAL 8 DAY;
    SELECT '';
    SELECT '最新的5篇文章:' as 文章;
    SELECT CONCAT(id, '. ', title, ' | ', addtime) FROM hh_news WHERE lang='cn' ORDER BY addtime DESC LIMIT 5;" 2>/dev/null | grep -v Warning
