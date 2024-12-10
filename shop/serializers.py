from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # 這樣 category 字段就會顯示 Category 模型的 __str__ 方法返回的名稱
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'  # 保留其他所有字段
