# user/decorators.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from functools import wraps

def owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.owner:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied  # or return HttpResponseRedirect(reverse('user:dashboard'))
    return _wrapped_view

def store_manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.store_manager:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied  # or return HttpResponseRedirect(reverse('user:dashboard'))
    return _wrapped_view

def shop_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.shop:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied  # or return HttpResponseRedirect(reverse('user:dashboard'))
    return _wrapped_view
