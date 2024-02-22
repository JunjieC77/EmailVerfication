from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),  # 注册页面的URL路由
    path('activate//<token>/', views.activate, name='activate'),  # 激活链接的URL路由
    path('sented',views.registration_activation_sent, name='registration_activation_sent'),
    path('completed',views.registration_activation_complete, name='registration_activation_complete')
]