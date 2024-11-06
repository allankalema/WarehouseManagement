# products/views.py
from django.shortcuts import render
from .models import Product
from user.decorators import *
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'products/product_list.html', {'products': products})
