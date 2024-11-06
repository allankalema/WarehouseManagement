# products/admin.py
from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'manufactured_date', 'expiry_date', 'boxes', 'pieces_per_box', 'pieces_left', 'boxes_left', 'section', 'user','store_name','created_at',)  # Add all the fields to list_display
    search_fields = ('name', 'description', 'section', 'user__email')  # Allow search by these fields
    list_filter = ('manufactured_date', 'expiry_date', 'section', 'user')  # Enable filtering

admin.site.register(Product, ProductAdmin)
