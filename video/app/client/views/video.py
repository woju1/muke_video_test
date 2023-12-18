# coding:utf-8
from django.views.generic import View
from app.libs.base_render import render_to_response

from app.models import Video, Comment
from app.model.video import FromType
from app.utils.permission import client_auth #获取user
# 重定向
from django.shortcuts import redirect, reverse, get_object_or_404


class ExVideo(View):
    TEMPLATE = 'client/videos/video.html'

    def get(self, request):
        # 除自制的视频
        videos = Video.objects.exclude(from_type=FromType.custom.value)
        data = {'videos': videos}
        return render_to_response(request, self.TEMPLATE, data=data)


class CusVideo(View):
    TEMPLATE = 'client/videos/video.html'

    def get(self, request):
        # 除自制的视频
        videos = Video.objects.filter(from_type=FromType.custom.value)
        data = {'videos': videos}
        return render_to_response(request, self.TEMPLATE, data=data)


class VideoSub(View):
    TEMPLATE = 'client/videos/video_sub.html'

    def get(self, request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        user =client_auth(request)
        comments = Comment.objects.filter(video=video, status=True)
        data = {'video': video, 'user':user, 'comments':comments}
        print(data)
        return render_to_response(request, self.TEMPLATE, data=data)
