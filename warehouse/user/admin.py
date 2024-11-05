# user/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'store_name')}),
        ('Permissions', {'fields': ('owner', 'store_manager', 'shop', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'store_name', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'store_name', 'owner', 'store_manager', 'shop', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
