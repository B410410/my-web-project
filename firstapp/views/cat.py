import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse, HttpRequest
from rest_framework.response import Response


API_KEY = 'live_ O8LmztNY5sTzshwBLsZYUYTfpBKzVI jYyG7OW0qtA2owXqkFAsEFkGKTJMME QOsK'
BASE_URL = 'https://api.thecatapi.com/v1/images/search'

class CatView(APIView):
    template_name = 'cat.html'
    
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        headers = {
            'x-api-key': API_KEY  # 將 API 密鑰傳遞到 TheCatAPI 進行驗證
        }

        try:
            # 向 TheCatAPI 發送 GET 請求以獲取隨機貓咪圖片
            response = requests.get(BASE_URL, headers=headers)
            response.raise_for_status()  # 檢查請求是否成功，如果失敗，會拋出異常

            # 如果請求成功，處理回應資料
            if response.status_code == 200:
                data = response.json()  # 將回應的 JSON 資料轉換為 Python 字典
                cat_image_url = data[0]['url']  # 從資料中提取圖片 URL
                return Response({"cat_image_url": cat_image_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "無法取得貓咪圖片"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            # 異常處理：如果發生錯誤（如無法連接到 API），返回錯誤消息
            return Response({"error": f"請求失敗：{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
