from django.conf.urls import url
from django.views.generic import RedirectView

from taskmanager import views
from taskmanager.forms import LoginForm

app_name = 'taskmanager'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.task, name='task'),
    url(r'^user/(?P<user_name>[a-zA-Z]+)/$', views.user, name='user'),
    url(r'^users/$', views.users, name='users'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^addtask', views.addTask, name='addtask'),
    url(r'^deletetask/(?P<task_id>[0-9]+)/$', views.deleteTask, name='deletetask'),
    url(r'^register', views.register, name='register'),
    url(r'^group/(?P<group_id>[0-9]+)/$', views.group, name='group'),
    url(r'^addgroup/$', views.addgroup, name='addgroup'),

]