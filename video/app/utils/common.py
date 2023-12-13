# coding:utf-8
# 公共函数。

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

