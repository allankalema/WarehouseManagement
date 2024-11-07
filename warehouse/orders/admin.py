from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

# Inline display for OrderItem within the Order admin view
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Show one extra empty form
    fields = ('product', 'boxes', 'pieces')

# Order admin with inline OrderItems
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store_manager', 'status', 'date')
    list_filter = ('status', 'date', 'store_manager')
    search_fields = ('user__username', 'store_manager__username')
    inlines = [OrderItemInline]

# Admin for OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'boxes', 'pieces')
    search_fields = ('order__id', 'product__name')

# Inline display for CartItem within the Cart admin view
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ('product', 'quantity')

# Cart admin with inline CartItems
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'boxes', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')
    inlines = [CartItemInline]

# Admin for CartItem
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    search_fields = ('cart__id', 'product__name')
