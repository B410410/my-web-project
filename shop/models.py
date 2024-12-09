from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='shop/images')

    def __str__(self):
        return self.name
        
    
class order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 計算總價：商品價格 * 購買數量
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        total_price_int = int(self.total_price)
        return f"訂單商品: {self.product.name} (數量: {self.quantity}, 總價: {total_price_int}台幣)"