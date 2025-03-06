from django.db import models


class Attribute(models.Model):
    # e.g., "Color", "Size"
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)  # e.g., "Red", "Small"
    collection = models.ForeignKey(
        'Collection', on_delete=models.CASCADE, related_name='attributes', null=True)

    def __str__(self):
        return f"{self.name}: {self.collection.title}"


class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # Specify upload directory
    image = models.ImageField(upload_to='collections/')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    # Specify upload directory
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image {self.id}"  # Provide a meaningful string representation


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    images = models.ManyToManyField(ProductImage, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants')
    attributes = models.ManyToManyField(
        AttributeValue, related_name='variants')
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {', '.join([str(val) for val in self.attributes.all()])}"
