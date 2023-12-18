# coding:utf-8
import datetime #过期时间
# 时间：_time = datetime.datetime.now() + datetime.timedelta(days=4) 就是时间持续4天。
#  response.set_cookie(COOKIE_NAME, str(user.id), _time)

from django.views.generic import View
# 重定向
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from app.libs.base_render import render_to_response
from app.utils.permission import client_auth
from app.utils.consts import COOKIE_NAME

from app.models import ClientUser


class User(View):
    TEMPLATE = 'client/auth/user.html'

    def get(self, request):
        user = client_auth(request)
        data = {'user':user}
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not all([username, password]):
            error = '缺少必要字段'
            # -1就相当于失败了。
            # error错误信息。
            return JsonResponse({'code':-1, 'msg':error})

        #看看能不能拿到
        user = ClientUser.get_user(username, password)
        if not user:
            error = '用户名或密码错误，未找到该用户'
            return JsonResponse({'code': -1, 'msg': error})

        response = render_to_response(request, self.TEMPLATE)
        #时间就不给了 ，让他持久化的登录。
        response.set_cookie(COOKIE_NAME, str(user.id))
        return response




class Regist(View):
    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not all([username, password]):
            error = '缺少必要字段'
            # -1就相当于失败了。
            # error错误信息。
            return JsonResponse({'code':-1, 'msg':error})

        # 判断是否存在。
        exists = ClientUser.objects.filter(username=username).exists()

        if exists:
            error = '该用户名存在！'
            return JsonResponse({'code':-1, 'msg':error})

        #
        ClientUser.add(username=username, password=password)
        return JsonResponse({'code': 0, 'msg': '注册成功，请您登录'})


class Logout(View):
    TEMPLATE = 'client/auth/user.html'
    def get(self, request):
        response = render_to_response(request, self.TEMPLATE)
        # 为空字符串， 就拿不到了。
        response.set_cookie(COOKIE_NAME, '')
        return response


