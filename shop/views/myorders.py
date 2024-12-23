from django.shortcuts import render, redirect
from rest_framework.views import APIView
from shop.views.Cart import CustomCart
from shop.models import Order, OrderItem, Product
from django.http import JsonResponse
from .. import serializers


def get_order(user):
    try:
        orders = Order.objects.filter(user=user)
        if orders:
            orders_j = serializers.OrderSerializer(orders, many=True)
            ret_json = {'orders': orders_j.data}
        else:
            ret_json = {'orders': []}
    except Exception as e:
        ret_json = {'status': 'error', 'msg': str(e)}

    return ret_json

def get_order_item(data):
    try:
        order_number = data.get('order_number', '')
        if order_number:
            order_item = OrderItem.objects.filter(order__order_number=order_number)
            order_item_j = serializers.OrderItemSerializer(order_item, many=True)
            ret_json = {'status': 'ok', 'order_items': order_item_j.data}
        else:
            ret_json = {'status': 'error', 'order_items': [], 'msg': '查無訂單明細'}
    except Exception as e:
        ret_json = {'status': 'error', 'msg': str(e)}

    return ret_json

class MyOrdersView(APIView):
    template_name = 'myorders.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('shop:login')
        
        user = request.user
        ret_json = get_order(user)

        return render(request, self.template_name, ret_json)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('shop:login')
        
        data = request.data
        user = request.user
        ret_json = get_order_item(data)

        return JsonResponse(ret_json)
