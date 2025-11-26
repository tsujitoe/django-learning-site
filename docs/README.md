# 📚 文件目錄

歡迎來到 Django Learning Site 的文件中心！

## 🚀 快速開始

新手？從這裡開始：

1. **[快速部署指令](QUICK_DEPLOY.md)** ⚡ - 最快速的部署方法（3 步驟）
2. **[完整部署指南](READY_TO_DEPLOY.md)** 🌟 - 詳細的部署說明和檢查清單

## 📖 設定指南

### 雲端服務設定

- **[Supabase & GCS 設定指南](SUPABASE_GCS_SETUP.md)** 🗄️
  - Supabase PostgreSQL 資料庫設定
  - Google Cloud Storage bucket 建立
  - 權限和安全性設定
  - 常見問題排解

### 資料庫管理

- **[資料庫遷移指南](MIGRATION_GUIDE.md)** 🔄
  - 使用 Cloud Shell 執行遷移
  - 使用 Cloud Run Jobs 執行遷移
  - 本地環境疑難排解
  - 建立超級使用者

### 部署檢查

- **[部署檢查清單](DEPLOYMENT_CHECKLIST.md)** ✅
  - 程式碼檢查結果
  - GitHub Secrets 設定清單
  - 部署後驗證步驟
  - 疑難排解指南

## 🛠️ 工具和腳本

### 自動化腳本

- **[setup-github-secrets.sh](setup-github-secrets.sh)**
  - 使用 GitHub CLI 快速設定 Secrets
  - 需要先安裝 `gh` 命令列工具

- **[pre-deployment-check.sh](pre-deployment-check.sh)**
  - 部署前自動檢查
  - 驗證必要檔案和設定
  - 檢查 Git 狀態

### 測試和遷移工具

- **[test_db_connection.py](test_db_connection.py)**
  - 測試 Supabase 資料庫連線
  - 診斷連線問題
  - 顯示 PostgreSQL 版本

- **[migrate_db.py](migrate_db.py)**
  - 執行資料庫遷移
  - 顯示遷移狀態
  - 錯誤處理和日誌

### 設定檔案

- **[cors.json](cors.json)**
  - GCS Bucket CORS 設定範例
  - 用於跨來源資源共享設定

## 📋 文件地圖

```
docs/
├── README.md                      # 本檔案 - 文件導覽
├── QUICK_DEPLOY.md                # 快速部署（推薦入口）
├── READY_TO_DEPLOY.md             # 完整部署指南（詳細版）
├── SUPABASE_GCS_SETUP.md          # 雲端服務設定
├── MIGRATION_GUIDE.md             # 資料庫遷移
├── DEPLOYMENT_CHECKLIST.md        # 部署檢查清單
├── setup-github-secrets.sh        # GitHub Secrets 設定腳本
├── pre-deployment-check.sh        # 部署前檢查腳本
├── test_db_connection.py          # 資料庫連線測試
├── migrate_db.py                  # 遷移執行腳本
└── cors.json                      # CORS 設定範例
```

## 🎯 依任務選擇文件

### 我想要...

#### 快速部署到生產環境
👉 [QUICK_DEPLOY.md](QUICK_DEPLOY.md)

#### 了解完整部署流程
👉 [READY_TO_DEPLOY.md](READY_TO_DEPLOY.md)

#### 設定 Supabase 資料庫
👉 [SUPABASE_GCS_SETUP.md](SUPABASE_GCS_SETUP.md) - 第 1 節

#### 設定 Google Cloud Storage
👉 [SUPABASE_GCS_SETUP.md](SUPABASE_GCS_SETUP.md) - 第 2 節

#### 執行資料庫遷移
👉 [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

#### 檢查部署是否正確
👉 [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

#### 解決部署問題
👉 [SUPABASE_GCS_SETUP.md](SUPABASE_GCS_SETUP.md) - 第 6 節（常見問題）

#### 設定 GitHub Actions
👉 [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - GitHub Secrets 設定

## 🆘 需要協助？

### 常見問題

1. **本地無法連接 Supabase**
   - 參考 [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - 本地網路問題排查

2. **圖片上傳失敗**
   - 參考 [SUPABASE_GCS_SETUP.md](SUPABASE_GCS_SETUP.md) - 第 6 節 Q&A

3. **GitHub Actions 部署失敗**
   - 檢查 [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - GitHub Secrets

4. **資料庫遷移錯誤**
   - 參考 [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - 疑難排解

### 檢查工具

執行自動檢查腳本（在專案根目錄執行）：
```bash
bash docs/pre-deployment-check.sh
```

測試資料庫連線（在專案根目錄執行）：
```bash
python docs/test_db_connection.py
```

## 📊 文件版本

- **最後更新**: 2025年11月26日
- **適用版本**: Django 4.2.26
- **部署平台**: Google Cloud Run

## 🔄 文件維護

如果您發現文件有誤或需要更新，請：
1. 在 GitHub 開 Issue
2. 提交 Pull Request
3. 聯繫維護者

---

**返回 [專案首頁](../README.md)**
