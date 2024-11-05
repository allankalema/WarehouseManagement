# user/views.py
import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm
from .models import User, VerificationCode

def generate_verification_code(length=6):
    """Generates a random code of letters and numbers."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_owner = True
            user.is_active = False  # Set inactive until verification
            user.save()

            # Generate and save the verification code
            code = generate_verification_code()
            VerificationCode.objects.create(user=user, code=code)

            # Send verification code to user's email
            send_mail(
                'Your Verification Code',
                f'Your verification code is {code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            # Redirect to verification page
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

            # If code is valid, activate the user and delete the code
            user.is_active = True
            user.save()
            verification.delete()

            return redirect('user:dashboard')  # Redirect to dashboard on success
        except VerificationCode.DoesNotExist:
            messages.error(request, "Verification code is incorrect.")
            return redirect('user:verify_email', user_id=user_id)
    return render(request, 'user/verify_email.html', {'user_id': user_id})

def dashboard_view(request):
    return render(request, 'user/dashboard.html')
