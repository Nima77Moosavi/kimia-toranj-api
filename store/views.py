from django.shortcuts import render
from .serializers import CollectionSerializer, ProductSerializer
from .models import Collection, Product
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .filters import ProductFilter


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
