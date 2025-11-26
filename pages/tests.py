from django.test import SimpleTestCase
from django.urls import reverse

class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        # 模擬一個使用者去瀏覽首頁 '/'
        response = self.client.get('/')
        # 斷言(Assert)：我們期望收到的狀態碼是 200 (代表成功)
        self.assertEqual(response.status_code, 200)