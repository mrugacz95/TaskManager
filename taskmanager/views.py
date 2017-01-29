from django.db import IntegrityError, connection
from django.db import InternalError
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from taskmanager.auth import TOKEN, createToken, getCurrentUser, authentication, hashPassword, set_cookie, \
    adminAuthentication
from taskmanager.forms import LoginForm, TaskForm, RegisterForm, AddGroupForm
from taskmanager.models import User, Task, Token, UserTask, GroupNames, UserGroup, GroupTask, Role


@adminAuthentication
def users(request):
    user = getCurrentUser(request)
    role = Role.objects.get(user__name=user.name)
    roleName = role.role_name
    if roleName == 'admin':
        users = User.objects.all()
        return render(request, 'taskmanager/users.html', {'users': users})
    else:
        return HttpResponse(404)


@authentication
def task(request, task_id):
    user = getCurrentUser(request)
    try:
        task = get_object_or_404(Task.objects.filter(id=task_id))
        isOwnerByTask = Task.objects.filter(Q(id=task_id, usertask__user_name__name=user.name)).count() > 0
        try:
            group = GroupNames.objects.get(grouptask__task_id__id=task_id)
            isOwnerByGroup = User.objects.filter(name=user.name, usergroup__group_names_id=group.id).count() > 0
        except GroupNames.DoesNotExist:
            isOwnerByGroup = False
        return render(request, 'taskmanager/task.html', {'task': task, 'isowner': isOwnerByTask or isOwnerByGroup})
    except Task.DoesNotExist:
        return HttpResponse(status=404)


@authentication
def user(request, user_name):
    try:
        user = User.objects.get(name=user_name)
        query = 'SELECT task.title, task.id,task.deadline,task.label,task.description FROM task LEFT JOIN group_task on task.id = group_task.task_id LEFT JOIN group_names on group_task.group_id = group_names.id LEFT JOIN user_group on group_names.id = user_group.group_names_id left join user_task on user_task.task_id = task.id WHERE user_group.user_name = "' + user_name + '" or user_task.user_name = "' + user_name + '" order by task.done,task.deadline'
        tasksList = list(Task.objects.raw(raw_query=query))
        groupList = GroupNames.objects.filter(usergroup__user_name=user_name)
        return render(request, 'taskmanager/user.html',
                      {'tasks': tasksList, 'user': user, 'groups': groupList, 'error': False})
    except Task.DoesNotExist:
        return render(request, 'taskmanager/user.html', {'error': True})


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
                    print(formUser.name)
                    response = HttpResponseRedirect(reverse('taskmanager:user', kwargs={'user_name': formUser.name}))
                    set_cookie(response, TOKEN, tokenObject.access_token)
                    return response
                else:
                    problem = 'Wrong password or login'
            except User.DoesNotExist:
                problem = 'Wrong login or password'
    response = render(request, 'taskmanager/login.html',
                      {'problem': problem, 'loginForm': LoginForm()})
    response.delete_cookie(TOKEN)
    return response


def logout(request):
    res = HttpResponseRedirect(reverse('taskmanager:login'))
    res.delete_cookie(TOKEN)
    return res


@authentication
def addTask(request):
    message = error = None
    if request.method == 'POST':
        form = TaskForm(request.POST)
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
        error = form.errors
    return render(request, 'taskmanager/addtask.html', {'form': TaskForm(), 'error': error, 'message': message})


@authentication
def deleteTask(request, task_id):
    user = getCurrentUser(request)
    try:
        Task.objects.get(id=task_id).delete()
        return HttpResponseRedirect(reverse('taskmanager:user', kwargs={'user_name': user.name}))
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
                newUser = User(name=userName, password=hashPassword(password), email=email, role_role_name_id='user',
                               token_token_id=token.pk)
                try:
                    newUser.save(force_insert=True)
                except IntegrityError:
                    problem = 'User with this login already exists'
                except InternalError:
                    problem = 'Login cant use polish diacritic signs'
            else:
                problem = 'Passwords are not equal'
        else:
            problem = form.errors
    return render(request, 'taskmanager/register.html', {'registerForm': RegisterForm(), 'problem': problem})


