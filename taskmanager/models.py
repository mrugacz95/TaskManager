# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class GroupNames(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'group_names'


class Role(models.Model):
    role_name = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'role'


class Task(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    deadline = models.DateTimeField(blank=True, null=True)
    label = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'


class Token(models.Model):
    access_token = models.CharField(max_length=32, blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    token_id = models.AutoField(db_column='token_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'token'


class User(models.Model):
    name = models.CharField(primary_key=True, max_length=32)
    password = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=32, blank=True, null=True)
    role_role_name = models.ForeignKey(Role, models.DO_NOTHING, db_column='role_role_name')
    token_token = models.ForeignKey(Token, models.DO_NOTHING, db_column='token_token_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'


class UserGroup(models.Model):
    user_name = models.ForeignKey(User, models.DO_NOTHING, db_column='user_name')
    group_names = models.ForeignKey(GroupNames, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_group'
        unique_together = (('user_name', 'group_names'),)

class GroupTask(models.Model):
    group_id = models.ForeignKey(GroupNames, models.DO_NOTHING, db_column='group_id')
    task_id = models.ForeignKey(Task, db_column='task_id', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'group_task'
        unique_together = (('group_id', 'task_id'),)


class UserTask(models.Model):
    user_name = models.ForeignKey(User, models.DO_NOTHING, db_column='user_name')
    task = models.ForeignKey(Task, db_column='task_id', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'user_task'
        unique_together = (('user_name', 'task'),)
