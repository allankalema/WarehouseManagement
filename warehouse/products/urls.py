# products/urls.py
from django.urls import path
from .views import product_list

app_name = 'products'

urlpatterns = [
    path('product-list/', product_list, name='product_list'),
]
