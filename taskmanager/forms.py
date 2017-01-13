from django import forms
from django.forms import PasswordInput


class LoginForm(forms.Form):
    login = forms.CharField(label='Your name', max_length=100)
    password = forms.CharField(label='Your name', max_length=100, widget=PasswordInput())
