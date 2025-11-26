from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Image
from .forms import ImageUploadForm


def gallery_list(request):
    """圖片列表頁面"""
    images = Image.objects.all()
    paginator = Paginator(images, 12)  # 每頁顯示 12 張圖片
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gallery/image_list.html', {
        'page_obj': page_obj
    })


def image_detail(request, pk):
    """圖片詳細頁面"""
    image = get_object_or_404(Image, pk=pk)
    return render(request, 'gallery/image_detail.html', {
        'image': image
    })


@login_required
def image_upload(request):
    """圖片上傳頁面（需要登入）"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            image.save()
            messages.success(request, '圖片上傳成功！')
            return redirect('gallery:image_detail', pk=image.pk)
    else:
        form = ImageUploadForm()
    
    return render(request, 'gallery/image_upload.html', {
        'form': form
    })


@login_required
def my_images(request):
    """我的圖片頁面（需要登入）"""
    images = Image.objects.filter(uploaded_by=request.user)
    paginator = Paginator(images, 12)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gallery/my_images.html', {
        'page_obj': page_obj
    })


@login_required
def image_delete(request, pk):
    """刪除圖片（需要登入且為擁有者）"""
    image = get_object_or_404(Image, pk=pk, uploaded_by=request.user)
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, '圖片已刪除！')
        return redirect('gallery:my_images')
    
    return render(request, 'gallery/image_confirm_delete.html', {
        'image': image
    })
