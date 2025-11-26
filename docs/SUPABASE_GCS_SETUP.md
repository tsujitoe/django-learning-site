# Supabase 和 Google Cloud Storage 設定指南

本指南將協助您設定 Supabase PostgreSQL 資料庫和 Google Cloud Storage 用於圖片儲存。

## 前置作業

已在 `requirements.txt` 中加入以下套件：
- `psycopg2-binary` - PostgreSQL 資料庫驅動程式
- `django-storages` - Django 雲端儲存後端
- `google-cloud-storage` - Google Cloud Storage 客戶端函式庫

## 1. 設定 Supabase 資料庫

### 1.1 建立 Supabase 專案

1. 前往 [Supabase](https://supabase.com/) 並登入
2. 點選 "New Project" 建立新專案
3. 填寫專案資訊：
   - Name: 您的專案名稱
   - Database Password: 設定一個強密碼（請記住此密碼）
   - Region: 選擇 `Northeast Asia (Tokyo)` 或最近的區域

### 1.2 取得資料庫連線資訊

1. 在 Supabase 專案頁面，點選左側選單的 "Settings" > "Database"
2. 在 "Connection string" 區段，選擇 "URI" 模式
3. 複製連線字串，格式如下：
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```

4. 從連線字串中提取以下資訊：
   - **SUPABASE_DB_HOST**: `db.[YOUR-PROJECT-REF].supabase.co`
   - **SUPABASE_DB_USER**: `postgres`
   - **SUPABASE_DB_PASSWORD**: 您在建立專案時設定的密碼
   - **SUPABASE_DB_NAME**: `postgres`
   - **SUPABASE_DB_PORT**: `5432`

### 1.3 在 Cloud Run 設定環境變數

在 Cloud Run 服務中設定以下環境變數：

```bash
gcloud run services update YOUR-SERVICE-NAME \
  --update-env-vars \
    USE_SUPABASE=True,\
    SUPABASE_DB_NAME=postgres,\
    SUPABASE_DB_USER=postgres,\
    SUPABASE_DB_PASSWORD=YOUR-PASSWORD,\
    SUPABASE_DB_HOST=db.YOUR-PROJECT-REF.supabase.co,\
    SUPABASE_DB_PORT=5432 \
  --region=YOUR-REGION
```

或透過 GCP Console：
1. 前往 Cloud Run 服務頁面
2. 點選您的服務
3. 點選上方的 "EDIT & DEPLOY NEW REVISION"
4. 在 "Variables & Secrets" > "Environment Variables" 加入上述變數

## 2. 設定 Google Cloud Storage

### 2.1 建立 Storage Bucket

```bash
# 建立 bucket (名稱必須全域唯一)
gsutil mb -l asia-northeast1 gs://YOUR-BUCKET-NAME

# 設定 bucket 為公開讀取（讓圖片可以公開訪問）
gsutil iam ch allUsers:objectViewer gs://YOUR-BUCKET-NAME

# 或者設定更細緻的 CORS 規則
gsutil cors set cors.json gs://YOUR-BUCKET-NAME
```

### 2.2 建立 CORS 設定檔（可選）

建立 `cors.json` 檔案：

```json
[
  {
    "origin": ["*"],
    "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
```

### 2.3 設定 Cloud Run 的服務帳號權限

```bash
# 取得 Cloud Run 服務的服務帳號
SERVICE_ACCOUNT=$(gcloud run services describe django-service \
  --region=asia-east1 \
  --format='value(spec.template.spec.serviceAccountName)')

# 授予 Storage 物件管理權限
gsutil iam ch serviceAccount:${SERVICE_ACCOUNT}:objectAdmin gs://your-bucket-name
```

或透過 GCP Console：
1. 前往 Cloud Storage > Browser
2. 點選您的 bucket
3. 前往 "Permissions" 標籤
4. 點選 "ADD PRINCIPAL"
5. 加入 Cloud Run 服務帳號並給予 "Storage Object Admin" 角色

### 2.4 在 Cloud Run 設定環境變數

```bash
gcloud run services update YOUR-SERVICE-NAME \
  --update-env-vars \
    USE_GCS=True,\
    GCS_BUCKET_NAME=YOUR-BUCKET-NAME \
  --region=YOUR-REGION
```

**注意**：Cloud Run 服務會自動使用其服務帳號的權限，不需要額外設定 `GCS_CREDENTIALS`。

## 3. 執行資料庫遷移

部署更新後，需要執行資料庫遷移：

### 方法 1: 使用 Cloud Run Jobs（推薦）

```bash
# 建立一次性的 migration job
gcloud run jobs create django-migrate \
  --image=YOUR-IMAGE-URL \
  --command=python \
  --args="manage.py,migrate" \
  --set-env-vars="$(gcloud run services describe YOUR-SERVICE-NAME --region=YOUR-REGION --format='value(spec.template.spec.containers[0].env)')" \
  --region=YOUR-REGION

# 執行 migration
gcloud run jobs execute django-migrate --region=YOUR-REGION
```

### 方法 2: 使用 Cloud Shell

```bash
# 連線到 Supabase 資料庫
psql "postgresql://postgres:YOUR-PASSWORD@db.YOUR-PROJECT-REF.supabase.co:5432/postgres"

# 或使用本地環境執行遷移
# 先設定環境變數，然後執行
python manage.py migrate
```

### 方法 3: 建立超級使用者

```bash
# 同樣使用 Cloud Run Jobs 或本地環境
python manage.py createsuperuser
```

## 4. 驗證設定

### 4.1 檢查資料庫連線

```bash
# 在 Cloud Shell 或本地執行
python manage.py dbshell
```

### 4.2 測試圖片上傳

1. 登入 Django Admin
2. 前往圖片上傳頁面
3. 上傳一張測試圖片
4. 檢查圖片是否成功儲存到 GCS bucket
5. 確認圖片 URL 是否為 `https://storage.googleapis.com/YOUR-BUCKET-NAME/...`

## 5. 本地開發設定

本地開發時，建議使用 SQLite 和本地檔案儲存：

在本地 `.env` 檔案中：
```env
SECRET_KEY=your-secret-key
DEBUG=True
USE_SUPABASE=False
USE_GCS=False
```

這樣可以在不影響生產環境的情況下進行開發。

## 6. 常見問題

### Q: 無法連線到 Supabase 資料庫
- 檢查防火牆設定是否允許連線
- 確認密碼正確
- 檢查連線字串格式

### Q: 圖片上傳失敗
- 確認 Cloud Run 服務帳號有 Storage Object Admin 權限
- 檢查 bucket 名稱是否正確
- 查看 Cloud Run 日誌了解錯誤訊息

### Q: 遷移失敗
- 確認資料庫連線正常
- 檢查是否已安裝 `psycopg2-binary`
- 查看完整錯誤訊息

## 7. 安全性建議

1. **不要在程式碼中硬編碼敏感資訊**
2. **使用 Secret Manager 管理密碼**：
   ```bash
   # 建立 secret
   echo -n "YOUR-PASSWORD" | gcloud secrets create supabase-db-password --data-file=-
   
   # 授予 Cloud Run 服務帳號讀取權限
   gcloud secrets add-iam-policy-binding supabase-db-password \
     --member=serviceAccount:YOUR-SERVICE-ACCOUNT \
     --role=roles/secretmanager.secretAccessor
   ```

3. **定期更換密碼**
4. **限制 bucket 的公開存取範圍**
5. **啟用 Cloud Armor 保護您的服務**

## 8. 成本估算

- **Supabase**: 免費方案包含 500MB 資料庫空間，2GB 檔案儲存
- **Google Cloud Storage**: 
  - 儲存：約 $0.02/GB/月 (Standard Storage in Asia)
  - 網路傳輸：免費（Cloud Run 到 GCS 同區域）
- **Cloud Run**: 按使用量計費

## 9. 監控和維護

建議設定以下監控：
- Supabase Dashboard: 監控資料庫使用量和效能
- GCP Monitoring: 監控 Storage 使用量和請求數
- Cloud Run Logs: 監控應用程式日誌和錯誤

## 完成！

設定完成後，您的 Django 應用程式將：
- ✅ 使用 Supabase PostgreSQL 作為生產資料庫
- ✅ 使用 Google Cloud Storage 儲存用戶上傳的圖片
- ✅ 在 Cloud Run 上穩定執行
- ✅ 本地開發時使用 SQLite 和本地儲存

如有任何問題，請查看 Cloud Run 和 Supabase 的日誌以取得詳細錯誤資訊。
