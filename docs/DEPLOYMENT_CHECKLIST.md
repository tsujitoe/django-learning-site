# GitHub Actions 部署前檢查清單

## ✅ 程式碼檢查結果

### 1. Django 應用程式
- ✅ `manage.py check` - 無錯誤
- ✅ 測試執行 - 17 個測試全部通過
- ✅ `settings.py` - 正確配置 Supabase 和 GCS
- ✅ `storage_backends.py` - GCS 儲存後端已建立
- ✅ `requirements.txt` - 包含所有必要套件
- ✅ `Dockerfile` - 正確配置

### 2. 相依套件
```
✅ Django 4.2.26
✅ psycopg2-binary 2.9.10 (PostgreSQL)
✅ django-storages 1.14.4
✅ google-cloud-storage 2.18.2
✅ gunicorn 23.0.0
✅ 其他必要套件
```

### 3. GitHub Actions 工作流程
- ✅ 測試任務 (test job)
- ✅ 部署任務 (deploy job)
- ✅ Docker 建置和推送
- ✅ Cloud Run 部署
- ✅ 環境變數配置

## 📝 需要在 GitHub 設定的 Secrets

在上傳到 GitHub 之前，您需要在 GitHub Repository 設定以下 Secrets：

### 前往設定頁面
1. 開啟您的 GitHub Repository
2. 點選 **Settings** > **Secrets and variables** > **Actions**
3. 點選 **New repository secret** 來新增每個 secret

### 必要的 Secrets

| Secret 名稱 | 值 | 說明 |
|------------|---|------|
| `GCP_PROJECT_ID` | `YOUR_PROJECT_ID` | GCP 專案 ID |
| `GCP_SA_KEY` | (JSON 內容) | GCP 服務帳號金鑰 (完整 JSON) |
| `SECRET_KEY` | `your-django-secret-key` | Django Secret Key |
| `SUPABASE_DB_NAME` | `postgres` | Supabase 資料庫名稱 |
| `SUPABASE_DB_USER` | `postgres` | Supabase 資料庫使用者 |
| `SUPABASE_DB_PASSWORD` | `your-supabase-password` | Supabase 資料庫密碼 |
| `SUPABASE_DB_HOST` | `db.your-project-ref.supabase.co` | Supabase 主機 |
| `GCS_BUCKET_NAME` | `your-bucket-name` | GCS Bucket 名稱 |

### 如何取得 GCP_SA_KEY

如果您還沒有服務帳號金鑰，執行以下步驟：

```bash
# 1. 建立服務帳號
gcloud iam service-accounts create github-actions \
    --description="GitHub Actions 部署用" \
    --display-name="GitHub Actions"

# 2. 授予必要權限
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# 3. 建立並下載金鑰
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com

# 4. 查看金鑰內容（複製整個 JSON）
cat github-actions-key.json

# ⚠️ 重要：設定完成後刪除本地金鑰檔案
rm github-actions-key.json
```

將完整的 JSON 內容貼到 GitHub Secret `GCP_SA_KEY` 中。

## 🚀 部署流程

### 自動部署（推薦）

1. ✅ 確認所有 GitHub Secrets 已設定
2. ✅ 將程式碼推送到 `main` 分支
3. GitHub Actions 會自動：
   - 執行測試
   - 建置 Docker 映像
   - 部署到 Cloud Run

```bash
git add .
git commit -m "feat: 新增 Supabase 和 GCS 支援"
git push origin feature/test-ci

# 如果在 main 分支
git checkout main
git merge feature/test-ci
git push origin main
```

### 手動驗證

部署完成後：

1. 查看 GitHub Actions 日誌
2. 訪問您的網站：`https://django-service-jukgut67fa-de.a.run.app`
3. 執行資料庫遷移（參考 MIGRATION_GUIDE.md）
4. 測試圖片上傳功能

## 🔍 troubleshooting

### 問題 1: GitHub Actions 失敗
- 檢查所有 Secrets 是否正確設定
- 查看 Actions 日誌了解具體錯誤

### 問題 2: 部署成功但網站無法訪問
- 檢查 Cloud Run 日誌：`gcloud run services logs read django-service --region=asia-east1`
- 確認環境變數是否正確設定

### 問題 3: 資料庫連線錯誤
- 確認 Supabase 密碼正確
- 檢查 Supabase 專案是否在執行中
- 參考 MIGRATION_GUIDE.md 執行遷移

### 問題 4: 圖片上傳失敗
- 確認 GCS Bucket 存在
- 檢查 Cloud Run 服務帳號權限
- 查看 Cloud Run 日誌

## 📊 部署後檢查清單

- [ ] GitHub Actions 成功執行
- [ ] Cloud Run 服務正常執行
- [ ] 網站可以訪問
- [ ] 資料庫遷移已完成
- [ ] 可以登入 Django Admin
- [ ] 圖片上傳功能正常
- [ ] 圖片儲存在 GCS bucket
- [ ] 圖片可以正常顯示

## 🎉 完成！

一切設定完成後，您的應用程式將：
- ✅ 自動測試每次提交
- ✅ 自動部署到 Cloud Run (main 分支)
- ✅ 使用 Supabase PostgreSQL
- ✅ 使用 Google Cloud Storage 儲存圖片
- ✅ 透過 HTTPS 安全訪問

## 📞 需要協助？

如果遇到問題：
1. 查看 GitHub Actions 日誌
2. 查看 Cloud Run 日誌
3. 參考 SUPABASE_GCS_SETUP.md
4. 參考 MIGRATION_GUIDE.md
