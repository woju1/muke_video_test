#coding:utf-8
#国内编程

from django.urls import path
from .views.base import Index
from .views.video import ExVideo, VideoSub, CusVideo
from .views.auth import User,Regist, Logout
from .views.comment import CommentView
from django.views.decorators.csrf import csrf_exempt  # 不执行csrf验证
urlpatterns = [
    path('', Index.as_view(), name='client_index'),
    path('video/ex', csrf_exempt(ExVideo.as_view()), name='client_ex_video'),
    path('video/custom', csrf_exempt(CusVideo.as_view()), name='client_cus_video'),
    path('video/<int:video_id>', csrf_exempt(VideoSub.as_view()), name='client_video_sub'),
    path('auth', csrf_exempt(User.as_view()), name='client_auth'),
    path('auth/regist', csrf_exempt(Regist.as_view()), name='client_regist'),
    path('auth/logout', csrf_exempt(Logout.as_view()), name='client_logout'),
    path('comment/add', csrf_exempt(CommentView.as_view()), name='client_add_comment'),

]