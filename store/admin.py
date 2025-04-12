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
<<<<<<< HEAD
    model = ProductImage  # ManyToManyField handling
=======
    model = ProductImage  # Use ProductImage directly
>>>>>>> 716d71bd9b74c2697b9acd9bcf971d704c9f877f
    extra = 1  # Number of empty forms to display

# Inline for ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Number of empty forms to display
    filter_horizontal = ('attributes',)  # Easier selection of attributes

# Admin for Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Manage images and variants inline
    inlines = [ProductImageInline, ProductVariantInline]
    list_display = ('title', 'collection', 'created_at')  # Display fields
    search_fields = ('title', 'description')  # Search by title and description
    list_filter = ('collection',)  # Filter by collection
    exclude = ('images',)  # Exclude images since we use inlines

# Admin for ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')  # Display fields
    search_fields = ('id',)  # Enable search by ID

# Admin for ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock', 'attributes_display')  # Display fields
    search_fields = ('product__title',)  # Enable search by product title
    list_filter = ('product__collection',)  # Filter by product collection

    def attributes_display(self, obj):
        return ", ".join([str(val) for val in obj.attributes.all()])
    attributes_display.short_description = 'Attributes'  # Custom column name
