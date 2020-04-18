#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/28 16:17
# @Author  : Mr.chen
# @Site    : 
# @File    : run.py
# @Software: PyCharm
# @Email   : 794281961@qq.com

import HTMLTestRunner
import time
import unittest
from conf.read_config import ReadConfig
from common.test_http_request import TestHttpRequest
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage
from common.my_log import MyLog

# 实例化日志类
logger=MyLog()


class RunTest:

    def runtestdict(self):
        report_path=ReadConfig().read_path( '/project.conf', 'TESTREPORT', 'report' )
        suite=unittest.TestSuite()
        loader=unittest.TestLoader()
        suite.addTest( loader.loadTestsFromTestCase( TestHttpRequest ) )
        now=time.strftime( '%Y-%m-%d_%H_%M_%S' )  # 获取当前时间
        file_path=report_path + 'test-' + now + '.html'

        # 执行用例
        with open( file_path, 'wb' ) as file:
            runner=HTMLTestRunner.HTMLTestRunner(
                # retry，用例执行失败后指定重试次数，
                # 如果save_last_try
                # 为True ，一个用例仅显示最后一次测试的结果。
                # 为True，则展示全部测试结果。
                # verbosity = 2
                # 为信息输出控制台的展示方式
                # retry，指定重试次数
                # 分类: unittest框架, 第三方报告
                stream=file,
                verbosity=2,
                title='Interface_iframe',
                description=u'Tim_chen :  ',
                retry=2,
                save_last_try=False
            )
            runner.run( suite )

    def send_email(self):
        sender='tim.chen@gizutech.com'
        receiverList=['tim.chen@gizutech.com']
        user='tim.chen@gizutech.com'
        emailPwd='Xiaoshen=='  # 用需开通授权码
        smtpServer='smtp.gizutech.com'
        commonPort=25
        emailTitle='Interface_test'
        test_report=r'/Users/mr.chen/Interface_test/test_result/html_report'  # 存放文件的目录
        lists=os.listdir( test_report )  # 列出目录的下所有文件保存到lists
        lists.sort( key=lambda fn: os.path.getmtime( test_report + "/" + fn ) )  # 按时间排序
        file_new=os.path.join( test_report, lists[-1] )  # 获取最新的文件保存到file_new
        attachPathList=[
            r'/Users/mr.chen/Interface_test/test_result/log/test_log.log',
            r'/Users/mr.chen/Interface_test/test_result/image']
        self.emailChanel( sender, receiverList, user, emailPwd, smtpServer, commonPort, emailTitle, file_new,
                          attachPathList )

    def emailChanel(self, sender, receiverList, user, emailPwd, smtpServer, commonPort, emailTitle, htmlPath=None,
                    attachPathList=None):
        multiPart=MIMEMultipart()
        multiPart['From']=sender
        multiPart['To']=','.join( receiverList )
        subject=emailTitle
        multiPart['Subject']=Header( subject, "utf-8" )
        if os.path.isfile( htmlPath ):
            if os.path.exists( htmlPath ):
                pass
            else:
                raise IOError( '{}'.format( "htmlPath not exist" ) )
        else:
            raise IOError( '{}'.format( "html path is not file.." ) )
        emailBody=MIMEText( _text=open( htmlPath, 'rb' ).read(), _subtype='html', _charset="utf-8" )
        multiPart.attach( emailBody )
        if isinstance( attachPathList, list ):
            for attachPath in attachPathList:
                if os.path.exists( attachPath ):
                    pass
                else:
                    raise IOError( '{}'.format( "attachPath not exist" ) )
        else:
            raise TypeError( "expected type is list,but get {}".format( type( attachPathList ).__name__ ) )
        for attachPath in attachPathList:
            if os.path.splitext( attachPath )[-1] == ".log":
                attach=MIMEText( open( attachPath, 'rb' ).read(), 'base64', 'utf-8' )
                attach["Content-Type"]='application/octet-stream'
                attach["Content-Disposition"]='attachment; filename="Interface_test.log"'  # filename not strict
                multiPart.attach( attach )
            if os.path.splitext( attachPath )[-1] == ".png":
                fp=open( attachPath, 'rb' )
                msgImage=MIMEImage( fp.read(), _subtype='octet-stream' )
                fp.close()
                msgImage.add_header( 'Content-Disposition', 'attachment', filename="attach.png" )
                multiPart.attach( msgImage )
        smtp=smtplib.SMTP( timeout=30 )
        try:
            smtp.connect( host=smtpServer, port=commonPort )
            smtp.login( user, emailPwd )
            smtp.sendmail( sender, receiverList, multiPart.as_string() )
        except smtplib.SMTPException as e:
            logger.info( '{},{}'.format( 'send fail', e ) )
        else:
            logger.info( '{}'.format( "success" ) )
        finally:
            try:
                smtp.quit()
            except smtplib.SMTPException:
                logger.info( "{}".format( 'quit fail' ) )
            else:
                logger.info( "{}".format( 'quit success' ) )


if __name__ == '__main__':
    RunTest().runtestdict()
    time.sleep(5)
    RunTest().send_email()
