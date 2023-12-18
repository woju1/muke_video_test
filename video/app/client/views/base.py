# coding:utf-8

from django.views.generic import View
from app.libs.base_render import render_to_response

# 重定向
from django.shortcuts import redirect, reverse


class Index(View):
    TEMPLATE = 'client/base.html'
    # TEMPLATE = ''

    def get(self, request):
        # return render_to_response(request, self.TEMPLATE)
        return redirect(reverse('client_ex_video'))