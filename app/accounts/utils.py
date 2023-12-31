from django.contrib.auth import login, logout, user_logged_in, user_logged_out
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from djoser.conf import settings

def login_user(request, user):
    token, _ = settings.TOKEN_MODEL.objects.get_or_create(user=user)
    if settings.CREATE_SESSION_ON_LOGIN:
        login(request, user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def logout_user(request):
    if settings.TOKEN_MODEL:
        settings.TOKEN_MODEL.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
    if settings.CREATE_SESSION_ON_LOGIN:
        logout(request)