# Generated by Django 5.1.6 on 2025-03-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_attribute_remove_product_stock_attributevalue_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=12, null=True),
        ),
    ]
