import binascii
import datetime
import hashlib
import os

from django.http import HttpResponseRedirect
from django.urls import reverse

from taskmanager.models import Token, User

TOKEN = 'TOKEN_COOKIE'


def authentication(func):
    def wrapper(*args, **kw):
        request = args[0]
        token = request.COOKIES.get(TOKEN)
        try:
            Token.objects.get(access_token=token)
            return func(*args, **kw)
        except Token.DoesNotExist:
            print('Token nie istnieje')
            return HttpResponseRedirect(reverse('taskmanager:login'))

    return wrapper


def createToken():
    randomToken = binascii.hexlify(os.urandom(32))
    expirationDate = datetime.datetime.now() + datetime.timedelta(days=7)
    newToken = Token(access_token=randomToken, expiration_date=expirationDate)
    newToken.save()
    return newToken


def getCurrentUser(request):
    token = request.COOKIES.get(TOKEN)
    try:
        user = User.objects.get(token_token__access_token=token)
        return user
    except User.DoesNotExist:
        return None
def hashPassword(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()