# Generated by Django 5.1.3 on 2024-12-11 05:19

import django.db.models.deletion
import filer.fields.image
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_product_image'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to=settings.FILER_IMAGE_MODEL),
        ),
    ]
