from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # 指定使用的模型
        fields = '__all__'  # 指定要序列化的字段，這裡選擇所有字段