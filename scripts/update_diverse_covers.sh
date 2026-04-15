#!/bin/bash
# 为各栏目下载多张不同Unsplash 图片，实现多样化封面

UPLOAD_DIR="/www/wwwroot/go.xiachaoqing.com/upload/epgo-photo-covers"
DB_HOST="127.0.0.1"
DB_USER="xiachaoqing"
DB_PASS="Xia@07090218"
DB_NAME="epgo_db"

# 栏目配置: category_id|folder_name|urls_array (以;分隔多个URL)
# 每个栏目配置 3-4 张不同的图片
declare -a CATEGORIES=(
    "101|ket|https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1531482615713-2afd69097998?w=1200\&h=800\&fit=crop\&q=80"
    "102|pet|https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1507842217343-583f20270319?w=1200\&h=800\&fit=crop\&q=80"
    "103|reading|https://images.unsplash.com/photo-1507842217343-583f20270319?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1532012197267-da84d127e765?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=1200\&h=800\&fit=crop\&q=80"
    "104|speech|https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1516321318423-f06f70a504f9?w=1200\&h=800\&fit=crop\&q=80"
    "105|daily|https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1487180144351-b8472da7d491?w=1200\&h=800\&fit=crop\&q=80;https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=1200\&h=800\&fit=crop\&q=80"
)

echo "============================================================"
echo "英语教育栏目多样化封面爬取与配置"
echo "============================================================"
echo ""

for item in "${CATEGORIES[@]}"; do
    IFS='|' read cat_id folder_name urls_str <<< "$item"

    echo "[栏目 $cat_id] 下载 $folder_name 的多张图片"

    # 创建目录
    mkdir -p "$UPLOAD_DIR/$folder_name" 2>/dev/null

    # 将URL字符串分割成数组
    IFS=';' read -ra urls <<< "$urls_str"

    downloaded_files=()

    for idx in "${!urls[@]}"; do
        url="${urls[$idx]}"
        filename="cover_v$(($idx + 1))_$(date +%s).jpg"
        filepath="$UPLOAD_DIR/$folder_name/$filename"

        echo "  [$((idx + 1))/${#urls[@]}] 下载 ${url:0:60}..."
        curl -fsSL -m 30 "$url" -o "$filepath" 2>/dev/null

        if [ -s "$filepath" ]; then
            filesize=$(du -h "$filepath" | cut -f1)
            echo "    ✓ 成功 ($filesize)"
            downloaded_files+=("$filepath")
        else
            echo "    ✗ 失败"
            rm -f "$filepath"
        fi

        sleep 1
    done

    # 为该栏目的文章分配不同的图片
    if [ ${#downloaded_files[@]} -gt 0 ]; then
        echo "  更新数据库（轮流分配 ${#downloaded_files[@]} 张不同的图片）..."

        # 查询该栏目的所有文章（轮流分配新封面）
        article_ids=$(mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -Nse "
            SELECT id FROM ep_news
            WHERE recycle=0
            AND (class1 = $cat_id OR class1 IN (
                SELECT id FROM ep_column WHERE bigclass = $cat_id
            ))
            ORDER BY id
        " 2>/dev/null)

        article_idx=0
        for article_id in $article_ids; do
            # 轮流分配图片
            file_idx=$((article_idx % ${#downloaded_files[@]}))
            selected_file="${downloaded_files[$file_idx]}"
            webpath=$(echo "$selected_file" | sed "s|/www/wwwroot/go.xiachaoqing.com||")

            mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -Nse "
                UPDATE ep_news SET imgurl='$webpath' WHERE id=$article_id
            " 2>/dev/null

            article_idx=$((article_idx + 1))
        done

        echo "  ✓ 栏目 $cat_id 完成（更新 $article_idx 篇，使用 ${#downloaded_files[@]} 张图片轮流分配）"
    fi

    echo ""
    sleep 1
done

echo "============================================================"
echo "✅ 完成！所有栏目已获得多样化封面"
echo "👉 访问 https://xiachaoqing.com 查看效果"
echo "💾 所有封面已保存到: $UPLOAD_DIR"
echo "============================================================"
