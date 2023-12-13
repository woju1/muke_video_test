# coding:utf-8
from django.views.decorators.http import require_POST
from django.views.generic import View

from django.shortcuts import redirect, reverse
# reverse跳转的是urls.py中定义的name
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # 分页
from django.contrib.auth import login, logout, authenticate  # 登录验证

from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth  # 装饰器验证


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        # 如果用户登录状态。就跳转页面。
        if request.user.is_authenticated:  # 是login,和logout关联的。
            return redirect(reverse('dashboard_index'))

        to = request.GET.get('to', '')

        data = {'error': '', 'to': to}
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to', '')

        data = {'error': ''}
        exists = User.objects.filter(username=username).exists()
        data['error'] = '没有该用户'
        if not exists:
            return render_to_response(request, self.TEMPLATE, data=data)
        # 如果用户存在了，就验证user
        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data['error'] = '你无权登录'
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request, user)  # 完成登录。 #is_authenticated 是和判断关联的。

        if to:
            return redirect(to)

        return redirect(reverse('dashboard_index'))


class Logout(View):
    def get(self, request):
        logout(request)  # 退出登录。
        return redirect(reverse('dashboard_login'))  # 然后在重新登录。


class AdminManger(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        # 拿超级管理员
        # users = User.objects.filter(is_superuser=True) #只拿管理员
        users = User.objects.all()  # 拿全部用户
        page = request.GET.get('page', 1)  # 第一页
        p = Paginator(users, 2)  # 每页分2个
        total_page = p.num_pages  # 页数
        if int(page) <= 1:  # 如果小于第一页， 就默认设置为第一页
            page = 1
        current_page = p.get_page(int(page)).object_list  #

        data = {'users': current_page, 'total': total_page, 'page_num': int(page)}
        return render_to_response(request, self.TEMPLATE, data=data)


class UpdateAdminStatus(View):

    def get(self, request):
        status = request.GET.get('status', '')
        username = request.GET.get('username', '') # 获取需要修改的用户名
        page_ys = request.GET.get('page_ys', '') # 获取需要修改的当前的页数

        user_to_update = User.objects.get(username=username) # 利用用户名，来用User获取用户对象。
        print("要需要的用户：", user_to_update)
        print("前：", user_to_update.is_superuser)
        _status = True if status == 'on' else False  # 如果status为on就为True，否则就为False
        user_to_update.is_superuser = _status  # 将状态赋值给is_superuser
        print("后：", user_to_update.is_superuser)
        user_to_update.save() # 保存要需要用户的对象。
        print("保存成功。")

        # 弄完跳转为管理员界面。
        return redirect(reverse('admin_manger')+f'?page={page_ys}') # 顺便跳转页数。

