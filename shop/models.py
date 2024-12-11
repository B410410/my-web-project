from django.db import models
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField

class UserForm(models.Model):
    CITY = [
        ('TP', '台北市'),
        ('NP', '新北市'),
        ('TY', '桃園市'),
        ('TC', '台中市'),
        ('TN', '台南市'),
        ('KS', '高雄市'),
        ('NA', '其他縣市'),
    ]
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=10, choices=CITY, default='NP')
    is_student = models.BooleanField(default=False)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)    #產品分類
    slu = models.CharField(max_length=20)   #產品編號
    name = models.CharField(max_length=100)     #產品名稱
    description = models.TextField()    #產品描述
    image = FilerImageField(on_delete=models.CASCADE, related_name="product_image")  # 圖片
    website = models.URLField(null=True)    #產品網站
    stock = models.PositiveIntegerField(default=0)  #庫存
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  #價格

    def __str__(self):
        return self.name
        
    
class order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  #訂單與產品的關聯
    quantity = models.PositiveIntegerField(default=1)   #訂單數量
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)   #訂單總價
    order_date = models.DateField(auto_now_add=True)    #訂單日期
    customer_name = models.CharField(max_length=200, blank=True, null=True) #顧客姓名
    shipping_address = models.TextField(blank=True, null=True)  #顧客地址
    status = models.CharField(  #訂單狀態
        max_length=20,
        choices=[('pending', '待處理'), ('completed', '已完成'), ('shipped', '已發貨')],
        default='pending'
    )

    def save(self, *args, **kwargs):
        # 計算總價：商品價格 * 購買數量
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        total_price_int = int(self.total_price)  # 顯示總價的整數部分
        return f"訂單商品: {self.product.name} (數量: {self.quantity}, 總價: {total_price_int}台幣)"