from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Image(models.Model):
    """圖片模型，用於儲存使用者上傳的圖片及相關資訊"""
    
    title = models.CharField(max_length=200, verbose_name='標題')
    description = models.TextField(blank=True, verbose_name='描述')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='圖片')
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='上傳者'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '圖片'
        verbose_name_plural = '圖片'

    def __str__(self):
        return self.title
