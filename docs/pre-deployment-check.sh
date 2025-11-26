#!/bin/bash

# 部署前最終檢查腳本
# 確保所有設定正確無誤

echo "=================================="
echo "部署前最終檢查"
echo "=================================="
echo ""

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# 檢查函式
check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
    ((ERRORS++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

echo "1. 檢查必要檔案..."
if [ -f "manage.py" ]; then
    check_pass "manage.py 存在"
else
    check_fail "manage.py 不存在"
fi

if [ -f "requirements.txt" ]; then
    check_pass "requirements.txt 存在"
else
    check_fail "requirements.txt 不存在"
fi

if [ -f "Dockerfile" ]; then
    check_pass "Dockerfile 存在"
else
    check_fail "Dockerfile 不存在"
fi

if [ -f ".github/workflows/django.yml" ]; then
    check_pass "GitHub Actions 工作流程存在"
else
    check_fail "GitHub Actions 工作流程不存在"
fi

echo ""
echo "2. 檢查 requirements.txt 必要套件..."
if grep -q "psycopg2-binary" requirements.txt; then
    check_pass "psycopg2-binary (PostgreSQL 驅動) 已包含"
else
    check_fail "psycopg2-binary 未包含"
fi

if grep -q "django-storages" requirements.txt; then
    check_pass "django-storages 已包含"
else
    check_fail "django-storages 未包含"
fi

if grep -q "google-cloud-storage" requirements.txt; then
    check_pass "google-cloud-storage 已包含"
else
    check_fail "google-cloud-storage 未包含"
fi

if grep -q "gunicorn" requirements.txt; then
    check_pass "gunicorn 已包含"
else
    check_fail "gunicorn 未包含"
fi

echo ""
echo "3. 檢查 .env 檔案..."
if [ -f ".env" ]; then
    check_pass ".env 檔案存在"
    
    if grep -q "SECRET_KEY=" .env; then
        check_pass "SECRET_KEY 已設定"
    else
        check_fail "SECRET_KEY 未設定"
    fi
    
    if grep -q "SUPABASE_DB_HOST=" .env; then
        check_pass "Supabase 設定存在"
    else
        check_warn "Supabase 設定不存在（如果不使用可忽略）"
    fi
    
    if grep -q "GCS_BUCKET_NAME=" .env; then
        check_pass "GCS Bucket 設定存在"
    else
        check_warn "GCS Bucket 設定不存在（如果不使用可忽略）"
    fi
else
    check_warn ".env 檔案不存在（生產環境使用 Cloud Run 環境變數）"
fi

echo ""
echo "4. 檢查 Git 狀態..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    check_pass "Git repository 已初始化"
    
    # 檢查是否有未提交的變更
    if git diff-index --quiet HEAD --; then
        check_pass "沒有未提交的變更"
    else
        check_warn "有未提交的變更"
        echo "   執行: git status 查看詳情"
    fi
    
    # 檢查遠端設定
    if git remote -v | grep -q "github.com"; then
        check_pass "GitHub 遠端已設定"
    else
        check_warn "GitHub 遠端未設定"
    fi
else
    check_fail "不是 Git repository"
fi

echo ""
echo "5. 檢查 GitHub Secrets（需要 GitHub CLI）..."
if command -v gh &> /dev/null; then
    if gh auth status &> /dev/null 2>&1; then
        check_pass "GitHub CLI 已登入"
        
        # 檢查 secrets（這會列出 secret 名稱但不會顯示值）
        secrets=$(gh secret list 2>/dev/null | awk '{print $1}')
        
        required_secrets=("GCP_PROJECT_ID" "GCP_SA_KEY" "SECRET_KEY" "SUPABASE_DB_NAME" "SUPABASE_DB_USER" "SUPABASE_DB_PASSWORD" "SUPABASE_DB_HOST" "GCS_BUCKET_NAME")
        
        for secret in "${required_secrets[@]}"; do
            if echo "$secrets" | grep -q "^$secret$"; then
                check_pass "$secret 已設定"
            else
                check_fail "$secret 未設定"
            fi
        done
    else
        check_warn "GitHub CLI 未登入（執行: gh auth login）"
    fi
else
    check_warn "GitHub CLI 未安裝（無法檢查 Secrets）"
fi

echo ""
echo "=================================="
echo "檢查結果總結"
echo "=================================="
echo -e "錯誤: ${RED}$ERRORS${NC}"
echo -e "警告: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 所有檢查通過！可以進行部署。${NC}"
    echo ""
    echo "下一步："
    echo "  1. git add ."
    echo "  2. git commit -m \"feat: 新增 Supabase 和 GCS 支援\""
    echo "  3. git push origin feature/test-ci"
    echo "  4. 合併到 main 分支以觸發自動部署"
    exit 0
else
    echo -e "${RED}❌ 發現 $ERRORS 個錯誤，請修正後再部署。${NC}"
    exit 1
fi
