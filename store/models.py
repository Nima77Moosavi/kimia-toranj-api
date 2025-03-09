from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='collections/')

    def __str__(self):
        return self.title


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name='attributes', null=True
    )  # Link Attribute to Collection instead of AttributeValue

    def __str__(self):
        if self.collection:
            return f"{self.name} ({self.collection.title})"
        return f"{self.name}"


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name='values'
    )
    value = models.CharField(max_length=255)  # e.g., "Red", "Small"

    def __str__(self):
        return f"{self.value} ({self.attribute.name})"


class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='images', null=True)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image {self.id}"


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants'
    )
    attributes = models.ManyToManyField(
        AttributeValue, related_name='variants')
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {', '.join([str(val) for val in self.attributes.all()])}"
