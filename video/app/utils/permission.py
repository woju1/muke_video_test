# coding:utf-8
# 装饰器验证
import functools

from django.shortcuts import redirect, reverse
from .consts import COOKIE_NAME
from app.models import ClientUser

def dashboard_auth(func):
    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user  # 拿到用户
        # 是否登录，是否为超级管理员
        if not user.is_authenticated or not user.is_superuser:
            path = request.path
            return redirect('{}?to={}'.format(reverse('dashboard_login'), path))  # 登录后，回到指定地址
        return func(self, request, *args, **kwargs)

    return wrapper


def client_auth(request):
    value = request.COOKIES.get(COOKIE_NAME)

    if not value:
        return None

    user = ClientUser.objects.filter(pk=value)

    if user:
        # 如果user存在。
        return user[0]
    else:
        return None
