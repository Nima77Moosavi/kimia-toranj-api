from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import permissions
from django_filters import rest_framework as filters

from .serializers import (
    CollectionSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductVariantSerializer,
    AttributeSerializer,
    AttributeValueSerializer
)
from .models import (
    Collection,
    Product,
    ProductImage,
    ProductVariant,
    Attribute,
    AttributeValue
)
from .filters import ProductFilter


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.prefetch_related('subcollections').all()
    serializer_class = CollectionSerializer

    @action(methods=['get'], detail=True)
    def products(self, request, pk=None):
        collection = self.get_object()
        # Optimize the query by prefetching related data for each Product.
        products = Product.objects.select_related('collection').prefetch_related(
            'variants__attributes__attribute', 'images').filter(collection=collection)

        # Apply filtering if filter params are passed in the request
        product_filter = ProductFilter(request.GET, queryset=products)
        if product_filter.is_valid():
            products = product_filter.qs

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def filters(self, request, pk=None):
        """Retrieve the attributes (filters) for the given collection."""
        collection = self.get_object()
        # Get attributes linked to this collection
        attributes = collection.attributes.all()
        serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optimize queries by selecting the collection and prefetching related variants and images.
        return Product.objects.select_related('collection').prefetch_related(
            'variants__attributes__attribute', 'images').all()

    def create(self, request, *args, **kwargs):
        # Create the product using the serializer.
        serializer = ProductSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                # Create ProductImage instances and associate them with the product
                ProductImage.objects.create(product=product, image=image)
        # Re-serialize the product so that the response includes the newly added images.
        product_serializer = ProductSerializer(
            product, context={'request': request})
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    ProductImageViewSet manages images related to a product.
    It makes sure to validate the product exists and that images are indeed provided.
    """
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Optimize queries for product images by selecting the related product.
        return ProductImage.objects.select_related('product').all()

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_400_BAD_REQUEST)

        images = request.FILES.getlist('images')
        if not images:
            return Response({"error": "No images uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        for image in images:
            img_instance = ProductImage.objects.create(
                product=product, image=image)
            created_images.append(img_instance)

        serializer = ProductImageSerializer(
            created_images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttributeViewSet(viewsets.ModelViewSet):
    """
    AttributeViewSet allows listing and CRUD for global attributes.
    Optionally, you can filter by a related collection using the query parameter 'collection'.
    It also provides an action `add_value` for adding a new AttributeValue to an attribute.
    """
    serializer_class = AttributeSerializer

    def get_queryset(self):
        collection_id = self.request.query_params.get('collection', None)
        if collection_id is not None:
            # Use the many-to-many relation to filter attributes by collection.
            return Attribute.objects.filter(collections__id=collection_id).distinct()
        return Attribute.objects.all()

    @action(detail=True, methods=['post'])
    def add_value(self, request, pk=None):
        attribute = self.get_object()
        value = request.data.get('value')
        if not value:
            return Response({"error": _("Value is required.")}, status=status.HTTP_400_BAD_REQUEST)
        attribute_value = AttributeValue.objects.create(
            attribute=attribute, value=value)
        serializer = AttributeValueSerializer(
            attribute_value, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductVariantViewSet(viewsets.ModelViewSet):
    """
    ProductVariantViewSet manages the variants of a product.
    Adding query-optimization with select_related and prefetch_related for related attribute data.
    """
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        return ProductVariant.objects.select_related('product') \
            .prefetch_related('attributes__attribute').all()
