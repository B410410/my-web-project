from django.urls import path
from .views.product import ShopProduct
from .views.Cart import Cart
from .views.testHtml import listing
from .views.testProduct import detail
from .views.Login import LoginView

# 添加 app_name 很重要
app_name = 'shop'

urlpatterns =[
    path('login/', LoginView.as_view(), name='login'), # 登入頁面
    path('product/', ShopProduct.as_view(), name='product'), # 商品頁面
    path('cart/', Cart.as_view(), name='cart'), # 購物車
    path('testhtml/', listing), # 測試練習
    path('testhtml/<str:id>', detail),
]