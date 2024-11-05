from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    store_name = forms.CharField(required=True, label="Store Name")  # Changed field name to store_name

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'store_name', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            self.add_error('password2', "Passwords do not match.")
