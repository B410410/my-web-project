from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn.models import PayPalIPN
from django.http import JsonResponse
from rest_framework.views import APIView
from ..models import Order

@csrf_exempt
def paypal_ipn(request):
    """
    PayPal IPN 回調處理
    """
    if request.method == "POST":
        ipn_obj = PayPalIPN(request.POST)  # 從 POST 請求中取得 PayPal IPN 數據
        ipn_obj.save()  # 保存 IPN 數據

        # 如果付款成功
        if ipn_obj.payment_status == "Completed":
            order_number = ipn_obj.invoice  # 訂單號通常存儲在 'invoice' 字段中
            try:
                # 查找對應的訂單
                order = Order.objects.get(order_number=order_number)
                order.status = "Paid"  # 更新訂單狀態為已付款
                order.save()
                return JsonResponse({"status": "success", "msg": "Payment successful"})
            except Order.DoesNotExist:
                return JsonResponse({"status": "error", "msg": "Order not found"})
        else:
            return JsonResponse({"status": "error", "msg": "Payment not completed"})
    return JsonResponse({"status": "error", "msg": "Invalid request"})
