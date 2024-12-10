from django.urls import path
from .views.views import ToDoList
from .views.quote import Doquote
from .views.cat import CatView

app_name = 'app'

urlpatterns =[
    path('firstapp/', ToDoList.as_view(), name='todo-list'),
    path('quote/', Doquote.as_view(), name='quote'),
    path('cat/', CatView.as_view(), name='cat'),
]