# encoding: utf-8
'''
@author: tim.chen
@contact: a794281961@126.com
@site: https://www.cnblogs.com/mrchenyushen/
@software: PyCharm
@file: lib_den.py
@time: 2019/12/5 10:51 上午
'''
import datetime
import time

import pytz

'''

new_time = datetime.datetime.now()
print(type(new_time), 'sss')
t = new_time.strftime('%H:%M:%S')
print(type(t))
old_time = datetime.datetime(2019, 12, 20, 9, 0, 0)
mid_time = (new_time - old_time).min
print(mid_time, 'mid_ssssss')
'''

DAY_FORMAT_STR = '%Y-%m-%d'
SECOND_FORMAT_STR = '%Y-%m-%d %X'

lang_zone = "Asia/Shanghai"
time_zone = pytz.timezone(lang_zone)

utc_time_zone = pytz.timezone("UTC")


def str2timestamp_of_time_zone(date, format=SECOND_FORMAT_STR, zone=None):
    """
    按照时区字符串形式日期转换为时间戳 ，默认格式"%Y-%m-%d"
    转换出错默认返回 0
    """
    if not zone:
        tz = time_zone
    else:
        tz = pytz.timezone(zone)
    try:
        timeArray = time.strptime(date, format)
        if tz:
            y, m, d, H, M, S = timeArray[0:6]
            dt = datetime.datetime(y, m, d, H, M, S)
            t = tz.localize(dt)
            t = t.astimezone(pytz.utc)
            return int(time.mktime(t.utctimetuple())) - time.timezone
        return int(time.mktime(timeArray))
    except Exception as e:
        return 0


if __name__ == '__main__':
    print(str2timestamp_of_time_zone('2019-12-20 11:37:20'))
