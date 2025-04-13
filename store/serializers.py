from .models import Collection, Attribute
from rest_framework import serializers
from collections import Counter
from django.utils.translation import gettext_lazy as _
from .models import (
    Collection,
    Attribute,
    AttributeValue,
    ProductImage,
    Product,
    ProductVariant,
    Order,
    OrderItem,
    Cart,
    CartItem
)

# ------------------------------------------------------------------
# Attribute & AttributeValue Serializers
# ------------------------------------------------------------------


class AttributeValueSerializer(serializers.ModelSerializer):
    # For writes, expect an attribute's primary key.
    attribute = serializers.PrimaryKeyRelatedField(
        queryset=Attribute.objects.all())

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Replace the raw PK with a friendly string representation.
        rep['attribute'] = str(instance.attribute)
        return rep

    class Meta:
        model = AttributeValue
        fields = ['id', 'value', 'attribute']


class AttributeSerializer(serializers.ModelSerializer):
    # Nest the possible values for each attribute.
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'title', 'values']


# ------------------------------------------------------------------
# Collection Serializer
# ------------------------------------------------------------------

class NestedCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class CollectionSerializer(serializers.ModelSerializer):
    # This field returns the immediate parent as a nested object.
    parent = NestedCollectionSerializer(read_only=True)
    # For writes, we accept a parent's ID via this write-only field.
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    # When reading, also return the chain of all parents (ancestors).
    all_parents = serializers.SerializerMethodField()
    # The attributes are nested in the output.
    attributes = AttributeSerializer(many=True, read_only=True)
    # For writes, accept an array of attribute IDs.
    attribute_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Attribute.objects.all(),
        required=False
    )
    # Nest immediate children (sub-collections).
    sub_collections = NestedCollectionSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id',
            'title',
            'parent',         # read-only representation of the immediate parent
            'parent_id',      # write-only field for setting the parent
            'all_parents',    # read-only list of all ancestors
            'description',
            'image',
            'attributes',     # read-only nested attributes
            'attribute_ids',  # write-only attribute IDs
            'sub_collections'  # read-only list of direct child collections
        ]

    def get_all_parents(self, obj):
        """
        Returns a list of all parent collections (ancestors),
        starting with the immediate parent and working upward.
        """
        parents = []
        current = obj.parent  # using the `parent` field from the model
        while current:
            # Use the lightweight serializer to represent each parent.
            serializer = NestedCollectionSerializer(
                current, context=self.context)
            parents.append(serializer.data)
            current = current.parent
        return parents

    def create(self, validated_data):
        # Pop off write-only fields.
        parent = validated_data.pop('parent_id', None)
        attribute_ids = validated_data.pop('attribute_ids', [])
        # Create the collection instance.
        instance = super().create(validated_data)
        if parent:
            instance.parent = parent
            instance.save()
        if attribute_ids:
            instance.attributes.set(attribute_ids)
        return instance

    def update(self, instance, validated_data):
        parent = validated_data.pop('parent_id', None)
        attribute_ids = validated_data.pop('attribute_ids', None)
        instance = super().update(instance, validated_data)
        if parent is not None:
            instance.parent = parent
            instance.save()
        if attribute_ids is not None:
            instance.attributes.set(attribute_ids)
        return instance


# ------------------------------------------------------------------
# Product Serializers: ProductImage, ProductVariant & Product
# ------------------------------------------------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductVariantSerializer(serializers.ModelSerializer):
    # For read operations, show the full details of attribute values.
    attributes = AttributeValueSerializer(many=True, read_only=True)
    # For write operations, allow clients to send a list of attribute value IDs.
    attribute_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=AttributeValue.objects.all(),
        required=True
    )
    # For write operations, specify which product the variant is for.
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = ProductVariant
        fields = ['id', 'product_id', 'attributes',
                  'attribute_ids', 'price', 'stock']

    def validate(self, data):
        """
        Validate that:
          1. Only one AttributeValue is provided per Attribute.
          2. The provided attribute values cover all attributes required by the product's collection.
        """
        product = data.get('product')
        # List of AttributeValue instances
        attribute_values = data.get('attribute_ids')

        # Check that each attribute is represented only once.
        attr_id_list = [attr_val.attribute.id for attr_val in attribute_values]
        counter = Counter(attr_id_list)
        for attr_id, count in counter.items():
            if count > 1:
                raise serializers.ValidationError({
                    'attribute_ids': f"Multiple values provided for attribute ID {attr_id}. Select only one value per attribute."
                })

        # Build a set of provided attribute IDs.
        provided_attribute_ids = set(attr_id_list)
        # Retrieve all required attribute IDs from the product's collection.
        required_attribute_ids = set(
            product.collection.attributes.values_list('id', flat=True))
        missing_attributes = required_attribute_ids - provided_attribute_ids

        if missing_attributes:
            raise serializers.ValidationError({
                'attribute_ids': (
                    "Missing attribute values for required attributes with IDs: "
                    f"{list(missing_attributes)}."
                )
            })
        return data

    def create(self, validated_data):
        attribute_values = validated_data.pop('attribute_ids', [])
        variant = super().create(validated_data)
        if attribute_values:
            variant.attributes.set(attribute_values)
        return variant

    def update(self, instance, validated_data):
        attribute_values = validated_data.pop('attribute_ids', None)
        instance = super().update(instance, validated_data)
        if attribute_values is not None:
            instance.attributes.set(attribute_values)
        return instance


class ProductSerializer(serializers.ModelSerializer):
    # collection = CollectionSerializer(read_only=True)
    # Write: accept collection's primary key.
    collection_id = serializers.PrimaryKeyRelatedField(
        source='collection',
        queryset=Collection.objects.all(),
        write_only=True
    )
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description',
            'collection_id',
            'created_at', 'updated_at',
            'variants', 'images'
        ]


# ------------------------------------------------------------------
# Order & OrderItem Serializers
# ------------------------------------------------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    # Read: show full product variant info.
    product_variant = ProductVariantSerializer(read_only=True)
    # Write: allow setting with product_variant's primary key.
    product_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        write_only=True,
        source='product_variant'
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant',
                  'product_variant_id', 'quantity', 'price']

    def validate(self, attrs):
        product_variant = attrs.get('product_variant')
        quantity = attrs.get('quantity')
        if product_variant and quantity:
            # Ensure the requested quantity is available in stock.
            if quantity > product_variant.stock:
                raise serializers.ValidationError(
                    _('Requested quantity exceeds available stock.')
                )
        return attrs

    def create(self, validated_data):
        # Extract the product variant from validated data.
        product_variant = validated_data.pop('product_variant', None)
        # Automatically set the price from the product variant's price.
        validated_data['price'] = product_variant.price
        # Now create the order item.
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    # Nest order items to show detailed information.
    items = OrderItemSerializer(many=True, read_only=True)
    # Optionally, on order create you might accept a list of order items.
    # For brevity, here we assume order items are created separately.

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at',
                  'updated_at', 'status', 'total', 'items']


# ------------------------------------------------------------------
# Cart & CartItem Serializers
# ------------------------------------------------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    product_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        write_only=True,
        source='product_variant'
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'product_variant_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    # Depending on your use case, you might let clients update items via nested writes;
    # here we simply return a read-only list.

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key',
                  'created_at', 'updated_at', 'items']
