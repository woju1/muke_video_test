# coding:utf-8
# 放数据库文件 → 客户端
import hashlib #自定义加密。

from django.db import models
from django.contrib.auth.hashers import make_password  # 密码加密。


# 加密函数→把密码加密。
def hash_password(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    result = hashlib.md5(password).hexdigest().upper()
    return result


class ClientUser(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=255, null=False, unique=True)
    # 头像
    avatar = models.CharField(max_length=500, default='')
    # 性别
    gender = models.CharField(max_length=10, default='')

    #
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True) # 第一次的时间

    def __str__(self):
        return 'username:{}'.format(self.username)

    @classmethod
    def add(cls, username, password, avatar='', gender='', birthday=None):
        return cls.objects.create(
            username=username,
            password=hash_password(password),
            avatar=avatar,
            gender=gender,
            birthday=birthday,
            status=True
        )

    @classmethod
    def get_user(cls, username, password):
        try:
            user = cls.objects.get(
                username=username,
                password=hash_password(password)
            )  # 没get到数据会异常。所以用try
            return user
        except Exception as e:
            return None

    #更新密码
    def update_password(self, old_password, new_password):
        hash_old_password = hash_password(old_password)

        # 如果密码不与老密码不同
        if hash_old_password != self.password:
            return False
        #否则
        hash_new_password = hash_password(new_password) #获取新密码
        #替换
        self.password = hash_new_password
        self.save() #保存
        return True

    #更新状态
    def update_status(self):
        self.status = not self.status#取反
        self.save()
        return True
