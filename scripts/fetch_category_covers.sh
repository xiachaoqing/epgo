#!/bin/bash
# 批量为栏目下载Unsplash 图片封面

UPLOAD_DIR="/www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers"
DB_HOST="127.0.0.1"
DB_USER="xiachaoqing"
DB_PASS="***REMOVED***"
DB_NAME="epgo_db"

# 栏目配置: category_id|folder_name|url|description
declare -a CATEGORIES=(
    "101|ket|https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=1200\&h=800\&fit=crop\&q=80|KET备考"
    "102|pet|https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200\&h=800\&fit=crop\&q=80|PET备考"
    "103|reading|https://images.unsplash.com/photo-1507842217343-583f20270319?w=1200\&h=800\&fit=crop\&q=80|英语阅读"
    "104|speech|https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200\&h=800\&fit=crop\&q=80|英语演讲"
    "105|daily|https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200\&h=800\&fit=crop\&q=80|每日英语"
    "106|download|https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1200\&h=800\&fit=crop\&q=80|资料下载"
    "107|about|https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200\&h=800\&fit=crop\&q=80|关于我们"
)

echo "============================================================"
echo "英语教育栏目封面爬取与配置"
echo "============================================================"
echo ""

total_success=0

for item in "${CATEGORIES[@]}"; do
    IFS='|' read cat_id folder_name url desc <<< "$item"

    echo "[栏目 $cat_id] $desc"
    echo "  图片URL: ${url:0:70}..."

    # 创建目录
    mkdir -p "$UPLOAD_DIR/$folder_name" 2>/dev/null

    # 下载图片
    filename="cover_$(date +%s).jpg"
    filepath="$UPLOAD_DIR/$folder_name/$filename"
    webpath="/upload/epgo-photo-covers/$folder_name/$filename"

    echo "  下载中..."
    curl -fsSL -m 30 "$url" -o "$filepath" 2>/dev/null

    if [ ! -s "$filepath" ]; then
        echo "  ✗ 下载失败或文件为空"
        rm -f "$filepath"
        continue
    fi

    filesize=$(du -h "$filepath" | cut -f1)
    echo "  ✓ 下载成功: $filename ($filesize)"

    # 更新数据库
    echo "  更新数据库..."
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -v 2>/dev/null <<EOF
UPDATE ep_news
SET imgurl='$webpath'
WHERE recycle=0
AND (class1 = $cat_id OR class1 IN (
    SELECT id FROM ep_column WHERE bigclass = $cat_id
))
AND imgurl LIKE '%epgo-covers%'
LIMIT 5000;
EOF

    # 统计更新的文章数
    updated=$(mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -Nse "
        SELECT COUNT(*) FROM ep_news WHERE imgurl='$webpath' AND recycle=0;
    " 2>/dev/null)

    echo "  ✓ 栏目 $cat_id 处理完成 ($updated 篇文章)"
    total_success=$((total_success + 1))

    echo ""
    sleep 1
done

echo "============================================================"
echo "✅ 完成！共处理 $total_success 个栏目"
echo "👉 访问 https://xiachaoqing.com 查看效果"
echo "💾 所有封面已保存到: $UPLOAD_DIR"
echo "============================================================"
