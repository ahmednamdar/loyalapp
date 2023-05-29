from django import forms
from django.contrib import admin
from .models import Order


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'customer': forms.Select(attrs={'hx-post': '/tribute', 'hx-trigger': 'change '}),
        }
