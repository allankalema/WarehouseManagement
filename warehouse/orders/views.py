from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Order, OrderItem
from products.models import Product, Notification
from user.models import User
from django.db import transaction
from user.decorators import shop_required  # Assuming this is the decorator for shop users

# Decorator to ensure only shop users can add to cart and make orders
@shop_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.boxes_left <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('products:product_list')

    # Check if the product already exists in the cart (based on session or cart model)
    cart = request.session.get('cart', {})
    if str(product_id) not in cart:
        cart[str(product_id)] = {'boxes': 1, 'pieces': product.pieces_per_box}  # Default to 1 box
    else:
        cart[str(product_id)]['boxes'] += 1
        cart[str(product_id)]['pieces'] = cart[str(product_id)]['boxes'] * product.pieces_per_box

    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('products:product_list')

@shop_required
def cart(request):
    cart = request.session.get('cart', {})
    products_in_cart = []

    for product_id, details in cart.items():
        product = Product.objects.get(id=product_id)
        products_in_cart.append({
            'product': product,
            'boxes': details['boxes'],
            'pieces': details['pieces'],
        })

    return render(request, 'cart.html', {'products_in_cart': products_in_cart})

@shop_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Product removed from your cart.")
    return redirect('cart')

@shop_required
def make_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    # Create the order
    with transaction.atomic():
        order = Order.objects.create(user=request.user)

        # Add order items
        for product_id, details in cart.items():
            product = Product.objects.get(id=product_id)
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                boxes=details['boxes'],
                pieces=details['pieces'],
            )
            # Reduce stock accordingly
            product.boxes_left -= details['boxes']
            product.save()

        # Clear the cart after order creation
        del request.session['cart']

        # Send notifications
        store_name = request.user.store_name
        store_managers = User.objects.filter(store_name=store_name, store_manager=True) | User.objects.filter(store_name=store_name, owner=True)

        for manager in store_managers:
            message = f"{request.user.first_name} {request.user.last_name} has made an order from the {store_name} store."
            Notification.objects.create(user=manager, message=message)

        # Send email to store owner
        owner = User.objects.filter(store_name=store_name, owner=True).first()
        if owner:
            owner.email_user(
                "New Order Notification",
                f"An order has been placed by {request.user.first_name} {request.user.last_name}.",
            )

    # Show order confirmation message
    messages.success(request, "Your order has been placed successfully.")
    return redirect('orders:order_detail', pk=order.pk)
