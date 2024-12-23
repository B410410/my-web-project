from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    # category 字段就會顯示 Category 模型的 __str__ 方法返回的名稱
    category = serializers.StringRelatedField()
    # 確保 image 字段返回的是 URL，而不是文件的路徑
    image = serializers.ImageField(use_url=True, required=False)  # 設置 use_url=True 來獲得圖片的 URL

    class Meta:
        model = Product
        fields = '__all__'  # 保留其他所有字段

# 購物車, 用 serializers.Serializer
class CartItemSerializer(serializers.Serializer):
    product_slu = serializers.CharField(source='product.slu')
    product_name = serializers.CharField(source='product.name')
    product_image = serializers.ImageField(source='product.image')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    product_category = serializers.CharField(source='product.category.name')
    quantity = serializers.IntegerField()

# 訂單商品
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_slu = serializers.CharField(source='product.slu')
    price = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['product_name', 'product_slu', 'price', 'quantity']

# 訂單
class OrderSerializer(serializers.ModelSerializer):
    # items = OrderItemSerializer(many=True)  # 一個訂單可能有多個產品項目
    user_username = serializers.CharField(source='user.username')
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    total_amount = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user_username', 'full_name', 'address', 'phone', 'status', 'total_amount', 'create_date']
