from django.conf.urls import url
from django.views.generic import RedirectView

from taskmanager import views

app_name = 'taskmanager'

urlpatterns = [
    url(r'^auth/tasks/$', RedirectView.as_view(url='tasks/')),
    url(r'^$', views.tasks, name='tasks'),
    url(r'task/(?P<task_id>[0-9]+)/$', views.task, name='task'),
    url(r'tasks/$', views.tasks, name='tasks'),
    url(r'user/(?P<user_name>[a-zA-Z]+)/$', views.user, name='user'),
    url(r'users/$', views.users, name='users'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'login$', views.login, name='login'),
]