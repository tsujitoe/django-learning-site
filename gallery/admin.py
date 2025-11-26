from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'created_at']
    list_filter = ['created_at', 'uploaded_by']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
