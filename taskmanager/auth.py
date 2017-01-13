import datetime

import binascii
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render

from taskmanager.models import Token, User

TOKEN = 'TOKEN_COOKIE'


def authentication(func):
    def wrapper(*args, **kw):
        request = args[0]
        token = request.COOKIES.get(TOKEN)
        try:
            tokenObject = Token.objects.get(access_token=token)
            print('authoricated with ' + tokenObject.access_token)
            return func(*args, **kw)
        except Token.DoesNotExist:
            return render(request, 'taskmanager/login.html', {'problem': True})

    return wrapper


def createToken():
    randomToken = binascii.hexlify(os.urandom(32))
    expirationDate = datetime.datetime.now() + datetime.timedelta(days=7)
    newToken = Token.objects.create(access_token=randomToken, expiration_date=expirationDate)
    return newToken


def getCurrentUser(request):
    token = request.COOKIES.get(TOKEN)
    users = User.objects.all()
    try:
        user = users.get(token_token__access_token=token)
        return user
    except User.DoesNotExist:
        return None
