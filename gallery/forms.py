from django import forms
from .models import Image


class ImageUploadForm(forms.ModelForm):
    """圖片上傳表單"""
    
    class Meta:
        model = Image
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '輸入圖片標題'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '輸入圖片描述（選填）'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
