from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Order, OrderItem, Cart
from products.models import Product, Notification
from user.models import User
from django.db import transaction
from django.core.mail import send_mail
from user.decorators import shop_required  # Assuming this is the decorator for shop users

@shop_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.boxes_left <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('products:product_list')

    # Check if item is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.boxes += 1
    cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect('products:product_list')

@shop_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    products_in_cart = [{'product': item.product, 'boxes': item.boxes, 'pieces': item.boxes * item.product.pieces_per_box} for item in cart_items]

    return render(request, 'cart.html', {'products_in_cart': products_in_cart})

@shop_required
def remove_from_cart(request, product_id):
    try:
        cart_item = Cart.objects.get(user=request.user, product_id=product_id)
        cart_item.delete()
        messages.success(request, "Product removed from your cart.")
    except Cart.DoesNotExist:
        messages.error(request, "This product is not in your cart.")
    return redirect('orders:cart')


@shop_required
def make_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('orders:cart')

    with transaction.atomic():
        order = Order.objects.create(user=request.user)

        for item in cart_items:
            product = item.product
            OrderItem.objects.create(
                order=order,
                product=product,
                boxes=item.boxes,
                pieces=item.boxes * product.pieces_per_box,
            )
            product.boxes_left -= item.boxes
            product.save()

        # Clear the cart
        cart_items.delete()

        # Send notifications
        store_name = request.user.store_name
        store_managers = User.objects.filter(
            store_name=store_name,
            store_manager=True
        ) | User.objects.filter(store_name=store_name, owner=True)

        for manager in store_managers:
            Notification.objects.create(
                user=manager,
                message=f"{request.user.first_name} {request.user.last_name} has made an order from {store_name}."
            )

        # Send email to store owner
        owner = User.objects.filter(store_name=store_name, owner=True).first()
        if owner:
            send_mail(
                "New Order Notification",
                f"An order has been placed by {request.user.first_name} {request.user.last_name}.",
                'noreply@example.com',
                [owner.email],
            )

    messages.success(request, "Your order has been placed successfully.")
    return redirect('orders:order_detail', pk=order.pk)