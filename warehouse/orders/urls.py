from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart, name='cart'), 
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('make_order/', views.make_order, name='make_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('store-orders/', views.store_orders_view, name='store_orders'),
]
