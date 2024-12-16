from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from ..models import Product, order, Category
from ..serializers import ProductSerializer
from django.views.generic.base import TemplateView
from .Cart import CustomCart


def Get_Product(category_id=None):
    data = {}
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
                data = {
                    'Products': serializer.data
                }
            else:
                data = {'Products': []}
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            data = {
                'Products': serializer.data
            }

    except Category.DoesNotExist:
        data2 = {'categories': []}
        print("Error: Categories data not found.")
        
    except Product.DoesNotExist:
        data = {'Products': []}
        print("Error: Products data not found.")
    
    except Exception as e:
        data = {'Products': [], 'error': str(e)}
        print(f"Error: {e}")
        
    return data


# def Post_Product(data_form):
#     print(data_form)
#     id = data_form.get('productId', '')
#     quantity = int(data_form.get('qty', 1))
#     ret_json = {'status': 'ERROR', 'msg': '儲存失敗'}
#     try:
#         # Product.objects.filter(price__gt=100).update(price=90, description='限時優惠')

#         resault = Product.objects.aggregate(
#             total_price = Sum('price'),
#             max_price = Max('price'),
#             min_price = Min('price'),
#             avg_price = Avg('price')
#         )


#         product = Product.objects.get(id=id)
#         # 建立一個新的訂單
#         new_order = order.objects.create(
#             product = product,
#             quantity = quantity
#         )

#         # create()會自動save()，所以不需要再次呼叫
#         # new_order.save()
#         ret_json = {'status': 'OK', 'msg': '儲存成功'}

#     except Product.DoesNotExist:
#         ret_json = {'status': 'ERROR', 'msg': '商品不存在'}
#     except Exception as e:
#         print('資料庫錯誤:', e)
#         ret_json = {'status': 'ERROR', 'msg': '儲存失敗,' + str(e)}
        
#     return ret_json

def get_cart_count(request):
    cart = CustomCart(request)
    count = sum(int(item['quantity']) for item in cart)
    return JsonResponse({'cart_count': count})


class ShopProduct(APIView):
    template_name ='product.html'

    def get(self, request, category_id=None):
        data = Get_Product(category_id)

        template_data = { 
            'data': data, 
            # 'data2': data2 
            }        
        
        return render(request, self.template_name, template_data)
    
    def post(self, request):
        try:
            data = request.data
            slu = data.get('slu')
            quantity = data.get('quantity', 1)
            product = Product.objects.get(slu=slu)
            cart = CustomCart(request)
            cart.add(product, quantity)

            cart = CustomCart(request)
            cart_items = list(cart)
            cart_count = len(cart)

            ret_json = {'status': 'ok', 'msg': f'{product.name} 已成功加入購物車！', 'cart_items':cart_items, 'cart_count':cart_count}

            return JsonResponse(ret_json)

        except Product.DoesNotExist:
            ret_json = {'status': 'error', 'msg': '商品不存在'}
            return JsonResponse(ret_json)
        
        except Exception as e:
            ret_json = {'status': 'error', 'msg': str(e)}
            return JsonResponse(ret_json)
        




