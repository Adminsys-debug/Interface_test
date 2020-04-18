#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/28 14:55
# @Author  : Mr.chen
# @Site    : 
# @File    : test_http_request.py
# @Software: PyCharm
# @Email   : 794281961@qq.com
# 专门写http测试用例的类


import unittest

from ddt import ddt, data

from common.do_excel import DoExcel
from common.http_requests import HttpRequests
from common.my_log import MyLog
from conf.read_config import ReadConfig

# 读取test_data文件夹中excel的test_data数据
test_file_path = ReadConfig().read_path('/project.conf', 'PROJECTS', 'test_data_path')
test_data = DoExcel(test_file_path, 'test_data').read_data()

# 实例化日志类
logger = MyLog()

# 读取conf文件夹中的http配置参数,传三个入参,路径,key,value
uat_env = ReadConfig().read_path('/project.conf', 'HTTP', 'uat_env')
# 全局变量,初始值
COOKIES = None


# todo
@ddt
class TestHttpRequest(unittest.TestCase):
    name_module = 2
    platform = 1
    request_method = 4
    name_url = 5
    name_params = 6
    exception_code = 7

    def setUp(self):
        self.t = DoExcel(test_file_path, 'test_data')
        logger.debug('{}'.format('Start test.......'))

    @data(*test_data)
    def test_http_request(self, a):  # 登录
        logger.debug('Test_data :{0}'.format(a))
        logger.debug('目前正常执行第 {0} 条 用例:'.format(a[0]))
        global COOKIES
        '''
        if a[self.name_module] == 'uat_warning':  # 先判断是否rank还是warning模块的
            if a[self.platform] == 'PF10':  # 如果是warning模块、再判断平台 01、02、03
'''
        # IP+路径拼接
        res = HttpRequests(uat_env + a[self.name_url], eval(a[self.name_params])).http_request(
            a[self.request_method], cookie=COOKIES)
        if len(res.cookies) != 0:  # 判断长度为0或者判断字典{}是否为空
            COOKIES = res.cookies  # 只有登录后才会生成cookie
        logger.debug(res.json())
        try:
            result = 'PASS'
            self.assertIn(str(a[self.exception_code]), str(res.json()))
        except AssertionError as e:
            result = 'Fail'
            raise e
        finally:
            self.t.write_data(a[0] + 1, str(res.json()), result)

    def tearDown(self):
        logger.debug('{}'.format('End test.......'))


if __name__ == '__main__':
    unittest.main()
