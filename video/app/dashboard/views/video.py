# coding:utf-8
from django.db import IntegrityError
from django.views.generic import View
from django.shortcuts import redirect, reverse

from app.libs.base_render import render_to_response  # mako的render
from app.utils.permission import dashboard_auth  # 装饰器验证
from app.model.video import (VideoType, FromType,
                             NationalityType,
                             IdentityType,
                             Video,
                             VideoSub,
                             VideoStar)
from app.utils.common import check_and_get_video_type  # 校验合法。
from app.utils.common import handle_video  # 处理上传的视频


# 第三方外链
class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):
        # 下面def post中使用了error字段。所以这里要定义。
        error = request.GET.get('error', '')
        data = {'error': error}

        # 从后端传到前端。 ##2.
        cus_videos = Video.objects.filter(from_type=FromType.custom.value)
        # 拿video，自制的信息不要。其他的视频都要。
        ex_videos = Video.objects.exclude(from_type=FromType.custom.value)
        # 拿到之后存入data中。
        data['ex_videos'] = ex_videos
        data['cus_videos'] = cus_videos

        # 然后回到html.(前端。external_video.html) 难道是通过get传入前端。

        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        # post中就是form表单中，提交后，每个标签中的name属性。
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_type = request.POST.get('from_type')
        nationality_type = request.POST.get('nationality_type')
        info = request.POST.get('info')
        video_id = request.POST.get('video_id')

        if video_id:
            reverse_path = reverse('video_update', kwargs={'video_id':video_id})
        else:
            reverse_path = reverse('external_video')


        # 拿到这些东西，有些东西需要验证。
        # (name, image, video_type, from_type, nationality_type)中只要有一个不存在。
        if not all([name, image, video_type, from_type, nationality_type, info]):
            # print('error')
            # 这里加上了error,所以def get中就要去取一下error了。
            return redirect('{}?error={}'.format(reverse_path, '缺少必要字段'))
        # print(name, image, video_type, from_type, nationality_type)

        # 验证---------------------------------------------------------------------------------
        result = check_and_get_video_type(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result['msg']))
        # 如果往下走，就相当于成功了。获取到数据对象。
        # video_type_obj = result.get('data')

        result = check_and_get_video_type(FromType, from_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result['msg']))
        # 如果往下走，就相当于成功了。获取到数据对象。
        # from_type_obj = result.get('data')

        result = check_and_get_video_type(NationalityType, nationality_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse_path, result['msg']))
        # 如果往下走，就相当于成功了。获取到数据对象。
        # nationality_type_obj = result.get('data')
        # 验证通过 --------------------------------------------------------------------------------

        if not video_id:
            try:
                # 创建
                Video.objects.create(
                    name=name,
                    image=image,
                    video_type=video_type,
                    from_type=from_type,
                    nationality_type=nationality_type,
                    info=info
                )
            except:
                return redirect('{}?error={}'.format(reverse_path, '创建失败'))
        else:
            try:
                video = Video.objects.get(pk=video_id)
                video.name = name
                video.image = image
                video.video_type = video_type
                video.from_type = from_type
                video.nationality_type = nationality_type
                video.info = info
                video.save()
            except:
                return redirect('{}?error={}'.format(reverse_path, '修改失败'))
        # 这里成功存到数据库了。，然后就从后端传到前端。去get. #####1.

        return redirect(reverse('external_video'))


# 编辑 和 附属信息。
# 第三方外链
class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        error = request.GET.get('error', '')

        data['video'] = video
        data['error'] = error
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, video_id):
        # url = request.POST.get('url')
        number = request.POST.get('number')
        videosub_id = request.POST.get('videosub_id')  # 创建、更新
        video = Video.objects.get(pk=video_id)
        if FromType(video.from_type) == FromType.custom:
            url = request.FILES.get('url')
        else:
            url = request.POST.get('url')

        url_format = reverse('video_sub', kwargs={'video_id': video_id})
        if not all([url, number]):
            return redirect('{}?error={}'.format(url_format, '缺少必要字段'))
        # print(url,video_id)
        if FromType(video.from_type) == FromType.custom:
            handle_video(url, video_id, number)
            return redirect(reverse('video_sub', kwargs={'video_id': video_id}))



        if not videosub_id:
            # 拿集数
            # 因为计算机中，0集就是第一集。
            try:
                VideoSub.objects.create(video=video, url=url, number=number)
            # except IntegrityError as e:
            #     # 处理数据库完整性错误
            #     error_message = '集数已存在，请选择一个不同的集数。'
            #     return redirect('{}?error={}'.format(url_format, error_message))
            except:
                return redirect('{}?error={}'.format(url_format, '创建失败'))
        else:
            try:
                # 更新
                video_sub = VideoSub.objects.get(pk=videosub_id)
                video_sub.url = url
                video_sub.number = number
                video_sub.save()
            except:
                return redirect('{}?error={}'.format(url_format, '修改失败'))

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoStarView(View):
    # def get 实际上走的是VideoSubView
    # 纯post提交
    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        path_format = "{}".format(redirect(reverse('video_sub', kwargs={'video_id': video_id})))

        # 判断
        if not all([name, identity, video_id]):
            # 这里加上了error,所以def get中就要去取一下error了。
            return redirect('{}?error={}'.format(path_format, '缺少必要字段'))

        # 身份验证
        result = check_and_get_video_type(IdentityType, identity, '非法的身份')
        # 如果不为0就是违法的。
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(path_format, result['msg']))

        # 这里就拿video对象了，然后创建了。
        video = Video.objects.get(pk=video_id)

        # 用VideoStar来创建。
        try:
            # 如果有相同的是不能创建成功的。
            VideoStar.objects.create(
                video=video,
                name=name,
                identity=identity
            )
        except:
            return redirect('{}?error={}'.format(path_format, '创建失败'))

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


# 点击删除演员的视图。
class StarDelete(View):
    # 还是用post, 我们提交这个star_id
    def get(self, request, star_id, video_id):
        # 我们去拿一下这个演员对象,然后使用delete()删除。
        VideoStar.objects.filter(id=star_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


# 功能删除。视频
class SubDelete(View):
    def get(self, request, videosub_id, video_id):
        VideoSub.objects.filter(id=videosub_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoUpdate(View):
    TEMPLATE = 'dashboard/video/video_update.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        data['video'] = video
        return render_to_response(request, self.TEMPLATE, data=data)


# 修改状态
class VideoUpdateStatus(View):
    def get(self,request,video_id):
        video = Video.objects.get(pk=video_id)
        video.status = not video.status
        video.save()
        return redirect(reverse('external_video'))


