# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Notification
from .forms import *
from user.decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model


@login_required
def product_list(request):
    user_store_name = request.user.store_name  # Get the store_name of the logged-in user
    products = Product.objects.filter(store_name=user_store_name)  # Fetch products only for this store
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

            create_product_notification(product)

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
        f"New Product Has been added to the ware house: {product.name}",
        f"A new product '{product.name}' was added  to your store '{store_name}'.",
        settings.DEFAULT_FROM_EMAIL,
        [owner.email],
        fail_silently=False,
    )

    # Send to the shops (exclude store managers)
    User = get_user_model()  # Get the actual user model class
    shop_users = User.objects.filter(store_name=store_name).exclude(store_manager=True)
    for shop_user in shop_users:
        send_mail(
            f"New Product Has been added  called : {product.name}",
            f"A new product '{product.name}' was added  to your store '{store_name}'. You can go ahead and make orders ",
            settings.DEFAULT_FROM_EMAIL,
            [shop_user.email],
            fail_silently=False,
        )


def home(request):
    return render(request, 'products/home.html')

def create_product_notification(product):
    """Creates notifications for the store owner and associated shop users."""
    store_name = product.store_name
    owner = product.user  # Store manager who created the product

    # Create a notification for the store manager (owner)
    Notification.objects.create(
        user=owner,
        message=f"New product '{product.name}' was added to your store '{store_name}'."
    )

    # Create notifications for shop users associated with this store
    User = get_user_model()
    shop_users = User.objects.filter(store_name=store_name).exclude(id=owner.id)
    for shop_user in shop_users:
        Notification.objects.create(
            user=shop_user,
            message=f"A new product '{product.name}' was added to '{store_name}'."
        )


@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    # Optionally mark all notifications as seen after viewing
    notifications.update(is_seen=True)
    return render(request, 'products/notifications_page.html', {'notifications': notifications})




@store_manager_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, store_name=request.user.store_name)  # Ensure product belongs to user's store
    old_boxes_count = product.boxes  # Store the original number of boxes

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            
            # Check if boxes count has increased
            if product.boxes > old_boxes_count:
                send_product_update_notification(product, old_boxes_count, product.boxes)

            messages.success(request, "Product updated successfully.")
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_update.html', {'form': form, 'product': product})

def send_product_update_notification(product, old_boxes, new_boxes):
    message = (f"The product '{product.name}' has been restocked. "
               f"more boxes have been added in to the store")
    store_name = product.store_name
    User = get_user_model()

    # Notify all users of the same store
    users_to_notify = User.objects.filter(store_name=store_name)
    notifications = [
        Notification(user=user, message=message)
        for user in users_to_notify
    ]
    Notification.objects.bulk_create(notifications)