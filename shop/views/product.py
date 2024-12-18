from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from ..models import Product, Order, Category
from ..serializers import ProductSerializer
from django.views.generic.base import TemplateView
from .Cart import CustomCart


def Get_Product(category_id=None):
    ret_json = {}
    data2 = {}
    try:
        # categories = Category.objects.all()
        # data2 = {
        #     'categories': categories.data
        # }
        
        if category_id:
            products = Product.objects.filter(category_id=category_id)
            if products:
                serializer = ProductSerializer(products, many=True)
                ret_json = {
                    'Products': serializer.data
                }
            else:
                ret_json = {'Products': []}
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            ret_json = {
                'Products': serializer.data
            }

    except Category.DoesNotExist:
        ret_json = {'categories': []}
        print("Error: Categories data not found.")
        
    except Product.DoesNotExist:
        ret_json = {'Products': []}
        print("Error: Products data not found.")
    
    except Exception as e:
        ret_json = {'Products': [], 'error': str(e)}
        print(f"Error: {e}")
        
    return ret_json

class ShopProduct(APIView):
    template_name ='product.html'

    def get(self, request, category_id=None):
        data = Get_Product(category_id)
        cart = CustomCart(request)
        cart_items = list(cart)
        cart_count = len(cart)
        cart_total = cart.get_total_price()

        template_data = { 
            'data': data, 
            'cart_items': cart_items, 
            'cart_count': cart_count,
            'cart_total': cart_total,
            }        
        
        return render(request, self.template_name, template_data)
    
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                ret_json = {'status': 'error', 'msg': '請先登入'}
                return JsonResponse(ret_json)
            data = request.data
            slu = data.get('slu')
            quantity = data.get('quantity', 1)
            product = Product.objects.get(slu=slu)
            cart = CustomCart(request)
            cart.add(product, quantity)

            cart = CustomCart(request)
            cart_items = list(cart)
            cart_count = len(cart)
            cart_total = cart.get_total_price()
            print('cart_count', cart_count)

            ret_json = {
                'status': 'ok',
                'msg': f'{product.name} 已成功加入購物車！', 
                'cart_items': cart_items, 
                'cart_count': cart_count,
                'cart_total': cart_total,
                }

            return JsonResponse(ret_json)

        except Product.DoesNotExist:
            ret_json = {'status': 'error', 'msg': '商品不存在'}
            return JsonResponse(ret_json)
        
        except Exception as e:
            ret_json = {'status': 'error', 'msg': str(e)}
            return JsonResponse(ret_json)
        
        




