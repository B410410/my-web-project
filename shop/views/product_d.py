from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Product, order, Category
from ..serializers import ProductSerializer

def get_product_d(slu=None):
    data = {}
    if not slu:
        return {'product_d': []}
    try:
        product = Product.objects.filter(slu=slu).first()
        if product:
            product_d = ProductSerializer([product], many=True)
            data = {
                'product_d':product_d.data
            }
        else:
            data = {
                'product_d':[]
            }
    except Exception as e:
        print('查詢錯誤:', e)
        data = {
                'product_d':[]
            }

    return data


class Product_d(APIView):
    template_name = 'product_d.html'

    def get(self, request, slu=None):
        data = get_product_d(slu)

        return render(request, self.template_name, data)