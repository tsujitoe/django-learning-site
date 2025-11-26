from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Hello! 這是金城武首頁</h1>")