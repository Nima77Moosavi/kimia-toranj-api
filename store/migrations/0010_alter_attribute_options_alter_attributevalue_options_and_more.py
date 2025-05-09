# Generated by Django 5.1.6 on 2025-04-12 10:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_cart_cartitem_order_orderitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attribute',
            options={'verbose_name': 'ویژگی', 'verbose_name_plural': 'ویژگی\u200cها'},
        ),
        migrations.AlterModelOptions(
            name='attributevalue',
            options={'verbose_name': 'مقدار ویژگی', 'verbose_name_plural': 'مقادیر ویژگی\u200cها'},
        ),
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'سبد خرید', 'verbose_name_plural': 'سبدهای خرید'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'آیتم سبد خرید', 'verbose_name_plural': 'آیتم\u200cهای سبد خرید'},
        ),
        migrations.AlterModelOptions(
            name='collection',
            options={'verbose_name': 'مجموعه', 'verbose_name_plural': 'مجموعه\u200cها'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارش\u200cها'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'آیتم سفارش', 'verbose_name_plural': 'آیتم\u200cهای سفارش'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'تصویر محصول', 'verbose_name_plural': 'تصاویر محصولات'},
        ),
        migrations.AlterModelOptions(
            name='productvariant',
            options={'verbose_name': 'نوع محصول', 'verbose_name_plural': 'انواع محصولات'},
        ),
        migrations.AddField(
            model_name='collection',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_collections', to='store.collection', verbose_name='زیر مجموعه'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='title',
            field=models.CharField(max_length=255, verbose_name='عنوان ویژگی'),
        ),
        migrations.AlterField(
            model_name='attributevalue',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='store.attribute', verbose_name='ویژگی'),
        ),
        migrations.AlterField(
            model_name='attributevalue',
            name='value',
            field=models.CharField(max_length=255, verbose_name='مقدار ویژگی'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='کلید نشست'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='آخرین به\u200cروزرسانی'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.cart', verbose_name='سبد خرید'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product_variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productvariant', verbose_name='نوع محصول'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='تعداد'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='attributes',
            field=models.ManyToManyField(blank=True, related_name='collections', to='store.attribute', verbose_name='ویژگی\u200cها'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='image',
            field=models.ImageField(upload_to='collections/', verbose_name='تصویر مجموعه'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='title',
            field=models.CharField(max_length=255, verbose_name='عنوان مجموعه'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'در انتظار'), ('processing', 'در حال پردازش'), ('completed', 'تکمیل شده'), ('cancelled', 'لغو شده')], default='pending', max_length=20, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=0, default=0.0, max_digits=12, verbose_name='مبلغ کل'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='آخرین به\u200cروزرسانی'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order', verbose_name='سفارش'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=12, null=True, verbose_name='قیمت محصول'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='store.productvariant', verbose_name='نوع محصول'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='تعداد'),
        ),
        migrations.AlterField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.collection', verbose_name='مجموعه'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='توضیحات محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, verbose_name='عنوان محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='آخرین به\u200cروزرسانی'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='products/', verbose_name='تصویر محصول'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='attributes',
            field=models.ManyToManyField(related_name='variants', to='store.attributevalue', verbose_name='ویژگی\u200cها'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=12, null=True, verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='store.product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='stock',
            field=models.PositiveIntegerField(default=0, verbose_name='موجودی انبار'),
        ),
    ]
