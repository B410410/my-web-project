from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.urls import reverse

class LoginView(APIView):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return JsonResponse({
                'status': 'error',
                'detail': '帳號和密碼為必填'
            }, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'ok',
                'message': '登入成功',
                'redirect': reverse('shop:product')
            }, status=200)
        else:
            return JsonResponse({
                'status': 'error',
                'detail': '帳號或密碼錯誤'
            }, status=401)