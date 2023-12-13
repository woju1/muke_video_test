# coding:utf-8
# 装饰器验证
import functools

from django.shortcuts import redirect, reverse


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
