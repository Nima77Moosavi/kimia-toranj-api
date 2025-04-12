from rest_framework import serializers
from .models import Product, ProductImage, ProductVariant, AttributeValue, Collection, Attribute


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value']


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all())

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'values', 'collection']


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
    # Make the images field writable so that it can accept image files when creating/updating the product.
    images = ProductImageSerializer(many=True, required=False)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'collection',
            'images', 'variants', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)

        # Handle images separately
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.collection = validated_data.get(
            'collection', instance.collection)
        instance.save()

        # Update images (delete existing ones and add new ones)
        instance.images.all().delete()  # Remove old images
        for image_data in images_data:
            ProductImage.objects.create(product=instance, **image_data)

        return instance
