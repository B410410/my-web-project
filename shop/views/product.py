from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, order
from ..serializers import ProductSerializer
from django.http import JsonResponse
from django.db.models import Sum, Max, Min, Avg
from django.views.generic.base import TemplateView



def Get_Product():
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    print('serializer', serializer.data)
    data = {
        'Products': serializer.data 
    }
    return data

def Post_Product(data_form):
    print(data_form)
    id = data_form.get('productId', '')
    quantity = int(data_form.get('qty', 1))
    ret_json = {'status': 'ERROR', 'msg': '儲存失敗'}
    try:
        # Product.objects.filter(price__gt=100).update(price=90, description='限時優惠')

        resault = Product.objects.aggregate(
            total_price = Sum('price'),
            max_price = Max('price'),
            min_price = Min('price'),
            avg_price = Avg('price')
        )


        product = Product.objects.get(id=id)
        # 建立一個新的訂單
        new_order = order.objects.create(
            product = product,
            quantity = quantity
        )

        # create()會自動save()，所以不需要再次呼叫
        # new_order.save()
        ret_json = {'status': 'OK', 'msg': '儲存成功'}

    except Product.DoesNotExist:
        ret_json = {'status': 'ERROR', 'msg': '商品不存在'}
    except Exception as e:
        print('資料庫錯誤:', e)
        ret_json = {'status': 'ERROR', 'msg': '儲存失敗,' + str(e)}
        
    return ret_json



class ShopProduct(APIView):
    template_name ='product.html'

    def get(self, request):
        data = Get_Product()

        return render(request, self.template_name, data)
    
    def post(self, request):
        data_form = request.data
        ret_json = Post_Product(data_form)

        return JsonResponse(ret_json)


class ShopProductView(TemplateView):
    template_name = 'shop/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 獲取所有商品資料
        products = Product.objects.all()
        # 使用ProductSerializer進行序列化
        serializer = ProductSerializer(products, many=True)
        context['Products'] = serializer.data
        return context
    

class AddToCartView(APIView):
    def post(self, request):
        data_form = request.data
        product_id = data_form.get('productId', '')
        quantity = int(data_form.get('qty', 1))
        ret_json = {'status': 'ERROR', 'msg': '儲存失敗'}

        try:
            # 確認商品是否存在
            product = Product.objects.get(id=product_id)

            # 創建訂單記錄
            new_order = order.objects.create(
                product=product,
                quantity=quantity
            )

            ret_json = {'status': 'OK', 'msg': '商品已加入購物車'}
        except Product.DoesNotExist:
            ret_json = {'status': 'ERROR', 'msg': '商品不存在'}
        except Exception as e:
            ret_json = {'status': 'ERROR', 'msg': '儲存失敗，' + str(e)}

        return JsonResponse(ret_json)

class CartView(TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 從Session中獲取購物車資料
        cart = self.request.session.get('cart', [])
        items = []
        total_price = 0

        for item in cart:
            try:
                product = Product.objects.get(id=item['product_id'])
                item_total = product.price * item['quantity']
                items.append({
                    'id': product.id,
                    'name': product.name,
                    'quantity': item['quantity'],
                    'price': product.price,
                    'total_price': item_total
                })
                total_price += item_total
            except Product.DoesNotExist:
                continue

        context['cart_items'] = items
        context['total_price'] = total_price
        return context
