from django.contrib import admin
from shop import models

class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'slu', 'name', 'stock', 'price',)
    ordering = ('category',)

admin.site.register(models.UserForm)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)