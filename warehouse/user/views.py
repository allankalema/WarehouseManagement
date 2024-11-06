# user/views.py
import random
import string
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm
from .models import User, VerificationCode
from .backends import RoleBasedBackend
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import *
from .backends import RoleBasedBackend

from django.utils.crypto import get_random_string

def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.store_name = form.cleaned_data['store_name']
            user.owner = True
            user.is_active = False  # Set inactive until verification
            user.save()

            code = generate_verification_code()
            VerificationCode.objects.create(user=user, code=code)

            send_mail(
                'Your Verification Code',
                f'Your verification code is {code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Account created successfully! Please verify your email.')

            return redirect('user:verify_email', user_id=user.id)
    else:
        form = UserRegistrationForm()
    return render(request, 'user/signup.html', {'form': form})

def verify_email_view(request, user_id):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            user = User.objects.get(id=user_id)
            verification = VerificationCode.objects.get(user=user, code=code)

            user.is_active = True
            user.save()
            verification.delete()

            send_mail(
                'Account Registration Successful',
                'Congratulations! Your account registration is complete.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            login(request, user)
            messages.success(request, 'Your email has been verified successfully!')

            return redirect(RoleBasedBackend().get_user_dashboard(user))
        except VerificationCode.DoesNotExist:
            messages.error(request, "Verification code is incorrect.")
            return redirect('user:verify_email', user_id=user_id)
    return render(request, 'user/verify_email.html', {'user_id': user_id})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')

            return redirect(RoleBasedBackend().get_user_dashboard(user))
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'user/login.html')

@owner_required
def dashboard_view(request):
    return render(request, 'user/dashboard.html')

@store_manager_required
def store_manager_dashboard(request):
    return render(request, 'user/store_manager_dashboard.html')

@shop_required
def shop_dashboard(request):
    return render(request, 'user/shop_dashboard.html')


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')

            return redirect(RoleBasedBackend().get_user_dashboard(user))  # Redirect to the user's main dashboard
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'user/update_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('user:login')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')

            # Send email notification
            send_mail(
                'Password Change Notification',
                'Your password was successfully changed.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return redirect(RoleBasedBackend().get_user_dashboard(user))  # Redirect to the dashboard after success
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/change_password.html', {'form': form})

def custom_403(request, exception=None):
    return render(request, 'user/403.html', status=403)


@login_required
@owner_required
def create_shop(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = get_random_string(length=8)  # Generate random password
        username = email.split('@')[0]  # Create a username from email

        # Create new shop user
        shop_user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            store_name=request.user.store_name,
            shop=True,
            owner=False,
            store_manager=False,
            password=password
        )

        # Email shop user their credentials
        send_mail(
            'Shop Account Created',
            f'Your account has been created:\nUsername: {username}\nPassword: {password}\nPlease log in and change your password.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Notify the owner
        send_mail(
            'Shop Account Registered',
            f'A new shop account has been created for {first_name} {last_name} (Email: {email}).',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )
        messages.success(request, 'Shop has successfully been created and active the user should login to that email to get the credentials')
        return redirect('user:dashboard')

    return render(request, 'user/create_shop.html')


@login_required
@owner_required
def create_store_manager(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = get_random_string(length=8)  # Generate random password
        username = email.split('@')[0]  # Create a username from email

        # Create new store manager user
        manager_user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            store_name=request.user.store_name,
            shop=False,
            owner=False,
            store_manager=True,
            password=password
        )

        # Email store manager user their credentials
        send_mail(
            'Store Manager Account Created',
            f'Your account has been created:\nUsername: {username}\nPassword: {password}\nPlease log in and change your password.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Notify the owner
        send_mail(
            'Store Manager Account Registered',
            f'A new store manager account has been created for {first_name} {last_name} (Email: {email}).',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )
        messages.success(request, 'Store manager account successfully created and working. the user should login to that email to get the credentials')
        return redirect('user:dashboard')

    return render(request, 'user/create_store_manager.html')