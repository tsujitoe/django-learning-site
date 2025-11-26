from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>🎉 哇哈哈哈!!! 太神啦！我的 CI/CD 自動部署成功了！ 🎉</h1><p>現在時間：v2 版本</p>")