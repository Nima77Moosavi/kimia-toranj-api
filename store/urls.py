from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollectionViewSet, ProductViewSet, ProductImageViewSet, ProductVariantViewSet, AttributeViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='product-image')
router.register(r'variants', ProductVariantViewSet, basename='variant')
router.register(r'attributes', AttributeViewSet, basename='attribute')


urlpatterns = [
    path('', include(router.urls))
]
