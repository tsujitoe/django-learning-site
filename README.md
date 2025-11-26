# Django Learning Site

一個整合 CI/CD、雲端資料庫和儲存的 Django 專案。

## 🚀 專案特色

- ✅ **自動化 CI/CD** - GitHub Actions 自動測試與部署
- ✅ **雲端資料庫** - Supabase PostgreSQL
- ✅ **雲端儲存** - Google Cloud Storage 圖片儲存
- ✅ **容器化部署** - Docker + Google Cloud Run
- ✅ **使用者認證** - Django Allauth (Email 登入)
- ✅ **圖片管理** - 圖片上傳、瀏覽、刪除功能

## 📋 技術堆疊

- **後端框架**: Django 4.2.26
- **資料庫**: Supabase PostgreSQL (生產) / SQLite (開發)
- **檔案儲存**: Google Cloud Storage (生產) / 本地儲存 (開發)
- **Web 伺服器**: Gunicorn
- **部署平台**: Google Cloud Run
- **CI/CD**: GitHub Actions
- **容器化**: Docker

## 🏗️ 專案結構

```
django-learning-site/
├── docs/                           # 📚 文件資料夾
│   ├── READY_TO_DEPLOY.md         # 部署準備指南
│   ├── QUICK_DEPLOY.md            # 快速部署指令
│   ├── SUPABASE_GCS_SETUP.md      # Supabase 和 GCS 設定
│   ├── MIGRATION_GUIDE.md         # 資料庫遷移指南
│   ├── DEPLOYMENT_CHECKLIST.md    # 部署檢查清單
│   ├── setup-github-secrets.sh    # GitHub Secrets 設定腳本
│   ├── pre-deployment-check.sh    # 部署前檢查腳本
│   ├── test_db_connection.py      # 資料庫連線測試
│   └── migrate_db.py              # 資料庫遷移腳本
├── mysite/                         # Django 專案設定
│   ├── settings.py                # 設定檔（支援環境變數）
│   ├── storage_backends.py        # GCS 儲存後端
│   └── urls.py
├── gallery/                        # 圖片管理應用
│   ├── models.py                  # Image 模型
│   ├── views.py                   # 圖片 CRUD 視圖
│   ├── forms.py                   # 圖片上傳表單
│   └── templates/
├── pages/                          # 靜態頁面應用
├── templates/                      # 全域模板
├── .github/workflows/              # GitHub Actions
│   └── django.yml                 # CI/CD 工作流程
├── Dockerfile                      # Docker 映像定義
├── requirements.txt                # Python 相依套件
├── manage.py                       # Django 管理指令
└── README.md                       # 本檔案

```

## 🚀 快速開始

### 本地開發

1. **Clone 專案**
```bash
git clone https://github.com/tsujitoe/django-learning-site.git
cd django-learning-site
```

2. **建立虛擬環境**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **安裝相依套件**
```bash
pip install -r requirements.txt
```

4. **設定環境變數**
```bash
# 建立 .env 檔案
cp .env.example .env

# 編輯 .env 設定本地開發環境
SECRET_KEY=your-secret-key
DEBUG=True
USE_SUPABASE=False  # 本地使用 SQLite
USE_GCS=False       # 本地使用檔案系統
```

5. **執行遷移並啟動開發伺服器**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

6. **訪問網站**
- 網站: http://localhost:8000
- Admin: http://localhost:8000/admin

### 執行測試

```bash
python manage.py test
```

## 🌐 部署到 Google Cloud Run

### 前置需求

- Google Cloud Platform 帳號
- Supabase 帳號
- GitHub Repository

### 快速部署

詳細部署步驟請參考：

1. **📖 [快速部署指令](docs/QUICK_DEPLOY.md)** - 3 步驟完成部署
2. **📖 [完整部署指南](docs/READY_TO_DEPLOY.md)** - 詳細的部署說明
3. **📖 [Supabase & GCS 設定](docs/SUPABASE_GCS_SETUP.md)** - 資料庫和儲存設定
4. **📖 [資料庫遷移指南](docs/MIGRATION_GUIDE.md)** - 遷移執行方法

### 部署概要

1. **設定 GitHub Secrets** (8 個必要的 Secrets)
2. **推送程式碼到 main 分支** - 自動觸發 CI/CD
3. **執行資料庫遷移** - 使用 Cloud Shell

詳細步驟請參考 [docs/QUICK_DEPLOY.md](docs/QUICK_DEPLOY.md)

## 📚 文件導覽

| 文件 | 說明 |
|------|------|
| [READY_TO_DEPLOY.md](docs/READY_TO_DEPLOY.md) | 🌟 完整部署指南 - 從設定到上線 |
| [QUICK_DEPLOY.md](docs/QUICK_DEPLOY.md) | ⚡ 快速部署指令參考 |
| [SUPABASE_GCS_SETUP.md](docs/SUPABASE_GCS_SETUP.md) | 🗄️ Supabase 和 GCS 詳細設定 |
| [MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) | 🔄 資料庫遷移執行指南 |
| [DEPLOYMENT_CHECKLIST.md](docs/DEPLOYMENT_CHECKLIST.md) | ✅ 部署前檢查清單 |

## 🔧 環境變數

### 必要環境變數

```env
# Django 基本設定
SECRET_KEY=your-secret-key
DEBUG=False

# Supabase 資料庫
USE_SUPABASE=True
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password
SUPABASE_DB_HOST=db.xxx.supabase.co
SUPABASE_DB_PORT=5432

# Google Cloud Storage
USE_GCS=True
GCS_BUCKET_NAME=your-bucket-name
```

完整環境變數說明請參考 [.env.example](.env.example)

## 🛠️ 開發工作流程

### 分支策略

- `main` - 生產環境，推送後自動部署
- `feature/*` - 功能開發分支

### CI/CD 流程

1. **推送到任何分支** → 執行測試
2. **推送到 main** → 執行測試 + 自動部署到 Cloud Run

### 本地開發最佳實踐

- 使用 SQLite 和本地儲存（`USE_SUPABASE=False`, `USE_GCS=False`）
- 定期執行測試: `python manage.py test`
- 提交前檢查: `python manage.py check`

## 📊 功能特色

### 使用者功能

- ✅ Email 註冊/登入/登出
- ✅ 密碼重設
- ✅ 個人圖片管理

### 圖片管理

- ✅ 圖片上傳（支援標題和描述）
- ✅ 圖片列表瀏覽（分頁）
- ✅ 圖片詳細頁面
- ✅ 刪除自己的圖片
- ✅ 圖片儲存到 GCS

### 管理功能

- ✅ Django Admin 完整管理介面
- ✅ 使用者管理
- ✅ 圖片內容管理

## 🔍 監控和除錯

### 查看 Cloud Run 日誌
```bash
gcloud run services logs read django-service --region=asia-east1 --limit=50
```

### 查看服務狀態
```bash
gcloud run services describe django-service --region=asia-east1
```

### 查看 GCS Bucket
```bash
gsutil ls -r gs://your-bucket-name
```

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📝 授權

本專案採用 MIT 授權。

## 📞 聯絡資訊

- GitHub: [@tsujitoe](https://github.com/tsujitoe)
- 專案網址: [部署後自動生成]

## 🎉 致謝

感謝所有開源專案的貢獻者！

---

**Built with ❤️ using Django, Supabase, and Google Cloud**