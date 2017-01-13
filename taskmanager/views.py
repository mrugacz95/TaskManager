import datetime
import hashlib

from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from taskmanager.auth import TOKEN, createToken, getCurrentUser, authentication
from taskmanager.forms import LoginForm, AddTaskForm
from taskmanager.models import User, Task, Token, UserTask


def users(request):
    users = User.objects.all()
    return render(request, 'taskmanager/users.html', {'users': users})


def user(request, user_name):
    user = get_object_or_404(User, pk=user_name)
    tasks = Task.objects.select_related(user_name)
    user.tasks = tasks
    return render(request, 'taskmanager/user.html', {'user': user})


@authentication
def task(request, task_id):
    user = getCurrentUser(request)
    try:
        task = get_object_or_404(Task.objects.filter(id=task_id, usertask__user_name__name=user.name))
        return render(request, 'taskmanager/task.html', {'task': task})
    except Task.DoesNotExist:
        return HttpResponse(status=404)


@authentication
def tasks(request):
    user = getCurrentUser(request)
    try:
        tasks = Task.objects.filter(usertask__user_name=user.name)
        return render(request, 'taskmanager/tasks.html', {'tasks': tasks, 'user': user})
    except Task.DoesNotExist:
        return render(request, 'taskmanager/tasks.html')


def login(request):
    response = render(request, 'taskmanager/login.html', {'problem': False, 'form': LoginForm()})
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
                    response = HttpResponseRedirect(reverse('taskmanager:tasks'))
                    set_cookie(response, TOKEN, tokenObject.access_token)
                    return response
            except User.DoesNotExist:
                response = render(request, 'taskmanager/login.html', {'problem': True, 'form': LoginForm()})
    response.delete_cookie(TOKEN)
    return response


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
    res = HttpResponseRedirect(reverse('taskmanager:login'))
    res.delete_cookie(TOKEN)
    return res


@authentication
def addTask(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            deadline = form.cleaned_data['deadline']
            label = form.cleaned_data['label']
            newTask = Task(title=title, description=description, deadline=deadline, label=label)
            newTask.save(force_insert=True)
            user = getCurrentUser(request)
            UserTask.objects.create(user_name=user, task_id=newTask.pk)
            return render(request, 'taskmanager/addtask.html',
                          {'form': AddTaskForm(), 'error': '', 'message': 'Success', })
        return render(request, 'taskmanager/addtask.html',
                      {'form': AddTaskForm(), 'error': form.errors, 'message': ''})
    return render(request, 'taskmanager/addtask.html', {'form': AddTaskForm(), 'error': '', 'message': ''})


@authentication
def deleteTask(request, task_id):
    try:
        Task.objects.get(id=task_id).delete()
        return HttpResponseRedirect(reverse('taskmanager:tasks'))
    except Task.DoesNotExist:
        return render(request, 'taskmanager/task.html', {'task_id': task_id, })
