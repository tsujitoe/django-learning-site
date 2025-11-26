# 1. 選擇基底映像檔 (就像選擇便當盒的材質)
# 我們使用 Python 3.10 的輕量版 (slim)
FROM python:3.10-slim

# 2. 設定容器內的工作目錄
WORKDIR /app

# 3. 設定環境變數 (讓 Python 輸出更即時，不要緩衝)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 安裝系統依賴 (有些 Python 套件需要編譯工具)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. 複製依賴清單並安裝
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. 複製專案所有程式碼進去
COPY . /app/

# 6.5. 收集靜態檔案（使用臨時的 SECRET_KEY）
RUN SECRET_KEY=temp_key_for_collectstatic python manage.py collectstatic --noinput

# 7. 告訴 Docker 這個容器會用哪個 Port (Cloud Run 預設用 8080)
EXPOSE 8080

# 8. 容器啟動時要執行的指令
# 這裡我們先用開發伺服器 runserver 測試，之後上線再改成 gunicorn
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
# 換成 Gunicorn
# --bind 0.0.0.0:$PORT : 讓 Gunicorn 監聽 Cloud Run 指定的 Port
# mysite.wsgi:application : 這是 Django 的進入點
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "mysite.wsgi:application"]