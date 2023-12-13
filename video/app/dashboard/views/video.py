# coding:utf-8

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


# 第三方外链
class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):
        # 下面def post中使用了error字段。所以这里要定义。
        error = request.GET.get('error', '')
        data = {'error': error}

        # 从后端传到前端。 ##2.
        # 拿video，自制的信息不要。其他的视频都要。
        videos = Video.objects.exclude(from_type=FromType.custom.value)
        # 拿到之后存入data中。
        data['videos'] = videos
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

        # 拿到这些东西，有些东西需要验证。
        # (name, image, video_type, from_type, nationality_type)中只要有一个不存在。
        if not all([name, image, video_type, from_type, nationality_type, info]):
            print('error')
            # 这里加上了error,所以def get中就要去取一下error了。
            return redirect('{}?error={}'.format(reverse('external_video'), '缺少必要字段'))
        # print(name, image, video_type, from_type, nationality_type)

        # 验证---------------------------------------------------------------------------------
        result = check_and_get_video_type(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))
        # 如果往下走，就相当于成功了。获取到数据对象。
        # video_type_obj = result.get('data')

        result = check_and_get_video_type(FromType, from_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))
        # 如果往下走，就相当于成功了。获取到数据对象。
        # from_type_obj = result.get('data')

        result = check_and_get_video_type(NationalityType, nationality_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result['msg']))
        # 如果往下走，就相当于成功了。获取到数据对象。
        # nationality_type_obj = result.get('data')
        # 验证通过 --------------------------------------------------------------------------------
        # 创建
        Video.objects.create(
            name=name,
            image=image,
            video_type=video_type,
            from_type=from_type,
            nationality_type=nationality_type,
            info=info
        )
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
        url = request.POST.get('url')
        # print(url,video_id)
        video = Video.objects.get(pk=video_id)

        # 拿集数
        length = video.video_sub.count()
        # 因为计算机中，0集就是第一集。

        VideoSub.objects.create(
            video=video,
            url=url,
            number=length + 1
        )
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
