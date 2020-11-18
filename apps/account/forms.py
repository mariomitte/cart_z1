from django import forms
from django.contrib.auth.models import User

from .models import User
from apps.orders.models import Customer


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserChangePassword(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)
        widgets = {
                'password': forms.PasswordInput(),
            }

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password',]
        widgets = {
                'password': forms.PasswordInput(),
            }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
