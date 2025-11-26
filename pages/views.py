from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Hello! 我是金城武</h1>")