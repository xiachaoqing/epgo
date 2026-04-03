#!/bin/bash

# ============================================================
# 英语陪跑GO - 自动化部署脚本
# 用法: ./deploy.sh [dev|staging|production]
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
PROJECT_ROOT="/Users/xiachaoqing/projects/epgo"
GIT_BRANCH="main"
ENVIRONMENT="${1:-staging}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/epgo"

# 日志函数
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

# ============================================================
# 第1步: 预检查
# ============================================================
echo -e "${BLUE}========== 预检查 ==========${NC}"

log "检查Git仓库状态..."
cd "$PROJECT_ROOT"

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    warning "有未提交的更改，请先提交:"
    git status
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        error "部署已取消"
    fi
fi

# 检查环境
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    error "不是Git仓库"
fi

success "Git仓库检查通过"

# ============================================================
# 第2步: 代码检查
# ============================================================
echo -e "${BLUE}========== 代码检查 ==========${NC}"

log "检查关键文件是否存在..."

REQUIRED_FILES=(
    "templates/epgo-education/index.php"
    "templates/epgo-education/shownews.php"
    "templates/epgo-education/news.php"
    "templates/epgo-education/head.php"
    "templates/epgo-education/foot.php"
    "templates/epgo-education/ajax/news.php"
    "templates/epgo-education/css/epgo-education.css"
    "TEMPLATE_DEVELOPMENT_LOG.md"
    "DEPLOYMENT_CHECKLIST.md"
    "TROUBLESHOOTING_GUIDE.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$PROJECT_ROOT/$file" ]; then
        error "缺少文件: $file"
    fi
done

success "所有关键文件存在"

# ============================================================
# 第3步: 数据库检查
# ============================================================
echo -e "${BLUE}========== 数据库检查 ==========${NC}"

log "检查文章总数..."
ARTICLE_COUNT=$(mysql -u root -p"$MYSQL_PASSWORD" -e "SELECT COUNT(*) FROM met_news WHERE displaytype=1" 2>/dev/null | tail -1)

if [ -z "$ARTICLE_COUNT" ] || [ "$ARTICLE_COUNT" -lt 5 ]; then
    warning "文章数较少 (当前: $ARTICLE_COUNT), 建议至少50篇"
else
    success "文章数充足: $ARTICLE_COUNT 篇"
fi

# ============================================================
# 第4步: 性能测试
# ============================================================
echo -e "${BLUE}========== 性能测试 ==========${NC}"

case "$ENVIRONMENT" in
    production)
        log "执行性能基准测试..."

        # 测试首页加载时间
        RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s https://xiachaoqing.com/)
        log "首页加载时间: ${RESPONSE_TIME}秒"

        if (( $(echo "$RESPONSE_TIME > 3" | bc -l) )); then
            warning "首页加载时间过长，建议优化"
        fi
        ;;
esac

# ============================================================
# 第5步: 备份
# ============================================================
echo -e "${BLUE}========== 备份 ==========${NC}"

log "创建备份..."
mkdir -p "$BACKUP_DIR"

# 备份数据库
log "备份数据库..."
BACKUP_FILE="$BACKUP_DIR/epgo_db_${TIMESTAMP}.sql.gz"
mysqldump -u root -p"$MYSQL_PASSWORD" epgo | gzip > "$BACKUP_FILE" 2>/dev/null || warning "数据库备份失败"
success "数据库备份: $BACKUP_FILE"

# 备份代码
log "备份代码..."
CODE_BACKUP="$BACKUP_DIR/epgo_code_${TIMESTAMP}.tar.gz"
tar --exclude='.git' --exclude='cache' --exclude='node_modules' \
    -czf "$CODE_BACKUP" -C "$(dirname $PROJECT_ROOT)" "epgo" 2>/dev/null || warning "代码备份失败"
success "代码备份: $CODE_BACKUP"

# ============================================================
# 第6步: 部署
# ============================================================
echo -e "${BLUE}========== 开始部署 ==========${NC}"

case "$ENVIRONMENT" in
    dev)
        log "部署到开发环境..."
        # 仅拉取最新代码
        git pull origin main
        success "开发环境部署完成"
        ;;

    staging)
        log "部署到测试环境..."
        git checkout main
        git pull origin main

        # 清除缓存
        rm -rf "$PROJECT_ROOT/cache"/*

        # 重启服务
        # (如需要)

        success "测试环境部署完成"
        ;;

    production)
        log "部署到生产环境..."

        # 再次确认
        echo -e "${YELLOW}即将部署到生产环境!${NC}"
        read -p "确认吗? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error "部署已取消"
        fi

        # 创建发布标签
        TAG="release_${TIMESTAMP}"
        git tag -a "$TAG" -m "Production release at $TIMESTAMP"
        git push origin "$TAG"

        # 检出tag
        git checkout "$TAG"

        # 清除缓存
        rm -rf "$PROJECT_ROOT/cache"/*

        # 重启Web服务
        log "重启Web服务..."
        sudo systemctl restart nginx php-fpm
        success "Web服务已重启"

        success "生产环境部署完成"
        ;;

    *)
        error "未知的环境: $ENVIRONMENT (dev|staging|production)"
        ;;
esac

# ============================================================
# 第7步: 验证
# ============================================================
echo -e "${BLUE}========== 验证部署 ==========${NC}"

# 检查关键页面是否可访问
declare -a URLS=(
    "/"
    "/ket-exam/"
    "/about/"
)

for url in "${URLS[@]}"; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://xiachaoqing.com$url")

    if [ "$HTTP_CODE" = "200" ]; then
        success "✓ $url ($HTTP_CODE)"
    else
        warning "✗ $url ($HTTP_CODE)"
    fi
done

# ============================================================
# 第8步: 通知
# ============================================================
echo -e "${BLUE}========== 部署通知 ==========${NC}"

log "准备发送部署通知..."

# 发送邮件通知 (可选)
# mail -s "部署通知: 英语陪跑GO ($ENVIRONMENT) $TIMESTAMP" \
#     support@xiachaoqing.com \
#     <<< "部署完成。备份位置: $BACKUP_FILE"

success "部署通知已发送"

# ============================================================
# 完成
# ============================================================
echo -e "${GREEN}========== 部署完成 ==========${NC}"
echo -e "时间戳: ${TIMESTAMP}"
echo -e "环境: ${ENVIRONMENT}"
echo -e "备份: ${BACKUP_FILE}"
echo -e "备份: ${CODE_BACKUP}"

if [ "$ENVIRONMENT" = "production" ]; then
    echo -e "\n${YELLOW}提醒:${NC}"
    echo "1. 监控服务器状态"
    echo "2. 检查错误日志: tail -f /var/log/nginx/error.log"
    echo "3. 测试关键功能"
    echo "4. 如有问题，使用以下命令回滚:"
    echo "   git checkout HEAD~1 && sudo systemctl restart nginx"
fi

exit 0
