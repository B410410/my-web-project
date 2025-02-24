"""
URL configuration for my_web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop.views import paypal_ipn

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('firstapp.urls')),
    path('shop/', include('shop.urls')),
    path('filer/', include('filer.urls')),
    path('panda/', include('panda_app.urls')),
    path('captcha/', include('captcha.urls')),                          # 機器人驗證模組
    path('accounts/', include('registration.backends.default.urls')),   # 帳號註冊驗證
    # path('paypal/ipn/', paypal_ipn, name='paypal_ipn'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)