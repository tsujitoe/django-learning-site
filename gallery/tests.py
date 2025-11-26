from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
from io import BytesIO
from .models import Image


def create_test_image():
    """建立測試用圖片檔案"""
    file = BytesIO()
    image = PILImage.new('RGB', (100, 100), color='red')
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return SimpleUploadedFile(
        name='test.png',
        content=file.read(),
        content_type='image/png'
    )


class ImageModelTest(TestCase):
    """圖片模型測試"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_image_creation(self):
        """測試圖片建立"""
        image = Image.objects.create(
            title='Test Image',
            description='Test Description',
            image=create_test_image(),
            uploaded_by=self.user
        )
        self.assertEqual(image.title, 'Test Image')
        self.assertEqual(image.description, 'Test Description')
        self.assertEqual(image.uploaded_by, self.user)
        self.assertTrue(image.image)
        
    def test_image_string_representation(self):
        """測試圖片字串表示"""
        image = Image.objects.create(
            title='Test Image',
            image=create_test_image(),
            uploaded_by=self.user
        )
        self.assertEqual(str(image), 'Test Image')
        
    def test_image_ordering(self):
        """測試圖片排序（應按建立時間倒序）"""
        image1 = Image.objects.create(
            title='Image 1',
            image=create_test_image(),
            uploaded_by=self.user
        )
        image2 = Image.objects.create(
            title='Image 2',
            image=create_test_image(),
            uploaded_by=self.user
        )
        images = Image.objects.all()
        self.assertEqual(images[0], image2)
        self.assertEqual(images[1], image1)


class GalleryViewsTest(TestCase):
    """圖片庫視圖測試"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.image = Image.objects.create(
            title='Test Image',
            description='Test Description',
            image=create_test_image(),
            uploaded_by=self.user
        )
        
    def test_gallery_list_view(self):
        """測試圖片列表頁面"""
        response = self.client.get(reverse('gallery:gallery_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Image')
        
    def test_image_detail_view(self):
        """測試圖片詳細頁面"""
        response = self.client.get(
            reverse('gallery:image_detail', args=[self.image.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Image')
        self.assertContains(response, 'Test Description')
        
    def test_image_upload_view_requires_login(self):
        """測試圖片上傳需要登入"""
        response = self.client.get(reverse('gallery:image_upload'))
        self.assertEqual(response.status_code, 302)  # 重導向到登入頁
        
    def test_image_upload_view_authenticated(self):
        """測試已登入使用者可以訪問上傳頁面"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('gallery:image_upload'))
        self.assertEqual(response.status_code, 200)
        
    def test_image_upload_post(self):
        """測試圖片上傳功能"""
        self.client.login(username='testuser', password='testpass123')
        image_file = create_test_image()
        response = self.client.post(
            reverse('gallery:image_upload'),
            {
                'title': 'New Image',
                'description': 'New Description',
                'image': image_file
            }
        )
        self.assertEqual(response.status_code, 302)  # 重導向
        self.assertEqual(Image.objects.count(), 2)
        new_image = Image.objects.latest('created_at')
        self.assertEqual(new_image.title, 'New Image')
        
    def test_my_images_view_requires_login(self):
        """測試我的圖片頁面需要登入"""
        response = self.client.get(reverse('gallery:my_images'))
        self.assertEqual(response.status_code, 302)
        
    def test_my_images_view_authenticated(self):
        """測試已登入使用者可以查看我的圖片"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('gallery:my_images'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Image')
        
    def test_image_delete_requires_login(self):
        """測試刪除圖片需要登入"""
        response = self.client.get(
            reverse('gallery:image_delete', args=[self.image.pk])
        )
        self.assertEqual(response.status_code, 302)
        
    def test_image_delete_only_owner(self):
        """測試只有擁有者可以刪除圖片"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('gallery:image_delete', args=[self.image.pk])
        )
        self.assertEqual(response.status_code, 404)
        
    def test_image_delete_post(self):
        """測試刪除圖片功能"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('gallery:image_delete', args=[self.image.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Image.objects.count(), 0)


class ImageFormTest(TestCase):
    """圖片表單測試"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_valid_form(self):
        """測試有效的表單"""
        from .forms import ImageUploadForm
        image_file = create_test_image()
        form = ImageUploadForm(
            data={'title': 'Test', 'description': 'Desc'},
            files={'image': image_file}
        )
        self.assertTrue(form.is_valid())
        
    def test_invalid_form_no_title(self):
        """測試無效的表單（缺少標題）"""
        from .forms import ImageUploadForm
        image_file = create_test_image()
        form = ImageUploadForm(
            data={'description': 'Desc'},
            files={'image': image_file}
        )
        self.assertFalse(form.is_valid())
        
    def test_invalid_form_no_image(self):
        """測試無效的表單（缺少圖片）"""
        from .forms import ImageUploadForm
        form = ImageUploadForm(
            data={'title': 'Test', 'description': 'Desc'}
        )
        self.assertFalse(form.is_valid())
