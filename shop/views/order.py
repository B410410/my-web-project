from django.shortcuts import render, redirect
from rest_framework.views import APIView
from shop.views.Cart import CustomCart
from shop.models import Order, OrderItem, Product
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings


def create_order(customer_data, cart, user):
    full_name = customer_data.get('full_name', '')
    address = customer_data.get('address', '')
    phone = customer_data.get('phone', '')
    total_amount = cart.get_total_price()
    email = user.email
    try:
        order = Order(
            user=user,
            full_name=full_name,
            address=address,
            phone=phone,
            status='未付款',
            total_amount=total_amount,
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

            # 減少庫存
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
            else:
                raise ValueError(f'產品{product.name}庫存不足，訂單建立失敗')

        # 使用 bulk_create，避免多次 save
        OrderItem.objects.bulk_create(order_items)

        # email通知(客戶)
        # try:
        #     send_mail(
        #         '訂單確認',
        #         f'''{user.username}您好，您的訂單已於{order.create_date}建立成功! 
        #         訂單編號:{order.order_number} 
        #         訂單金額:{total_amount}元 
                
        #         您可以在此查看您的訂單詳情: http://example.com/shop/myorders/

        #         感謝您的訂購!!''',
        #         settings.EMAIL_HOST_USER,
        #         [email],
        #         fail_silently=False,
        #     )
        # except Exception as e:
        #     order.delete()  # 刪除訂單
        #     return {'status': 'error', 'msg': '發送 email 失敗，請檢查是否是正確的信箱。'}

        # # email通知(廠商)
        # send_mail(
        #     '新訂單建立',
        #     f'有客戶建立新訂單，訂單編號:{order.order_number}',
        #     settings.EMAIL_HOST_USER,
        #     [settings.EMAIL_HOST_USER],
        #     fail_silently=False,
        # )

        ret_json = {'status': 'ok', 'msg': f"訂單編號 {order.order_number} 建立成功"}
    
    except Exception as e:
        print('訂單建立失敗', e)
        ret_json = {'status': 'error', 'msg': str(e)}

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
        cart.clear()

        return JsonResponse(ret_json)
