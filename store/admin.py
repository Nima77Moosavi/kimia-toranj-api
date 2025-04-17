from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import (
    Attribute,
    AttributeValue,
    Collection,
    Product,
    ProductImage,
    ProductVariant,
    Order,
    OrderItem,
    Cart,
    CartItem
)

# -----------------------------------------------------------
# Inline for AttributeValue (used in the Attribute admin)
# -----------------------------------------------------------


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1  # Number of empty inline forms

# -----------------------------------------------------------
# Attribute Admin
# -----------------------------------------------------------


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]
    list_display = ('title',)
    search_fields = ('title',)

# -----------------------------------------------------------
# Collection Admin
# -----------------------------------------------------------


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

# -----------------------------------------------------------
# Inline for ProductImage (to manage multiple images)
# -----------------------------------------------------------


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# -----------------------------------------------------------
# Inline for ProductVariant (to manage variants for a product)
# -----------------------------------------------------------


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    filter_horizontal = ('attributes',)  # Easier M2M selection

# -----------------------------------------------------------
# Product Admin
# -----------------------------------------------------------


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Manage images and variants inline in the product detail view.
    inlines = [ProductImageInline, ProductVariantInline]
    list_display = ('title', 'collection', 'created_at')
    search_fields = ('title', 'description')
    autocomplete_fields = ('collection',)  # For better UX in large datasets
    list_filter = ('collection',)
    exclude = ('images',)  # Exclude images field since they are inlined.

# -----------------------------------------------------------
# ProductImage Admin
# -----------------------------------------------------------


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ('id',)

# -----------------------------------------------------------
# Custom Admin Form for ProductVariant
# Enforces that all attributes required by the product's collection are provided.
# -----------------------------------------------------------


class ProductVariantAdminForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        # This is a queryset from the form.
        attributes = cleaned_data.get('attributes')

        if product:
            required_attribute_ids = set(
                product.collection.attributes.values_list('id', flat=True)
            )
            provided_attribute_ids = set()
            if attributes:
                for attr_value in attributes:
                    # Ensure the attribute field is available on each AttributeValue.
                    if getattr(attr_value, 'attribute', None):
                        provided_attribute_ids.add(attr_value.attribute.id)
            missing = required_attribute_ids - provided_attribute_ids
            if missing:
                raise ValidationError({
                    'attributes': f"Missing attribute values for required attributes with ids: {list(missing)}."
                })
        return cleaned_data

# -----------------------------------------------------------
# ProductVariant Admin using the custom form
# -----------------------------------------------------------


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    form = ProductVariantAdminForm
    list_display = ('product', 'stock', 'attributes_display')
    search_fields = ('product__title',)
    list_filter = ('product__collection',)

    def attributes_display(self, obj):
        return ", ".join([str(val) for val in obj.attributes.all()])
    attributes_display.short_description = 'Attributes'

# -----------------------------------------------------------
# Order and OrderItem Admin
# -----------------------------------------------------------


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # No extra blank rows


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    # Assuming the User model uses phone_number.
    search_fields = ('user__phone_number',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variant', 'quantity', 'price')
    search_fields = ('order__user__phone_number',
                     'product_variant__product__title')

# -----------------------------------------------------------
# Cart and CartItem Admin
# -----------------------------------------------------------


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('id', 'user', 'session_key', 'created_at')
    search_fields = ('user__phone_number', 'session_key')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_variant', 'quantity')
    search_fields = ('cart__user__phone_number',
                     'product_variant__product__title')
