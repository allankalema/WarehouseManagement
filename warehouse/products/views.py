# products/views.py
from django.shortcuts import render, redirect
from .models import Product
from .forms import *
from user.decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model


@login_required
def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'products/product_list.html', {'products': products})


@store_manager_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Save product with auto-filled fields
            product = form.save(commit=False)
            product.user = request.user
            product.store_name = request.user.store_name  # Automatically fill store_name
            product.save()

            # Send email to the store owner and shops
            send_product_creation_email(product)

            messages.success(request, "Product created successfully.")
            return redirect('products:product_list')
    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form})

def send_product_creation_email(product):
    store_name = product.store_name
    owner = product.user  # Store manager's user (the one who created the product)

    # Send to the owner
    send_mail(
        f"New Product Created: {product.name}",
        f"A new product '{product.name}' was created in your store '{store_name}'.",
        settings.DEFAULT_FROM_EMAIL,
        [owner.email],
        fail_silently=False,
    )

    # Send to the shops (exclude store managers)
    User = get_user_model()  # Get the actual user model class
    shop_users = User.objects.filter(store_name=store_name).exclude(storemanager=True)
    for shop_user in shop_users:
        send_mail(
            f"New Product Created: {product.name}",
            f"A new product '{product.name}' was created in your store '{store_name}'.",
            settings.DEFAULT_FROM_EMAIL,
            [shop_user.email],
            fail_silently=False,
        )