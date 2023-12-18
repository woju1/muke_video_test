# coding:utf-8
# 国内编程

from django.urls import path
from .views.base import Index
from .views.auth import Login, AdminManger, Logout, UpdateAdminStatus
from .views.video import ExternalVideo, VideoSubView,VideoStarView,StarDelete, SubDelete, VideoUpdate, VideoUpdateStatus
from django.views.decorators.csrf import csrf_exempt  # 不执行csrf验证

urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('login/', csrf_exempt(Login.as_view()), name='dashboard_login'),
    path('admin/manger', csrf_exempt(AdminManger.as_view()), name='admin_manger'),
    path('logout', csrf_exempt(Logout.as_view()), name='logout'),
    path('admin/manger/update/status', csrf_exempt(UpdateAdminStatus.as_view()), name='admin_update_status'),
    path('video/external_link', csrf_exempt(ExternalVideo.as_view()), name='external_video'),
    path('video/video_sub/<int:video_id>', csrf_exempt(VideoSubView.as_view()), name='video_sub'),
    path('video/star', csrf_exempt(VideoStarView.as_view()), name='video_star'),
    path('video/star/delete/<int:star_id>/<int:video_id>',
         csrf_exempt(StarDelete.as_view()), name='star_delete'),
    path('video/sub/delete/<int:videosub_id>/<int:video_id>',
         csrf_exempt(SubDelete.as_view()), name='sub_delete'),
    path('video/update/<int:video_id>',
         csrf_exempt(VideoUpdate.as_view()), name='video_update'),
    path('video/update/status/<int:video_id>',
         csrf_exempt(VideoUpdateStatus.as_view()), name='video_update_status'),

]
