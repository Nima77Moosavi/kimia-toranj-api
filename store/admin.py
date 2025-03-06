from django.contrib import admin
from .models import Attribute, AttributeValue, Collection, Product, ProductImage, ProductVariant

# Inline for AttributeValue


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1  # Number of empty forms to display

# Admin for Attribute


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]  # Manage AttributeValues inline
    list_display = ('name',)  # Display fields in the list view
    search_fields = ('name',)  # Enable search by name

# Admin for Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Display fields in the list view
    search_fields = ('title',)  # Enable search by title

# Inline for ProductImage


class ProductImageInline(admin.TabularInline):
    model = Product.images.through  # Use the through model for ManyToManyField
    extra = 1  # Number of empty forms to display

# Inline for ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Number of empty forms to display
    filter_horizontal = ('attributes',)  # Easier selection of attributes

# Admin for Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Manage ProductImages and ProductVariants inline
    inlines = [ProductImageInline, ProductVariantInline]
    # Display fields in the list view
    list_display = ('title', 'collection', 'created_at')
    # Enable search by title and description
    search_fields = ('title', 'description')
    list_filter = ('collection',)  # Enable filtering by collection
    # Exclude the images field since we're using an inline
    exclude = ('images',)

# Admin for ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')  # Display fields in the list view
    search_fields = ('id',)  # Enable search by ID

# Admin for ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('product', 'stock', 'attributes_display')
    search_fields = ('product__title',)  # Enable search by product title
    # Enable filtering by product collection
    list_filter = ('product__collection',)

    def attributes_display(self, obj):
        return ", ".join([str(val) for val in obj.attributes.all()])
    attributes_display.short_description = 'Attributes'  # Custom column name
