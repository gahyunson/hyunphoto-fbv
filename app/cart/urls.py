from django.urls import path, include

from cart import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_list, name='cart-list'),
]