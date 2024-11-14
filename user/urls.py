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
    path('update-profile/', update_profile, name='update_profile'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password_view, name='change_password'),
    path('create-shop/', create_shop, name='create_shop'),
    path('create-store-manager/', create_store_manager, name='create_store_manager'),
    path('shop/delete/<int:shop_id>/', delete_shop, name='delete_shop'),
    path('shop/deactivate/<int:shop_id>/', deactivate_shop, name='deactivate_shop'),
    path('user/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('user/deactivate/<int:user_id>/', deactivate_user, name='deactivate_user'),
]
