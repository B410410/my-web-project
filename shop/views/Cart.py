from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.cart import Cart
from ..models import Product
from  cart.cart import Cart


class CustomCart(Cart):
    # 初始化購物車，從 session 中載入現有的購物車資料
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart', {})
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        slu = str(product.slu)

        if slu not in self.cart:
            self.cart[slu] = {
                'slu': slu,
                'product_id': product.id,
                'quantity': 0,
                'price': str(product.price),
                'name': product.name,
                'image': product.image.url if product.image else '',
                'stock':product.stock
            }

        quantity = int(quantity)
        current_quantity = int(self.cart[slu]['quantity'])
        # 更新數量
        if update_quantity:
            if quantity > product.stock:
                raise ValueError('庫存不足')
        
            self.cart[slu]['quantity'] = quantity
        else:
            new_quaantity = quantity + current_quantity
            if new_quaantity > product.stock:
                raise ValueError('購物車數量已大於庫存')
            
            self.cart[slu]['quantity'] = new_quaantity

        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True


    # 計算總金額
    def get_total_price(self):
        total = 0
        for item in self.cart.values():
            total += float(item['price']) * int(item['quantity'])
        return int(total)

    # 清空
    def clear(self):
        del self.session['cart']
        self.save()

    def get_items(self):
        return self.cart

    # 刪除商品
    def remove(self, slu):
        slu = str(slu)
        if slu in self.cart:
            del self.cart[slu]
            self.save()

    # 使購物車可以迭代，便於在模板中使用
    def __iter__(self):
        for item in self.cart.values():
            item['total'] = float(item['price']) * int(item['quantity'])
            yield item
    
    # 返回購物車中商品的數量
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


class CartView(APIView):
    template_name = 'cart.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('shop:login')
        cart = CustomCart(request)
        cart_items = list(cart)
        cart_total = cart.get_total_price()
        template_data = {
            'cart_items': cart_items, 
            'cart_total': cart_total
        }

        return render(request, self.template_name, template_data)

    # def post(self, request):
    #     # 處理加入商品到購物車
    #     data = json.loads(request.body)
    #     slu = data.get('slu')
    #     quantity = int(data.get('quantity', 1))
    #     try:
    #         product = Product.objects.get(slu=slu)
    #         cart = Cart(request)
    #         cart.add(product=product, quantity=quantity, update_quantity=False)

    #         ret_json = {'status': 'ok', 'msg': f'{product.name} 已成功加入購物車！'}
    #         return Response(ret_json)

    #     except Product.DoesNotExist:
    #         ret_json = {'status': 'error', 'msg': '商品不存在'}
    #         return Response(ret_json)
        
    #     except Exception as e:
    #         ret_json = {'status': 'error', 'msg': str(e)}
    #         return Response(ret_json)

    def put(self, request):
        # 更新數量
        data = request.data
        slu = data.get('slu')
        quantity = int(data.get('quantity'))
        try:
            product = Product.objects.get(slu=slu)
            cart = CustomCart(request)
            cart.add(product, quantity, update_quantity=True)

            cart_items = list(cart)
            cart_count = len(cart)
            total_price = cart.get_total_price()

            ret_json = {
                'status': 'ok', 
                'cart_items': cart_items, 
                'total_price': total_price,
                'cart_count': cart_count,
                }
            return JsonResponse(ret_json)
        
        except Product.DoesNotExist:
            ret_json = {'status': 'error', 'msg': '商品不存在'}
            return JsonResponse(ret_json)

        except Exception as e:
            ret_json = {'status': 'error', 'msg': str(e)}
            return JsonResponse(ret_json)

    def delete(self, request):
        # 刪除
        data = request.data
        slu = data.get('slu')
        try:
            cart = CustomCart(request)
            cart.remove(slu)

            cart_items = list(cart)
            cart_count = len(cart)
            total_price = cart.get_total_price()

            ret_json = {
                'status': 'ok', 
                'cart_items': cart_items, 
                'total_price': total_price,
                'cart_count': cart_count,
                }
            return JsonResponse(ret_json)
        
        except Exception as e:
            ret_json = {'status': 'error', 'msg': str(e)}
            return JsonResponse(ret_json)
