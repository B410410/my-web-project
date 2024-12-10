from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class ProfileView(APIView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('shop:login')

        user = request.user
        data = {
            'user': user
        }

        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name', '')
        email = data.get('email', '')
        password = data.get('password', '')
        user = request.user

        # 驗證email格式
        if email and not self.is_valid_email(email):
            return Response({'status': 'error', 'msg': '無效的email格式'}, status=400)

        if name:
            user.username = name
        if email:
            user.email = email
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)
        
        user.save()

        return Response({'status': 'ok', 'msg': '資料已更新'})

    # 檢查email格式是否有效
    def is_valid_email(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
