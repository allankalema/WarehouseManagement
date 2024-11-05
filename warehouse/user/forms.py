# user/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    storename = forms.CharField(required=True, label="Store Name")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'storename', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            self.add_error('password2', "Passwords do not match.")
