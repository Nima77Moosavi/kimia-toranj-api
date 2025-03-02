from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostImageViewSet, WYSIWYGImageUploadView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'post-images', PostImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('wysiwyg-upload/', WYSIWYGImageUploadView.as_view(), name='wysiwyg-upload'),
]