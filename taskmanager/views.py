import datetime

from django.conf import settings
from django.db import DatabaseError
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from taskmanager.auth import TOKEN, createToken, getCurrentUser, authentication, hashPassword
from taskmanager.forms import LoginForm, AddTaskForm, RegisterForm
from taskmanager.models import User, Task, Token, UserTask, GroupNames


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
        tasksList = Task.objects.filter(Q(usertask__user_name=user.name)).order_by('deadline')
        #groupName = GroupNames.objects.filter(usergroup__user_name=user.name).first()
        #print(groupName.name)
        #tasksList = Task.objects.filter(grouptask__group__usergroup=groupName.name)
        query = 'SELECT task.title, task.id,task.deadline,task.label,task.description FROM task LEFT JOIN group_task on task.id = group_task.task_id LEFT JOIN group_names on group_task.group_id = group_names.id LEFT JOIN user_group on group_names.id = user_group.group_names_id left join user_task on user_task.task_id = task.id WHERE user_group.user_name = "'+user.name+'" or user_task.user_name = "'+user.name+'"'
        tasksList = list(Task.objects.raw(raw_query=query))
        groupList = GroupNames.objects.filter(usergroup__user_name=user.name)
        return render(request, 'taskmanager/tasks.html', {'tasks': tasksList, 'user': user, 'groups':groupList, 'error': False})
    except Task.DoesNotExist:
        return render(request, 'taskmanager/tasks.html', {'error': True})


def login(request):
    problem = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            formLogin = form.cleaned_data['login']
            formPassword = form.cleaned_data['password']
            try:
                formUser = User.objects.get(pk=formLogin)
                hashedPassword = hashPassword(formPassword)
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
                else:
                    problem = 'Wrong password or login'
            except User.DoesNotExist:
                problem = 'Wrong login or password'
    response = render(request, 'taskmanager/login.html',
                      {'problem': problem, 'loginForm': LoginForm(), 'registerForm': RegisterForm()})
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
    message = error = None
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
            message = 'Success'
        error= form.errors
    return render(request, 'taskmanager/addtask.html', {'form': AddTaskForm(), 'error': error, 'message': message})


@authentication
def deleteTask(request, task_id):
    try:
        Task.objects.get(id=task_id).delete()
        return HttpResponseRedirect(reverse('taskmanager:tasks'))
    except Task.DoesNotExist:
        return render(request, 'taskmanager/task.html', {'task_id': task_id, })


def register(request):
    problem = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['login']
            password = form.cleaned_data['password']
            repass = form.cleaned_data['repeatPassword']
            email = form.cleaned_data['email']
            if password == repass:
                token = createToken()
                newUser = User(name=userName, password=hashPassword(password), email=email, role_role_name_id='user', token_token_id=token.pk)
                try:
                    newUser.save(force_insert=True)
                except IntegrityError:
                    problem = 'User with this login already exists'
            else:
                problem = 'Passwords are not equal'
        else:
            problem = form.errors
    return render(request, 'taskmanager/register.html', {'registerForm': RegisterForm(), 'problem': problem})

@authentication
def group(request, group_id):
    GroupNames.objects.filter(id=group_id)
    return render(request, 'taskmanager/group.html', {'group':group})