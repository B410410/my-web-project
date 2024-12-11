from django.urls import path
from .views.product import ShopProduct
from .views.Cart import Cart
from .views.testHtml import listing
from .views.testProduct import detail
from .views.Login import LoginView
from .views.Logout import logout_view
from .views.contact import Contact
from .views.profile import ProfileView

# 添加 app_name 很重要
app_name = 'shop'

urlpatterns =[
    path('login/', LoginView.as_view(), name='login'), # 登入
    path('logout/', logout_view, name='logout'), # 登出
    path('profile/', ProfileView.as_view(), name='profile'), #用戶資料
    path('product/', ShopProduct.as_view(), name='product'), # 商品頁面
    path('product/<int:slu>/', ShopProduct.as_view(), name='product_detail'), # 單個商品
    path('cart/', Cart.as_view(), name='cart'), # 購物車
    path('testhtml/', listing), # 測試練習
    path('testhtml01/', detail),
    path('contact/', Contact.as_view(), name='contact') #聯絡客服
]