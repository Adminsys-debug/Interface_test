#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 21:05
# @Author  : Mr.chen
# @Site    : 
# @File    : http_requests.py
# @Software: PyCharm
# @Email   : 794281961@qq.com
# 完成http请求
import requests
from common.my_log import MyLog

logger = MyLog()


class HttpRequests:
    # cookies = ""

    def __init__(self, url, param):
        self.url = url
        self.param = param

    def http_request(self, method, cookie=None, type=None):
        global cookies
        if method.upper() == 'GET':
            res = requests.get(self.url, self.param, cookies=cookie)
        elif method.upper() == 'POST':
            res = requests.post(self.url, self.param, cookies=cookie)
        else:
            logger.debug('Requests is Error.......^__^')
        return res


if __name__ == '__main__':
    # 登录成功
    login_request = HttpRequests('url', 'param').http_request('Get')
    cookie = login_request.cookies()
    login_request_ = HttpRequests('url', 'param').http_request('Post', cookie)
