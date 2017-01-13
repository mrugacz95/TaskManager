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
        self.helper.add_input(Submit('submit', 'Submit'))


class AddTaskForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    description = forms.CharField(label='description', max_length=200)
    deadline = forms.DateField(label='deadline', initial=datetime.date.today)
    label = forms.CharField(label='label', max_length=100)

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
