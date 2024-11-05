# user/views.py
import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import User, VerificationCode
from .backends import RoleBasedBackend

def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.store_name = form.cleaned_data['storename']
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
            return redirect(RoleBasedBackend().get_user_dashboard(user))
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'user/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'user/dashboard.html')

@login_required
def store_manager_dashboard(request):
    return render(request, 'user/store_manager_dashboard.html')

@login_required
def shop_dashboard(request):
    return render(request, 'user/shop_dashboard.html')
