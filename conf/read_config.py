#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 21:24
# @Author  : Mr.chen
# @Site    :
# @File    : read_config.py
# @Software: PyCharm
# @Email   : 794281961@qq.com


import configparser, os
from random import random


class ReadConfig:
    def read_config(self, file_path, section, option):
        cf = configparser.ConfigParser()
        cf.read(file_path, encoding='UTF-8')
        value = cf.get(section, option)
        return value

    def read_path(self, file_name, section, option):
        project_path = (os.path.split(__file__)[0] + file_name)
        _path = self.read_config(project_path, section, option)
        return _path


if __name__ == '__main__':
    # IP = ReadConfig().read_config('../conf/http.conf', 'HTTP', 'ip')
    # 获取文件路径('文件名',kye,value)
    _path = ReadConfig().read_path('/project.conf', 'PROJECTS', 'test_data_path')
    print(_path, '2221231231')
