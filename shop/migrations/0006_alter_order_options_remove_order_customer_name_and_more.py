# Generated by Django 5.1.3 on 2024-12-17 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_product_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-create_date',)},
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='order',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('unpaid', '未付款'), ('paid', '已付款'), ('shipped', '已出貨')], default='unpaid', max_length=20),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
