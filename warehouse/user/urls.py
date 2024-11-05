
from django.urls import path, include
from .views import *

app_name = 'user' 

urlpatterns = [
     path('signup/', signup_view, name='signup'),
    path('verify/<int:user_id>/', verify_email_view, name='verify_email'),
    path('dashboard/', dashboard_view, name='dashboard'),
]