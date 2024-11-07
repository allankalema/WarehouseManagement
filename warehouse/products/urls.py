# products/urls.py
from django.urls import path
from .views import*

app_name = 'products'

urlpatterns = [
    path('product-list/', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('', home, name='home'),
    path('notifications/',notifications_page, name='notifications_page'),
    path('update/<int:pk>/',product_update, name='product_update'),
]
