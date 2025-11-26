# 🚀 快速部署指令參考

## 立即部署（3 步驟）

### 1️⃣ 設定 GitHub Secrets
前往: https://github.com/tsujitoe/django-learning-site/settings/secrets/actions

需要設定的 Secrets (8 個):
```
GCP_PROJECT_ID          = your-gcp-project-id
SECRET_KEY              = your-django-secret-key
SUPABASE_DB_NAME        = postgres
SUPABASE_DB_USER        = postgres  
SUPABASE_DB_PASSWORD    = your-supabase-password
SUPABASE_DB_HOST        = db.your-project-ref.supabase.co
GCS_BUCKET_NAME         = your-bucket-name
GCP_SA_KEY              = (服務帳號 JSON - 完整內容)
```

### 2️⃣ 提交並推送
```bash
git add .
git commit -m "feat: 新增 Supabase 和 GCS 支援"
git push origin feature/test-ci
```

### 3️⃣ 合併到 main 觸發部署
```bash
git checkout main
git merge feature/test-ci  
git push origin main
```

---

## 部署後執行遷移（Cloud Shell）

```bash
# 替換為您的實際值
export USE_SUPABASE=True SUPABASE_DB_NAME=postgres SUPABASE_DB_USER=postgres \
SUPABASE_DB_PASSWORD='your-supabase-password' SUPABASE_DB_HOST=db.your-project-ref.supabase.co \
SECRET_KEY='your-django-secret-key' USE_GCS=False

git clone https://github.com/tsujitoe/django-learning-site.git
cd django-learning-site
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

---

## 建立 GCP 服務帳號金鑰（如果需要）

```bash
gcloud iam service-accounts create github-actions --display-name="GitHub Actions"

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

gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com

cat key.json  # 複製到 GitHub Secret GCP_SA_KEY
rm key.json
```

---

## 常用監控指令

```bash
# 查看 Cloud Run 日誌
gcloud run services logs read django-service --region=asia-east1 --limit=50

# 查看服務狀態
gcloud run services describe django-service --region=asia-east1

# 查看環境變數
gcloud run services describe django-service --region=asia-east1 \
  --format='value(spec.template.spec.containers[0].env)'

# 查看 GCS bucket 內容
gsutil ls -r gs://your-bucket-name
```

---

## 網站 URL
https://django-service-jukgut67fa-de.a.run.app

---

## 需要協助？
📖 詳細文件: READY_TO_DEPLOY.md
📖 設定指南: SUPABASE_GCS_SETUP.md  
📖 遷移指南: MIGRATION_GUIDE.md
