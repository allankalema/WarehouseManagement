from django.contrib import admin
from .models import Product, Notification

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'manufactured_date', 'expiry_date', 
        'boxes', 'pieces_per_box', 'pieces_left', 'boxes_left', 
        'section', 'user', 'store_name', 'created_at'
    )
    search_fields = ('name', 'description', 'section', 'user__email')  # Search by these fields
    list_filter = ('manufactured_date', 'expiry_date', 'section', 'user')  # Enable filtering

admin.site.register(Product, ProductAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_seen', 'created_at')  # No need for product if it's not related
    search_fields = ('user__email', 'message')  # Search by user email and message content
    list_filter = ('is_seen', 'created_at', 'user')  # Enable filtering by seen status, creation date, and user

    # Mark notifications as seen directly in the admin interface (custom action)
    actions = ['mark_as_seen']

    def mark_as_seen(self, request, queryset):
        """Mark selected notifications as seen."""
        updated_count = queryset.update(is_seen=True)
        self.message_user(request, f'{updated_count} notifications marked as seen.')
    mark_as_seen.short_description = "Mark selected notifications as seen"

admin.site.register(Notification, NotificationAdmin)
