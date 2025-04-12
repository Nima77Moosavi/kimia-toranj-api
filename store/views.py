from django.shortcuts import render
from .serializers import (CollectionSerializer, ProductSerializer, ProductImageSerializer, ProductVariantSerializer,
                          AttributeSerializer, AttributeValueSerializer)
from .models import Collection, Product, ProductImage, ProductVariant, Attribute, AttributeValue
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django_filters import rest_framework as filters
from .filters import ProductFilter


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    @action(methods=['get'], detail=True)
    def products(self, request, pk=None):
        collection = self.get_object()
        # Apply filters to the products queryset for this collection
        products = Product.objects.filter(collection=collection)

        # Apply filtering if filter params are passed in the request
        product_filter = ProductFilter(request.GET, queryset=products)
        if product_filter.is_valid():
            products = product_filter.qs

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        # Parse the product data and create the product
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # Save the product
            product = serializer.save()

            # Now handle the images associated with this product
            images = request.FILES.getlist('images')
            for image in images:
                # Create a ProductImage instance and associate it with the product
                ProductImage.objects.create(product=product, image=image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        # Get the product ID from the request data
        product_id = request.data.get('product')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that 'images' are uploaded in the request
        images = request.FILES.getlist('images')
        if not images:
            return Response({"error": "No images uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        for image in images:
            # Create ProductImage instances and associate them with the product
            ProductImage.objects.create(product=product, image=image)

        return Response({"status": "Images uploaded successfully!"}, status=status.HTTP_201_CREATED)


class AttributeViewSet(viewsets.ModelViewSet):
    serializer_class = AttributeSerializer

    def get_queryset(self):
        collection_id = self.request.query_params.get('collection', None)
        if collection_id is not None:
            return Attribute.objects.filter(collection_id=collection_id)
        return Attribute.objects.all()

    @action(detail=True, methods=['post'])
    def add_value(self, request, pk=None):
        attribute = self.get_object()
        value = request.data.get('value')

        if value:
            # Create the new attribute value
            attribute_value = AttributeValue.objects.create(
                attribute=attribute, value=value)
            return Response({"id": attribute_value.id, "value": attribute_value.value}, status=status.HTTP_201_CREATED)

        serializer = AttributeValueSerializer(attribute_value)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
