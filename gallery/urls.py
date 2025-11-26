from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery_list, name='gallery_list'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('upload/', views.image_upload, name='image_upload'),
    path('my-images/', views.my_images, name='my_images'),
    path('image/<int:pk>/delete/', views.image_delete, name='image_delete'),
]
