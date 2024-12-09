from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, order
from ..serializers import ProductSerializer
from django.http import JsonResponse

def Get_Product():
    pass




class Cart(APIView):
    template_name ='Cart.html'

    def get(self, request):
        data = {}
        # data = Get_Product()

        return render(request, self.template_name, data)
    
    def post(self, request):
        data_form = request.data
        ret_json = {}
        # ret_json = Post_Product(data_form)

        return JsonResponse(ret_json)