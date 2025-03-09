from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollectionViewSet, ProductViewSet, ProductImageViewSet, ProductVariantViewSet, AttributeViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'attributes', AttributeViewSet, basename='attribute')


urlpatterns = [
    path('', include(router.urls))
]
