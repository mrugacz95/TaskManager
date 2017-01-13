import os

import binascii
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import status
from rest_framework.response import Response
import hashlib
import datetime
from taskmanager.forms import LoginForm
from taskmanager.models import User, Role, Task, Token, UserTask

TOKEN = 'TOKEN_COOKIE'


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def users(request):
    users = User.objects.all()
    return render(request, 'taskmanager/users.html', {'users': users})


def user(request, user_name):
    user = get_object_or_404(User, pk=user_name)
    tasks = Task.objects.select_related(user_name)
    user.tasks = tasks
    return render(request, 'taskmanager/user.html', {'user': user})


def task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'taskmanager/task.html', {'task': task})


def authentication(func):
    def wrapper(*args, **kw):
        request = args[0]
        token = request.COOKIES.get(TOKEN)
        print('trying with ' + token)
        tokens = Token.objects.all()
        for tok in tokens:
            print(tok.access_token)
        try:
            tokenObject = Token.objects.get(access_token=token)
            print('authoricated with ' + tokenObject.access_token)
            return func(*args, **kw)
        except Token.DoesNotExist:
            return no_auth(request)

    return wrapper


@authentication
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'taskmanager/tasks.html', {'tasks': tasks})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            formLogin = form.cleaned_data['login']
            formPassword = form.cleaned_data['password']
            formUser = User.objects.get(pk=formLogin)
            m = hashlib.md5()
            m.update(formPassword.encode('utf-8'))
            hashedPassword = m.hexdigest()
            randomToken = binascii.hexlify(os.urandom(32))
            expirationDate = datetime.datetime.now() + datetime.timedelta(days=7)
            try:
                tokenObject = Token.objects.create(access_token=randomToken, expiration_date=expirationDate)
                if formUser.password == hashedPassword:
                    res = HttpResponseRedirect('tasks')
                    set_cookie(res, TOKEN, randomToken)
                    return res
            except Token.DoesNotExist:
                pass
    return render(request, 'taskmanager/login.html', {})


def no_auth(request):
    return HttpResponse("brak autoryzacji", status=status.HTTP_403_FORBIDDEN)


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 7 * 24 * 60 * 60  # week
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)
