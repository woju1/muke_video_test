# coding:utf-8
import os
from celery import task

from app.libs.base_qiniu import video_qiniu
from app.models import VideoSub, Video

@task
def video_task(command, out_path_name, path_name, video_file_name, video_id, number):
    from app.utils.common import remove_path
    print('---------------')
    print(command, out_path_name, path_name, video_file_name, video_id, number)

    os.system(command)
    out_name = '{}.mp4'.format(out_path_name)

    if not os.path.exists(out_name):
        remove_path([path_name, out_name])
        return False

    url = video_qiniu.put(video_file_name, out_name)

    if url:
        video = Video.objects.get(pk=video_id)

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
