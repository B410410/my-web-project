from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # category 字段就會顯示 Category 模型的 __str__ 方法返回的名稱
    category = serializers.StringRelatedField()
    # 確保 image 字段返回的是 URL，而不是文件的路徑
    image = serializers.ImageField(use_url=True, required=False)  # 設置 use_url=True 來獲得圖片的 URL


    class Meta:
        model = Product
        fields = '__all__'  # 保留其他所有字段
