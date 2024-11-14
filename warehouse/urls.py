
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403
from user import views

handler403 = 'user.views.custom_403'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', include('products.urls')),
    path('', include('orders.urls')),

]
