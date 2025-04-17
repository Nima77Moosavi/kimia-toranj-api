from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Collection(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="عنوان دسته بندی")
    parent = models.ForeignKey(
        'self', on_delete=models.PROTECT, related_name='subcollections',
        null=True, blank=True, verbose_name=" دسته بندی والد"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="توضیحات")
    image = models.ImageField(
        upload_to='collections/', verbose_name="تصویر دسته بندی", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Attribute(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="عنوان ویژگی")
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, null=True, related_name='attributes', verbose_name="دسته بندی"
    )

    def __str__(self):
        return f'{self.title} ({self.collection.title})'

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی‌ها"


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name='values', verbose_name="ویژگی")
    value = models.CharField(
        max_length=255, verbose_name="مقدار ویژگی")

    def __str__(self):
        return f"{self.value} ({self.attribute})"

    class Meta:
        verbose_name = "مقدار ویژگی"
        verbose_name_plural = "مقادیر ویژگی‌ها"


class Product(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="عنوان محصول")
    description = models.TextField(
        verbose_name="توضیحات محصول")
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products', verbose_name="مجموعه")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="آخرین به‌روزرسانی")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images', null=True, verbose_name="محصول")
    image = models.ImageField(
        upload_to='products/', verbose_name="تصویر محصول")

    def __str__(self):
        return f"Image {self.id}"

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصولات"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants', verbose_name="محصول"
    )
    attributes = models.ManyToManyField(
        AttributeValue, related_name='variants', verbose_name="ویژگی‌ها"
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=0, null=True, verbose_name="قیمت"
    )
    stock = models.PositiveIntegerField(
        default=0, verbose_name="موجودی انبار"
    )

    def __str__(self):
        # If the object is not yet saved, there may be no M2M data available.
        if not self.pk:
            return f"{self.product.title} - (بدون ویژگی)"
        # Retrieve the attribute values.
        attr_values = self.attributes.all()
        if attr_values.exists():
            attr_string = ", ".join([str(val) for val in attr_values])
        else:
            attr_string = "(بدون ویژگی)"
        return f"{self.product.title} - {attr_string}"

    class Meta:
        verbose_name = "نوع محصول"
        verbose_name_plural = "انواع محصولات"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders', verbose_name="کاربر")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="آخرین به‌روزرسانی")
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    total = models.DecimalField(
        max_digits=12, decimal_places=0, default=0.00, verbose_name="مبلغ کل")

    def __str__(self):
        return f"Order #{self.id} ({self.user})"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name='order_items', verbose_name="نوع محصول")
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="تعداد")
    price = models.DecimalField(
        max_digits=12, decimal_places=0, null=True, verbose_name="قیمت محصول")

    def __str__(self):
        return f"{self.product_variant} x {self.quantity}"

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', null=True, blank=True, verbose_name="کاربر")
    session_key = models.CharField(
        max_length=40, blank=True, null=True, verbose_name="کلید نشست")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="آخرین به‌روزرسانی")

    def __str__(self):
        return f"Cart ({self.user or 'Anonymous'})"

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items', verbose_name="سبد خرید")
    product_variant = models.ForeignKey(
        'ProductVariant', on_delete=models.CASCADE, verbose_name="نوع محصول")
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="تعداد")

    def __str__(self):
        return f"{self.product_variant} x {self.quantity}"

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"
