from django.shortcuts import render, redirect
from rest_framework.views import APIView
from shop.views.Cart import CustomCart
from shop.models import Order, OrderItem, Product
from django.http import JsonResponse


def create_order(customer_data, cart, user):
    full_name = customer_data.get('full_name', '')
    address = customer_data.get('address', '')
    phone = customer_data.get('phone', '')
    try:
        order = Order(
            user=user,
            full_name=full_name,
            address=address,
            phone=phone,
            status='unpaid',
        )
        order.save()

        order_items = []
        for item in cart:
            product = Product.objects.get(slu=item['slu'])
            quantity = item['quantity']
            price = item['price']

            order_item = OrderItem(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            order_items.append(order_item)

        # 使用 bulk_create，避免多次 save
        OrderItem.objects.bulk_create(order_items)
        ret_json = {'status': 'ok', 'msg': f"訂單編號 {order.order_number} 建立成功"}
    
    except Exception as e:
        print('訂單建立失敗', e)
        ret_json = {'status': 'error', 'msg': '訂單建立失敗'}

    return ret_json


class OrderView(APIView):
    template_name = 'order.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('shop:login')
        cart = CustomCart(request)
        cart_items = list(cart)
        cart_count = len(cart)
        cart_total = cart.get_total_price()

        template_data = {  
            'cart_items': cart_items, 
            'cart_count': cart_count,
            'cart_total': cart_total,
            }        
        
        return render(request, self.template_name, template_data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('shop:login')
        customer_data = request.data
        cart = CustomCart(request)
        user = request.user
        ret_json = create_order(customer_data, cart, user)

        return JsonResponse(ret_json)
