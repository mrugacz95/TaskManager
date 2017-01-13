import datetime
import hashlib

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from taskmanager.auth import TOKEN, createToken, getCurrentUser, authentication
from taskmanager.forms import LoginForm
from taskmanager.models import User, Task, Token


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


@authentication
def tasks(request):
    user = getCurrentUser(request)
    print(user.name)
    try:
        tasks = Task.objects.filter(usertask__user_name=user.name)
        return render(request, 'taskmanager/tasks.html', {'tasks': tasks})
    except Task.DoesNotExist:
        return render(request, 'taskmanager/tasks.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            formLogin = form.cleaned_data['login']
            formPassword = form.cleaned_data['password']
            try:
                formUser = User.objects.get(pk=formLogin)
                m = hashlib.md5()
                m.update(formPassword.encode('utf-8'))
                hashedPassword = m.hexdigest()
                print(hashedPassword)
                if formUser.password == hashedPassword:
                    token = request.COOKIES.get(TOKEN)
                    if token == '':
                        tokenObject = createToken()
                    else:
                        try:
                            tokenObject = Token.objects.get(access_token=token)
                            if tokenObject.expiration_date < timezone.now():
                                tokenObject = createToken()
                        except Token.DoesNotExist:
                            tokenObject = createToken()
                    formUser.token_token_id = tokenObject.pk
                    formUser.save()
                    res = HttpResponseRedirect('tasks/')
                    set_cookie(res, TOKEN, tokenObject.access_token)
                    return res
            except User.DoesNotExist:
                pass
    return render(request, 'taskmanager/login.html', {'problem': True})


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 7 * 24 * 60 * 60  # week
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)


def logout(request):
    res = render(request, 'taskmanager/login.html', {'problem': False})
    res.delete_cookie(TOKEN)
    return res