@authentication
def group(request, group_id):
    groupObj = GroupNames.objects.get(id=group_id)
    groupUsers = User.objects.filter(usergroup__group_names_id=group_id)
    user = getCurrentUser(request)
    isMember = GroupNames.objects.filter(usergroup__user_name=user.name, id=group_id).count() > 0
    tasksList = Task.objects.filter(grouptask__group_id=group_id).order_by('done', 'deadline')
    return render(request, 'taskmanager/group.html',
                  {'group': groupObj, 'users': groupUsers, 'tasks': tasksList, 'isMember': isMember})


@authentication
def addgroup(request):
    user = getCurrentUser(request)
    problem = None
    message = None
    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            groupName = form.cleaned_data['name']
            group = GroupNames(name=groupName)
            group.save()
            UserGroup.objects.create(group_names_id=group.pk, user_name=user)
            message = "Success"
            return HttpResponseRedirect(reverse('taskmanager:user', kwargs={'user_name': user.name}))
        else:
            problem = form.errors
    return render(request, 'taskmanager/addgroup.html', {'form': AddGroupForm(), 'problem': problem})


@authentication
def addMeToGroup(request, group_id):
    user = getCurrentUser(request)
    newUserGroup = UserGroup(user_name_id=user.name, group_names_id=group_id)
    newUserGroup.save()
    return HttpResponseRedirect(reverse('taskmanager:group', kwargs={'group_id': group_id}))


@authentication
def addTaskToGroup(request, group_id):
    message = error = None
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            deadline = form.cleaned_data['deadline']
            label = form.cleaned_data['label']
            newTask = Task(title=title, description=description, deadline=deadline, label=label)
            newTask.save(force_insert=True)
            newGroupTask = GroupTask(group_id_id=group_id, task_id_id=newTask.pk)
            newGroupTask.save()
            message = 'Success'
            return HttpResponseRedirect(reverse('taskmanager:group', kwargs={'group_id': group_id}))
        error = form.errors
    return render(request, 'taskmanager/addtask.html', {'form': TaskForm(), 'error': error, 'message': message})


@authentication
def main(request):
    user = getCurrentUser(request)
    return HttpResponseRedirect(reverse('taskmanager:user', kwargs={'user_name': user.name}))


@authentication
def done(request, task_id):
    taskObj = Task.objects.get(id=task_id)
    taskObj.done = True
    taskObj.save()
    return HttpResponseRedirect(reverse('taskmanager:main'))


@authentication
def search(request):
    users = None
    groups = None
    tasks = None
    query = None
    if request.method == 'GET':
        query = request.GET['query']
        searchQuery = '\S*' + query + '\S*'
        users = User.objects.filter(name__regex=searchQuery)
        tasks = Task.objects.filter(Q(title__regex=searchQuery) | Q(label__regex=searchQuery))
        groups = GroupNames.objects.filter(name__regex=searchQuery)
    return render(request, 'taskmanager/search.html',
                  {'tasks': tasks, 'users': users, 'groups': groups, 'query': query})


@authentication
def withdrawFromGroup(request, group_id):
    user = getCurrentUser(request)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM user_group where user_name = "%s" and group_names_id = "%s"' % (user.name, group_id))
    return HttpResponseRedirect(reverse('taskmanager:main'))


@authentication
def editTask(request, task_id):
    message = None
    error = None
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            deadline = form.cleaned_data['deadline']
            label = form.cleaned_data['label']
            task.label = label
            task.deadline = deadline
            task.title = title
            task.description = description
            task.save()
            return HttpResponseRedirect(reverse('taskmanager:main'))
        else:
            error = "Form is not valid"
    data = {'title': task.title, 'description': task.description, 'deadline': task.deadline, 'label': task.label}
    form = TaskForm(initial=data)
    return render(request, 'taskmanager/edittask.html', {'form': form, 'error': error, 'message': message})


@adminAuthentication
def makeAdmin(request, user_name):
    user = User.objects.get(name=user_name)
    role = Role.objects.get(role_name='admin')
    user.role_role_name = role
    user.save()
    return HttpResponseRedirect(reverse('taskmanager:users'))


@adminAuthentication
def deleteUser(request, user_name):
    user = User.objects.get(name=user_name)
    user.delete()
    return HttpResponseRedirect(reverse('taskmanager:users'))


def deleteTokens(request):
    cursor = connection.cursor()
    cursor.execute("CALL deleteOldTokens();")
    return HttpResponseRedirect(reverse('taskmanager:users'))
