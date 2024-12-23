from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework.views import APIView
from ..models import Product, Order, OrderItem
from ..serializers import OrderSerializer, OrderItemSerializer
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

def orderitems(id=None):
    try:
        order = Order.objects.get(id=id)
        order_items = OrderItem.objects.filter(order=order)
        paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,                             # PayPal 收款郵箱
                'amount': order.total_amount,                                           # 訂單金額
                'item_name': f'MyWeb訂單編號{order.order_number}',                      # 訂單名稱
                'invoice': str(order.order_number),                                     # 訂單編號
                'currency_code': 'TWD',                                                 # 設置貨幣
                'notify_url': 'http://www.your-domain.com/paypal/ipn/',                 # PayPal 回調 URL
                'return_url': 'http://www.your-domain.com/shop/payment-success/',       # 支付成功後重定向 URL
                'cancel_return': 'http://www.your-domain.com/shop/payment-cancelled/',  # 支付取消後重定向 URL
            }
        paypalForm = PayPalPaymentsForm(initial=paypal_dict)
        order_j = OrderSerializer(order)
        order_items_j = OrderItemSerializer(order_items, many=True)
        template_data = {
            'order': order_j.data,
            'order_items': order_items_j.data,
            'paypalForm': paypalForm,
        }
    except Exception as e:
        print('查無訂單,', e)
        template_data = {}

    return template_data

def checkoutOrder(order_data):
    try:
        order_number = order_data.get('order_number', '')
        order = Order.objects.get(order_number=order_number)
        if order:

            
            ret_json = {'status': 'ok', 'msg': f"訂單編號 {order.order_number} 付款成功"}
        else:
            ret_json = {'status': 'error', 'msg': f"訂單編號不存在"}
    except Exception as e:
        print('訂單付款失敗', e)
        ret_json = {'status': 'error', 'msg': str(e)}
    
    return ret_json


class CheckoutView(APIView):
    template_name = 'checkout.html'

    def get(self, request, id=None):
        if not request.user.is_authenticated:
            return redirect('shop:login')
        
        template_data = orderitems(id)
        
        if not template_data:
            return redirect('shop:myorders')
        return render(request, self.template_name, template_data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('shop:login')
        order_data = request.data
        user = request.user
        ret_json = checkoutOrder(order_data, user)

        return JsonResponse(ret_json)