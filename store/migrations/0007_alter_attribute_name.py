# Generated by Django 5.1.6 on 2025-03-09 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_product_images_productimage_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
