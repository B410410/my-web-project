from django.urls import path
from .views.product import ShopProduct
from .views.product_d import Product_d
from .views.Cart import CartView
from .views.Login import LoginView
from .views.Logout import logout_view
from .views.contact import Contact
from .views.profile import ProfileView
from .views.order import OrderView
from .views.myorders import MyOrdersView
from .views.checkout import CheckoutView

# 添加 app_name 很重要
app_name = 'shop'

urlpatterns =[
    path('login/', LoginView.as_view(), name='login'),                                   # 登入
    path('logout/', logout_view, name='logout'),                                         # 登出
    path('profile/', ProfileView.as_view(), name='profile'),                             # 用戶資料
    path('', ShopProduct.as_view(), name='product'),                                     # 商品頁面
    path('<int:slu>/', Product_d.as_view(), name='product_detail'),                      # 商品詳細資料
    path('category/<int:category_id>/', ShopProduct.as_view(), name='product_category'), # 商品類別
    path('cart/', CartView.as_view(), name='cart'),                                      # 購物車
    path('order/', OrderView.as_view(), name='order'),                                   # 下單頁面
    path('checkout/<int:id>/', CheckoutView.as_view(), name='checkout'),           # 結帳
    path('myorders/', MyOrdersView.as_view(), name='myorders'),                          # 檢視訂單
    path('contact/', Contact.as_view(), name='contact')                                  # 聯絡客服
]