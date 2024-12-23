from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField
import random
import string
import uuid

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
    # on_delete=models.CASCADE:這個參數指定了當 category 被刪除時，與之相關的 Product 也會被刪除
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
        
    
class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20) 
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(  #訂單狀態
        max_length=20,
        choices=[('未付款', '未付款'), ('已付款', '已付款'), ('已出貨', '已出貨')],
        default='未付款',
    )
    class Meta:
        ordering = ('-create_date',)    # 按建立日期降序排列

    def __str__(self):
        return f"訂單編號: {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4())[:20]
        # 從Order的父類別方法開始用
        super(Order, self).save(*args, **kwargs)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # PositiveIntegerField:存儲正整數，只接受大於或等於 0 的整數
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"訂單編號: {self.order.order_number}, 價錢: {self.price}"
