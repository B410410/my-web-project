from django.contrib import admin
from .models import Product, order

admin.site.register(Product)
admin.site.register(order)