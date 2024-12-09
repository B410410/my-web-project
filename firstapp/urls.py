from django.urls import path
from .views.views import ToDoList
from .views.quote import Doquote

urlpatterns =[
    path('firstapp', ToDoList.as_view(), name='todo-list'),
    path('quote', Doquote.as_view(), name='quote'),
]