#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 16:06
# @Author  : Mr.chen
# @Site    : 
# @File    : my_log.py
# @Software: PyCharm
# @Email   : 794281961@qq.com


from conf.read_config import ReadConfig
import logging, tushare

# 读取project配置文件中log文件路径
_path = ReadConfig().read_path('/project.conf', 'LOG', 'log_path')


class MyLog:
    def my_log(self, msg, msg_level, log_name='Debug_log', level='DEBUG',
               file_path=_path):
        # 日志收集器
        logger = logging.getLogger(log_name)
        logger.setLevel(level)  # 日志收集器的级别
        # 输出渠道  相对路径
        fh = logging.FileHandler(file_path, encoding='UTF-8')
        sh = logging.StreamHandler()
        fh.setLevel(level)  # 输出渠道的级别
        sh.setLevel(level)
        formatter = logging.Formatter('【%(asctime)s】-【%(levelname)s】-【%(filename)s-%(name)s】-【日志信息】:%(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        logger.addHandler(fh)
        if msg_level == 'DEBUG':
            logger.debug(msg)
        elif msg_level == 'INFO':
            logger.info(msg)
        elif msg_level == 'WARNING':
            logger.warning(msg)
        elif msg_level == 'ERROR':
            logger.error(msg)
        elif msg_level == 'CRITICAL':
            logger.critical(msg)
        # 使用完成后删除Handler、保持环境干净性
        logger.removeHandler(sh)
        logger.removeHandler(fh)

    def debug(self, msg):
        self.my_log(msg, 'DEBUG')

    def info(self, msg):
        self.my_log(msg, 'INFO')

    def warning(self, msg):
        self.my_log(msg, 'WARNING')

    def error(self, msg):
        self.my_log(msg, 'ERROR')

    def critical(self, msg):
        self.my_log(msg, 'CRITICAL')


if __name__ == '__main__':
    MyLog().error('{}'.format('This is a mylog'))
