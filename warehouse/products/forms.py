# products/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'manufactured_date', 'expiry_date', 'pieces_per_box', 'boxes', 'pieces_left', 'boxes_left']
