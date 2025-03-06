from django.shortcuts import render
from .serializers import CollectionSerializer, ProductSerializer
from .models import Collection, Product
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .filters import ProductFilter


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    @action(methods=['get'], detail=True)
    def products(self, request, pk=None):
        collection = self.get_object()
        products = Product.objects.filter(collection=collection)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
