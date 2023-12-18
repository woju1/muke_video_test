# coding:utf-8
# 公共函数。
import os
import time
import shutil

from django.conf import settings
from app.libs.base_qiniu import video_qiniu
from app.models import VideoSub, Video
# from app.tasks.task import video_task 异步队列

def check_and_get_video_type(type_obj, type_value, message):
    '''
    检测类型是否合法。

    :param type_obj:  类型
    :param type_value: 字符串
    :param message: 错误信息
    :return:
    '''
    try:
        type_obj(type_value)  # 正确：VideoType('movie') 。 错误：VideoType('movies')
    except:
        # 失败
        return {'code': -1, 'msg': message}
    # 成功
    return {'code': 0, 'msg': 'success'}

# 判断是否存在，再删除。
def remove_path(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

def handle_video(video_file, video_id, number):
    # 输入的地址
    in_path = os.path.join(settings.BASE_DIR, 'app\\dashboard\\temp_in')
    out_path = os.path.join(settings.BASE_DIR, 'app\\dashboard\\temp_out')
    # print(video_file, video_id, number)
    # # 这样可以把对象的方法都拿出来。dir.
    # print(dir(video_file))
    # print(path)

    name = '{}-{}'.format(int(time.time()), video_file.name)
    # print('name:',name)
    # 总终地址
    path_name = '\\'.join([in_path, name])
    out_path_name = '\\'.join([out_path, name.split('.')[0]])

    # 文件临时地址
    # temp_path = video_file.temporary_file_path()
    # 文件复制粘贴
    # 把temp_path 传到 path_name下
    # shutil.copyfile(temp_path, path_name)
    # 直接将文件内容写入目标文件→源文件复制的输入的地址
    with open(path_name, 'wb') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)
    # 上面完成的复制的视频文件的作用。
    command = 'ffmpeg -i {} {}.mp4'.format(path_name, out_path_name) # 转码
    # print(path_name)
    # print(out_path_name)
    # os.system('dir')

    # 以下交给异步队列去做。
    os.system(command)
    out_name = '{}.mp4'.format(out_path_name)
    # 判断路径是否存在。
    if not os.path.exists(out_name):
        remove_path([path_name, out_name])
        return False
    # print('out_name:', out_name)
    url = video_qiniu.put(video_file.name, out_name)
    # print(url) #['http://s5t1cuxxz.hb-bkt.clouddn.com//小猪佩奇.mp4']
    if url:
        video = Video.objects.get(pk=video_id)
        # print('video:', video)
        # print('url:', url)
        # print('number:', number)
        #

        try:
            VideoSub.objects.create(
                video=video,
                url=url,
                number=number
            )
            return True
        except:
            return False
        finally:
            remove_path([path_name, out_name])
    remove_path([path_name, out_name])

    # 异步队列因为兼容原因。不能使用。需要3.6，我的环境是3.11.
    # video_task.delay(
    #     command, out_path_name, path_name, video_file.name, video_id, number)
    return False


