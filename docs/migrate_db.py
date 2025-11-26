"""
資料庫遷移腳本
在部署到生產環境後執行此腳本
"""
import os
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    print("開始執行資料庫遷移...")
    try:
        # 執行遷移
        call_command('migrate', verbosity=2)
        print("\n✅ 資料庫遷移完成！")
        
        # 顯示已套用的遷移
        print("\n已套用的遷移:")
        call_command('showmigrations')
        
    except Exception as e:
        print(f"\n❌ 遷移失敗: {e}")
        import traceback
        traceback.print_exc()
