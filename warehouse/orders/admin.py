from django.contrib import admin
from .models import Order, OrderItem

# Inline admin interface for OrderItems within the Order admin view
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Add a new empty form for each order
    fields = ('product', 'boxes', 'pieces')  # Display these fields in the inline form
    readonly_fields = ('product',)  # Make the product field readonly since it's already associated

# Custom Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'date', 'store_manager')  # Displayed columns in the list view
    list_filter = ('status', 'date', 'store_manager')  # Filters for status, date, and store manager
    search_fields = ('user__username', 'store_manager__username')  # Search orders by user or store manager
    ordering = ('-date',)  # Order by date in descending order (latest first)
    inlines = [OrderItemInline]  # Add the inline for order items inside the order view

    def get_readonly_fields(self, request, obj=None):
        """Make the `user` and `store_manager` fields readonly in certain cases."""
        if obj:  # If the object is being edited (not created)
            return ['user', 'store_manager']
        return []

# Register the models and their admin classes
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
