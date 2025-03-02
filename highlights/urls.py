from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HighlightViewSet, HighlightMediaViewSet

router = DefaultRouter()
router.register(r'highlights', HighlightViewSet)
router.register(r'highlight-media', HighlightMediaViewSet)

urlpatterns = [
    path('', include(router.urls))
]
