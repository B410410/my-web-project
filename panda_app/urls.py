from django.urls import path
from .views.excel01 import Excel01

urlpatterns =[
    path('excel01/', Excel01.as_view(), name='Excel01'),
]