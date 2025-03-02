from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='collections/') # Specify upload directory
    
    def __str__(self):
        return self.title
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/') # Specify upload directory
    
    def __str__(self):
        return f"Image {self.id}" # Provide a meaningful string representation

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    stock = models.PositiveIntegerField()
    images = models.ManyToManyField(ProductImage, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items') # Added on_delete
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=0) # Price at the time of order