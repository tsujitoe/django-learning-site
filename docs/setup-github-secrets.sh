#!/bin/bash

# GitHub Secrets 設定腳本
# 此腳本幫助您快速設定 GitHub Repository Secrets

echo "=================================="
echo "GitHub Secrets 設定助手"
echo "=================================="
echo ""

# 檢查是否安裝 GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ 錯誤：未安裝 GitHub CLI (gh)"
    echo "請安裝 GitHub CLI: https://cli.github.com/"
    echo ""
    echo "安裝方法："
    echo "  Windows: winget install --id GitHub.cli"
    echo "  macOS: brew install gh"
    echo "  Linux: 請參考官方文件"
    exit 1
fi

echo "✅ 已偵測到 GitHub CLI"
echo ""

# 檢查是否已登入
if ! gh auth status &> /dev/null; then
    echo "請先登入 GitHub："
    gh auth login
fi

echo ""
echo "正在設定 GitHub Secrets..."
echo ""

# 設定 Secrets
echo "1. 設定 GCP_PROJECT_ID..."
gh secret set GCP_PROJECT_ID --body "your-gcp-project-id"

echo "2. 設定 SECRET_KEY..."
gh secret set SECRET_KEY --body "your-django-secret-key"

echo "3. 設定 SUPABASE_DB_NAME..."
gh secret set SUPABASE_DB_NAME --body "postgres"

echo "4. 設定 SUPABASE_DB_USER..."
gh secret set SUPABASE_DB_USER --body "postgres"

echo "5. 設定 SUPABASE_DB_PASSWORD..."
gh secret set SUPABASE_DB_PASSWORD --body "your-supabase-password"

echo "6. 設定 SUPABASE_DB_HOST..."
gh secret set SUPABASE_DB_HOST --body "db.your-project-ref.supabase.co"

echo "7. 設定 GCS_BUCKET_NAME..."
gh secret set GCS_BUCKET_NAME --body "your-bucket-name"

echo ""
echo "⚠️  還需要手動設定 GCP_SA_KEY"
echo ""
echo "請執行以下步驟："
echo ""
echo "1. 建立服務帳號金鑰："
echo "   gcloud iam service-accounts keys create key.json \\"
echo "     --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com"
echo ""
echo "2. 設定 GitHub Secret："
echo "   gh secret set GCP_SA_KEY < key.json"
echo ""
echo "3. 刪除本地金鑰："
echo "   rm key.json"
echo ""
echo "=================================="
echo "✅ 大部分 Secrets 已設定完成"
echo "=================================="
echo ""
echo "請完成 GCP_SA_KEY 設定後，即可推送程式碼進行部署。"
