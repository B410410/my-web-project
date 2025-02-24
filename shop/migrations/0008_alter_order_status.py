# Generated by Django 5.1.3 on 2024-12-19 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_order_address_alter_order_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('未付款', '未付款'), ('已付款', '已付款'), ('已出貨', '已出貨')], default='未付款', max_length=20),
        ),
    ]
