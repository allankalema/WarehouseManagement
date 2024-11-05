# user/urls.py
from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('verify/<int:user_id>/', verify_email_view, name='verify_email'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('store-manager-dashboard/', store_manager_dashboard, name='store_manager_dashboard'),
    path('shop-dashboard/', shop_dashboard, name='shop_dashboard'),
]
