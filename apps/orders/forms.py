from django.conf import settings
from django import forms
from django.db import transaction
from django.contrib import messages

from .models import Customer, Order, ShippingAddress, CreditCard


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ('warning', 'submitted')

class EditShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ('email', 'warning', 'submitted',)

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('birth_date', 'gender', 'contact', 'photo')
        widgets = {
            'birth_date': forms.DateInput(
                attrs = {'placeholder': 'Y-M-D'},
            ),
        }

class CreditCardEditForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        exclude = ('customer', 'credit_card_expiration_date')
        widgets = {
            'credit_card_number': forms.NumberInput(
                attrs = {'placeholder': '0000000000000'},
            ),
            'credit_card_cvc': forms.NumberInput(
                attrs = {'placeholder': '000'},
            ),
            'month_date': forms.NumberInput(
                attrs = {'placeholder': '00'},
            ),
            'year_date': forms.NumberInput(
                attrs = {'placeholder': '00'},
            ),
        }
