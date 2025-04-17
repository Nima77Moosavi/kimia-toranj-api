from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .models import Post, PostImage

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09123456789',
            password='password'
        )

        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user
        )
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        post_image = PostImage.objects.create(
            post=self.post,
            image=image_file
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')
        
    def test_post_image_str(self):
        post_image = PostImage.objects.get(post=self.post)
        self.assertEqual(str(post_image), f"Image for {self.post.title}")
        
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post.')
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(self.post.created_at)
        self.assertTrue(self.post.updated_at)
        
    def post_image_creation(self):
        post_image = PostImage.objects.get(post=self.post)
        self.assertEqual(post_image.post, self.post)
        self.assertTrue(post_image.image)
        self.assertTrue(post_image.image.url.endswith('test_image.jpg'))

