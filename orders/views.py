from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Order, OrderItem, Cart
from products.models import Product, Notification
from user.models import User
from django.conf import settings
from user.decorators import *
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
    # Get the user's cart items
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('orders:cart')

    with transaction.atomic():
        # Get the store name from the user's profile
        store_name = request.user.store_name

        # Create a new order with the store name
        order = Order.objects.create(user=request.user, store_name=store_name)

        # Update each CartItem's boxes count based on the form data
        for item in cart_items:
            product = item.product
            # Get the boxes count from the form data
            boxes = request.POST.get(f'boxes_{product.id}')
            if boxes is not None and boxes.isdigit():
                item.boxes = int(boxes)  # Update the CartItem boxes count
                item.save()
            
            # Create an OrderItem using the updated boxes count
            OrderItem.objects.create(
                order=order,
                product=product,
                boxes=item.boxes,
                pieces=item.boxes * product.pieces_per_box
            )
            
        # Clear the user's cart after the order is created
        cart_items.delete()

        # Notify store managers and the store owner
        store_managers = User.objects.filter(
            store_name=store_name,
            store_manager=True
        ) | User.objects.filter(store_name=store_name, owner=True)

        for manager in store_managers:
            Notification.objects.create(
                user=manager,
                message=f"{request.user.first_name} {request.user.last_name} has made an order from {store_name}."
            )

        # Send email to the store owner if they exist
        owner = User.objects.filter(store_name=store_name, owner=True).first()
        if owner:
            send_mail(
                "New Order Notification",
                f"An order has been placed by {request.user.first_name} {request.user.last_name}.",
                'noreply@example.com',
                [owner.email],
            )

    # Success message and redirect
    messages.success(request, "Your order has been placed successfully.")
    return redirect('orders:order_detail', order_id=order.pk)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

@store_manager_required
@login_required
def store_orders_view(request):
    # Get all orders with store_name matching the logged-in user's store_name and status 'pending'
    store_orders = Order.objects.filter(store_name=request.user.store_name, status='pending')
    
    # Group orders by user
    orders_by_user = {}
    for order in store_orders:
        user_orders = orders_by_user.setdefault(order.user, [])
        user_orders.append(order)
    
    context = {
        'orders_by_user': orders_by_user,
    }
    return render(request, 'orders/store_orders.html', context)


@store_manager_required
def order_confirmation_and_rejection(request):
    # Query all orders for the current store manager's store name
    orders = Order.objects.filter(store_name=request.user.store_name)
    
    orders_by_user = {}
    for order in orders:
        if order.user not in orders_by_user:
            orders_by_user[order.user] = []
        orders_by_user[order.user].append(order)

    if request.method == "POST":
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = get_object_or_404(Order, id=order_id)

        if action == "approve":
            # Change order status to approved
            order.status = 'approved'
            order.save()

            # Send email to the user who placed the order
            send_mail(
                'Order Approved',
                f'Your order {order.id} has been approved by the store manager.',
                settings.DEFAULT_FROM_EMAIL,
                [order.user.email]
            )

            # Create a notification for the user
            Notification.objects.create(
                user=order.user,
                message=f'Your order {order.id} has been approved.',
                is_seen=False,
            )

            # Send email to other store managers with the same store name
            store_managers = User.objects.filter(store_name=order.store_name, store_manager=True).exclude(id=order.user.id)
            for manager in store_managers:
                send_mail(
                    'Order Approved Notification',
                    f'Order {order.id} has been approved by the store manager.',
                    settings.DEFAULT_FROM_EMAIL,
                    [manager.email]
                )

            # Update product stock based on each item in the order
            for order_item in order.items.all():
                product = order_item.product
                product.boxes_left -= order_item.boxes
                product.pieces_left = product.boxes_left * product.pieces_per_box
                product.save()

            messages.success(request, f'Order {order.id} has been approved successfully.')

        elif action == "reject":
            # Change order status to rejected
            order.status = 'rejected'
            order.save()

            # Send email to the user who placed the order
            send_mail(
                'Order Rejected',
                f'Your order {order.id} has been rejected by the store manager.',
                settings.DEFAULT_FROM_EMAIL,
                [order.user.email]
            )

            # Create a notification for the user
            Notification.objects.create(
                user=order.user,
                message=f'Your order {order.id} has been rejected.',
                is_seen=False,
            )

            # Send email to other store managers with the same store name
            store_managers = User.objects.filter(store_name=order.store_name, store_manager=True).exclude(id=order.user.id)
            for manager in store_managers:
                send_mail(
                    'Order Rejected Notification',
                    f'Order {order.id} has been rejected by the store manager.',
                    settings.DEFAULT_FROM_EMAIL,
                    [manager.email]
                )

            messages.warning(request, f'Order {order.id} has been rejected.')

        return redirect('orders:store_orders')

    return render(request, 'orders/store_orders.html', {'orders_by_user': orders_by_user})
