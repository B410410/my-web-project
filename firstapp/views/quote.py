from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import random
from rest_framework.views import APIView

def quote():
    quotes = [
        '失敗為成功之母',
        '嘗試做一些你不精通的事，否則你永遠不會成長',
        '嘗試一些事，遭遇失敗後從中學習，比你什麼事都不做更好',
        '走得多慢都無所謂，只要你不停下腳步',
        '成功，就是不斷地練習基本動作',
        '不要因為怕辛苦，就拒絕一個想法、夢想或目標，成功通常伴隨著辛苦',
        '當你真心渴望某件事，整個宇宙都會聯合起來幫助你完成'
    ]

    return random.choice(quotes)

class Doquote(APIView):
    template_name = 'quote.html'
    def get(self, request):
        data = quote()
        data_d = {'quote': data}

        return render(request, self.template_name, data_d)
    