# coding:utf-8

from django.views.generic import View
from django.shortcuts import reverse
from django.http import JsonResponse  # ajax要用的。
from app.models import Comment, ClientUser, Video


class CommentView(View):
    def post(self, request):
        content = request.POST.get('content', '')
        user_id = request.POST.get('userId', '')
        video_id = request.POST.get('videoId', '')

        if not all([content, user_id, video_id]):
            error = '缺少必要字段'
            return JsonResponse({'code': -1, 'msg': error})

        print((content, user_id, video_id))
        video = Video.objects.get(pk=video_id)
        user = ClientUser.objects.get(pk=user_id)
        comment = Comment.objects.create(content=content, video=video, user=user)
        data = {'comment': comment.data()}
        print(data)
        return JsonResponse({'code': 0, 'msg': 'success', 'data': data})
