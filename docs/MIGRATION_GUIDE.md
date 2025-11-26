# 資料庫遷移執行指南

由於本地環境的 IPv6 網路問題，請使用以下方法之一執行資料庫遷移：

## 方法 1: 使用 Google Cloud Shell（推薦）

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 點選右上角的 Cloud Shell 圖示（>_）啟動 Cloud Shell
3. 在 Cloud Shell 中執行以下指令：

```bash
# 設定環境變數
export USE_SUPABASE=True
export SUPABASE_DB_NAME=postgres
export SUPABASE_DB_USER=postgres
export SUPABASE_DB_PASSWORD='your-supabase-password'
export SUPABASE_DB_HOST=db.your-project-ref.supabase.co
export SUPABASE_DB_PORT=5432
export SECRET_KEY='your-django-secret-key'
export DEBUG=False

# Clone 您的專案（或下載）
git clone https://github.com/tsujitoe/django-learning-site.git
cd django-learning-site

# 安裝 Python 相依套件
pip install -r requirements.txt

# 執行遷移
python manage.py migrate

# 建立超級使用者（可選）
python manage.py createsuperuser
```

## 方法 2: 使用 Cloud Run Jobs

建立一個一次性的 Job 來執行遷移：

```bash
# 首先需要重新建置包含新套件的 Docker 映像
# 授予 Cloud Build 權限
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member=user:your-email@gmail.com \
    --role=roles/cloudbuild.builds.editor

# 重新建置映像
gcloud builds submit --tag asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/my-repo/django-app:latest

# 更新 Cloud Run 服務使用新映像
gcloud run services update django-service \
    --image asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/my-repo/django-app:latest \
    --region=asia-east1

# 建立遷移 Job
gcloud run jobs create django-migrate \
    --image=asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/my-repo/django-app:latest \
    --command=python \
    --args="manage.py,migrate" \
    --set-env-vars="USE_SUPABASE=True,SUPABASE_DB_NAME=postgres,SUPABASE_DB_USER=postgres,SUPABASE_DB_PASSWORD=your-supabase-password,SUPABASE_DB_HOST=db.your-project-ref.supabase.co,SUPABASE_DB_PORT=5432,SECRET_KEY=your-django-secret-key,DEBUG=False" \
    --region=asia-east1

# 執行遷移
gcloud run jobs execute django-migrate --region=asia-east1
```

## 方法 3: 使用 psql 直接連線（驗證設定）

如果您已安裝 PostgreSQL 客戶端：

```bash
# 直接連線到 Supabase
psql "postgresql://postgres:your-supabase-password@db.your-project-ref.supabase.co:5432/postgres?sslmode=require"

# 或使用分開的參數
psql -h db.your-project-ref.supabase.co -p 5432 -U postgres -d postgres
# 密碼: your-supabase-password
```

## 方法 4: 在 Supabase 控制台檢查

1. 前往 [Supabase Dashboard](https://supabase.com/dashboard/project/your-project-ref)
2. 點選 "Table Editor" 或 "SQL Editor"
3. 確認資料庫連線正常
4. 您可以在這裡查看遷移後建立的資料表

## 本地網路問題排查

如果您想在本地執行，可以嘗試：

### 選項 A: 使用 IPv4 強制連線

修改 Windows hosts 檔案（需要管理員權限）：
```
C:\Windows\System32\drivers\etc\hosts
```

加入：
```
# 取得 IPv4 位址後再加入
# xxx.xxx.xxx.xxx db.your-project-ref.supabase.co
```

### 選項 B: 啟用 IPv6

1. 檢查 IPv6 是否啟用：
```bash
ipconfig
```

2. 如果沒有 IPv6 位址，聯絡您的 ISP 或網路管理員

### 選項 C: 使用 VPN 或代理

某些 VPN 服務可能會影響 IPv6 連線，嘗試：
- 關閉 VPN
- 切換到不同的網路（例如手機熱點）

## 驗證遷移成功

遷移完成後，訪問您的網站：
```
https://django-service-jukgut67fa-de.a.run.app/admin
```

應該能看到 Django Admin 登入頁面，這表示資料庫遷移成功。

## 下一步

遷移成功後：
1. ✅ 建立超級使用者帳號
2. ✅ 測試圖片上傳功能
3. ✅ 確認圖片儲存到 GCS bucket

## 需要協助？

如果遇到問題，請檢查：
- Cloud Run 日誌：`gcloud run services logs read django-service --region=asia-east1`
- Supabase 連線狀態
- 環境變數設定
