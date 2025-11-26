from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Hello! 這是我的 Django 首頁</h1>")