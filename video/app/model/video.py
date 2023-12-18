# coding:utf-8
# 视频文件
from enum import Enum  # 枚举
from django.db import models


# 视频国籍的枚举
class NationalityType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'


# 给标签
NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.korea.label = '韩国'
NationalityType.america.label = '美国'
NationalityType.other.label = '其他'


# 视频来源的枚举
class FromType(Enum):
    aQiYi = 'aQiYi'
    youku = 'youku'
    custom = 'custom'


FromType.aQiYi.label = '爱奇异'
FromType.youku.label = '优酷'
FromType.custom.label = '自制'


# 视频类型的枚举
class VideoType(Enum):
    movie = 'movie'
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'variety'
    other = 'other'


# 给标签
VideoType.movie.label = '电影'
VideoType.cartoon.label = '卡通'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.other.label = '其他'


# 身份证
class IdentityType(Enum):
    to_star = 'to_star'  # 主角
    supporting_rule = 'supporting_rule'  # 配角
    director = 'director'  # 导演


IdentityType.to_star.label = '主角'
IdentityType.supporting_rule.label = '配角'
IdentityType.director.label = '导演'


class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)  # 默认其他的值
    # 视频来源
    from_type = models.CharField(max_length=20, null=False, default=FromType.custom.value)  # 也定义一个枚举
    # 初频的国籍
    nationality_type = models.CharField(max_length=20, default=NationalityType.other.value)  # 也定义一个枚举#默认其他国家
    # 信息
    info = models.TextField()
    # 视频是否可用
    status = models.BooleanField(default=True, db_index=True)
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 更新的时间
    update_time = models.DateTimeField(auto_now=True)  # 每一次更新的时间

    # 做一个联合索引
    # 保证 name, 视频类型（video_type）,视频来源（from_to）， 国籍（nationality），不重复就可以了。
    class Meta:
        unique_together = ('name', 'video_type', 'from_type', 'nationality_type')

    def __str__(self):
        return self.name


# 不知道演员什么身份，加演员的附表。
class VideoStar(models.Model):
    # 做一下video的关联，外键
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    # 人名
    name = models.CharField(max_length=100, null=False)
    # 身份
    identity = models.CharField(max_length=50, default='')

    # 事实上我们都要保证唯一。唯一性。
    # 然后我们做一个Meta
    class Meta:
        # 视频，人名，身份。
        # 都要保证唯一。
        unique_together = ('video', 'name', 'identity')

    @property
    def ident(self):
        try:
            result = IdentityType(self.identity)
        except:
            return ''
        return result.label

    def __str__(self):
        return self.name


# 变形金刚可能有好几集，这些集数怎么区分开呢？→集数。
# 还有没有一个地方去存我们的播放地址。→播放地址
class VideoSub(models.Model):
    # 做一下video的关联，外键
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    # 地址
    url = models.CharField(max_length=500, null=False)
    # 集数
    number = models.IntegerField(default=1)  # 默认给他一集。 #很多电影只有一部

    # 事实上我们都要保证唯一。唯一性。
    # 然后我们做一个Meta
    class Meta:
        # 视频，集数。
        # 都要保证唯一。
        unique_together = ('video', 'number')

    def __str__(self):
        return "video:{}, number:{}".format(self.video.name, self.number)  # 给了一视频名称和集数
