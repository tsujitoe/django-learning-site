# Django 圖片庫專案 - Google 登入與圖片上傳功能

## 功能說明

此專案實作了以下功能：

1. **Google 帳號登入** - 使用 django-allauth 整合 Google OAuth2 認證
2. **圖片上傳** - 登入使用者可以上傳圖片並填寫標題與描述
3. **圖片瀏覽** - 所有人都可以瀏覽圖片庫
4. **圖片管理** - 使用者可以查看和刪除自己上傳的圖片
5. **完整測試** - 包含模型、視圖、表單的單元測試

## 專案結構

```
django-learning-site/
├── mysite/                 # 專案設定
│   ├── settings.py         # 包含 allauth 和 media 設定
│   └── urls.py             # 主要 URL 配置
├── gallery/                # 圖片庫應用程式
│   ├── models.py           # Image 模型
│   ├── views.py            # 視圖函式
│   ├── forms.py            # 圖片上傳表單
│   ├── urls.py             # gallery URL 配置
│   ├── admin.py            # 管理後台設定
│   ├── tests.py            # 單元測試
│   └── templates/gallery/  # HTML 模板
├── templates/              # 共用模板
│   └── base.html           # 基礎模板
├── media/                  # 使用者上傳的圖片（自動建立）
└── requirements.txt        # Python 相依套件
```

## 安裝步驟

### 1. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

在專案根目錄建立 `.env` 檔案，加入以下內容：

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

# Google OAuth 設定（稍後設定）
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

### 3. 執行資料庫遷移

```bash
python manage.py migrate
```

### 4. 建立超級使用者

```bash
python manage.py createsuperuser
```

### 5. 執行開發伺服器

```bash
python manage.py runserver
```

## Google OAuth 設定

### 1. 建立 Google Cloud 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 "Google+ API"

### 2. 設定 OAuth 同意畫面

1. 在左側選單選擇「API和服務」→「OAuth 同意畫面」
2. 選擇「外部」使用者類型
3. 填寫應用程式名稱和支援電子郵件
4. 儲存並繼續

### 3. 建立 OAuth 2.0 憑證

1. 在左側選單選擇「API和服務」→「憑證」
2. 點擊「建立憑證」→「OAuth 用戶端 ID」
3. 應用程式類型選擇「網頁應用程式」
4. 新增授權重新導向 URI：
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - `http://localhost:8000/accounts/google/login/callback/`
5. 建立後會取得 Client ID 和 Client Secret

### 4. 在 Django 管理後台設定

1. 前往 http://127.0.0.1:8000/admin/
2. 登入管理後台
3. 找到「Sites」→ 點擊「example.com」
   - Domain name: `127.0.0.1:8000`
   - Display name: `localhost`
   - 儲存
4. 找到「Social applications」→「新增」
   - Provider: `Google`
   - Name: `Google OAuth`
   - Client id: 貼上從 Google 取得的 Client ID
   - Secret key: 貼上從 Google 取得的 Client Secret
   - Sites: 選擇「127.0.0.1:8000」並加到右側
   - 儲存

### 5. 更新 .env 檔案（選用）

將 Client ID 和 Secret 加入 `.env`：

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

## 使用方式

### 瀏覽圖片

訪問 http://127.0.0.1:8000/gallery/ 查看所有圖片

### 使用 Google 登入

1. 點擊導航欄的「登入」
2. 選擇「使用 Google 登入」
3. 選擇 Google 帳號並授權

### 上傳圖片

1. 登入後，點擊「上傳圖片」
2. 填寫標題（必填）和描述（選填）
3. 選擇圖片檔案
4. 點擊「上傳」

### 管理我的圖片

1. 點擊「我的圖片」查看自己上傳的所有圖片
2. 在圖片詳細頁面可以刪除自己的圖片

## 執行測試

執行所有測試：

```bash
python manage.py test gallery
```

測試涵蓋：
- ✅ 圖片模型的建立、字串表示、排序
- ✅ 圖片列表頁面
- ✅ 圖片詳細頁面
- ✅ 圖片上傳（需登入）
- ✅ 我的圖片頁面（需登入）
- ✅ 圖片刪除（需登入且為擁有者）
- ✅ 表單驗證

## API 端點

- `/` - 首頁
- `/gallery/` - 圖片列表
- `/gallery/image/<id>/` - 圖片詳細頁面
- `/gallery/upload/` - 上傳圖片（需登入）
- `/gallery/my-images/` - 我的圖片（需登入）
- `/gallery/image/<id>/delete/` - 刪除圖片（需登入）
- `/accounts/login/` - 登入頁面
- `/accounts/signup/` - 註冊頁面
- `/accounts/logout/` - 登出
- `/accounts/google/login/` - Google 登入

## 技術棧

- **Django 4.2.26** - Web 框架
- **django-allauth 65.3.0** - 認證與社交登入
- **Pillow 10.4.0** - 圖片處理
- **Bootstrap 5.3** - 前端框架
- **SQLite** - 資料庫

## 注意事項

1. **圖片儲存**：上傳的圖片儲存在 `media/images/` 目錄，依日期分類
2. **權限控制**：
   - 所有人可以瀏覽圖片
   - 只有登入使用者可以上傳圖片
   - 只有圖片擁有者可以刪除自己的圖片
3. **分頁**：圖片列表每頁顯示 12 張圖片
4. **開發環境**：本設定僅適用於開發環境，正式環境需要額外配置

## 疑難排解

### PowerShell 執行原則錯誤

如果在啟動虛擬環境時遇到執行原則錯誤：

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 圖片無法顯示

確認 `MEDIA_ROOT` 和 `MEDIA_URL` 設定正確，且開發伺服器有提供 media 檔案服務。

### Google 登入失敗

1. 檢查 OAuth 憑證是否正確設定
2. 確認重新導向 URI 完全相符
3. 檢查 Sites 設定是否正確

## 後續開發建議

1. 新增圖片編輯功能
2. 實作圖片搜尋和篩選
3. 新增圖片標籤功能
4. 實作圖片留言功能
5. 新增圖片喜歡/收藏功能
6. 優化圖片縮圖處理
7. 實作更多社交登入選項（Facebook, GitHub 等）

## 授權

本專案僅供學習使用。
