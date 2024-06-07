from django.urls import path
from .views import index,user_register,user_login,user_logout,all_products, detail,all_news, to_cart, cart, create_chekout_sessions, success_payment

urlpatterns = [
    path('', index, name="index"),
    path('products/', all_products, name='products'),
    path('register/', user_register, name="register"),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('detail/<int:pk>/', detail, name="detail"),
    path('new/', all_news, name='news'),
    path('to-cart/<int:product_id>/<str:action>/', to_cart, name='to-cart'),
    path('cart/', cart, name="cart"),

    path('payment/', create_chekout_sessions, name='payment'),
    path('success/', success_payment, name='success')
]
