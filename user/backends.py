# user/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User

class RoleBasedBackend(ModelBackend):
    def get_user_dashboard(self, user):
        if user.owner:
            return 'user:dashboard'
        elif user.store_manager:
            return 'user:store_manager_dashboard'
        elif user.shop:
            return 'user:shop_dashboard'
        return 'user:dashboard'
