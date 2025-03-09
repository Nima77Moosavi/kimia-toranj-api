from rest_framework import serializers
from .models import Product, ProductImage, ProductVariant, AttributeValue, Collection, Attribute


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value']


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(
        many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'values']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'attributes', 'price', 'stock']


class CollectionSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'description', 'image', 'attributes']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'collection',
            'images', 'variants', 'created_at', 'updated_at'
        ]
