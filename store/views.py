from django.shortcuts import render
from .serializers import CollectionSerializer, ProductSerializer, ProductImageSerializer, ProductVariantSerializer
from .models import Collection, Product, ProductImage, ProductVariant
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
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(image=image, products=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        # Get the product ID from the URL or the request data
        product_id = request.data.get('product')
        product = Product.objects.get(id=product_id)

        # Validate that 'images' is in the request
        images = request.FILES.getlist('images')
        if not images:
            return Response({"error": "No images uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        for image in images:
            # Create product image and associate it with the product
            ProductImage.objects.create(image=image, product=product)

        return Response({"status": "Images uploaded successfully!"}, status=status.HTTP_201_CREATED)


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
