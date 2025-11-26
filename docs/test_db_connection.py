"""
測試 Supabase 資料庫連線
"""
import psycopg2
from decouple import config

def test_connection():
    print("正在測試 Supabase 資料庫連線...")
    print(f"主機: {config('SUPABASE_DB_HOST')}")
    print(f"資料庫: {config('SUPABASE_DB_NAME')}")
    print(f"使用者: {config('SUPABASE_DB_USER')}")
    print(f"連接埠: {config('SUPABASE_DB_PORT')}")
    
    try:
        conn = psycopg2.connect(
            host=config('SUPABASE_DB_HOST'),
            database=config('SUPABASE_DB_NAME'),
            user=config('SUPABASE_DB_USER'),
            password=config('SUPABASE_DB_PASSWORD'),
            port=config('SUPABASE_DB_PORT'),
            sslmode='require',
            connect_timeout=10
        )
        
        print("\n✅ 連線成功！")
        
        # 測試查詢
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"\nPostgreSQL 版本: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ 連線失敗: {e}")
        print("\n可能的原因：")
        print("1. 網路連線問題（防火牆或 VPN）")
        print("2. 密碼錯誤")
        print("3. Supabase 專案未啟動")
        print("4. 主機名稱錯誤")
        return False

if __name__ == '__main__':
    test_connection()
