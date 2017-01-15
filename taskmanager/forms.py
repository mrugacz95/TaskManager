import datetime
from audioop import reverse

from crispy_forms.layout import Submit
from django import forms
from django.forms import PasswordInput
from crispy_forms.helper import FormHelper

from taskmanager import views


class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=100)
    password = forms.CharField(label='password', max_length=100, widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('login', 'Sign In'))


class RegisterForm(forms.Form):
    login = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=PasswordInput())
    repeatPassword = forms.CharField(label='Repeat password', max_length=100, widget=PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('register', 'Register'))
        self.helper.field_class = 'text-input'


class AddTaskForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=200)
    deadline = forms.DateField(label='Deadline', initial=datetime.date.today)
    label = forms.CharField(label='Label', max_length=100)

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
