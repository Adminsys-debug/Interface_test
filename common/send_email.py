# !/usr/bin/python3
# @File: send_email.py
# --coding:utf-8--
# @Author: tim.chen
# @date 2019/11/7 11:37
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage


def main():
    sender = 'tim.chen@gizutech.com'
    receiverList = ['tim.chen@gizutech.com']
    user = 'tim.chen@gizutech.com'
    emailPwd = 'Xiaoshen=='  # 用需开通授权码
    smtpServer = 'smtp.gizutech.com'
    commonPort = 25
    emailTitle = 'Interface_test'
    test_report = r'/Users/mr.chen/Interface_test/test_result/html_report'  # 存放文件的目录
    lists = os.listdir(test_report)  # 列出目录的下所有文件保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn))  # 按时间排序
    file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
    attachPathList = [
        r'/Users/mr.chen/Interface_test/test_result/log/test_log.log',
        r'/Users/mr.chen/Interface_test/test_result/image']
    emailChanel(sender, receiverList, user, emailPwd, smtpServer, commonPort, emailTitle, file_new, attachPathList)


def emailChanel(sender, receiverList, user, emailPwd, smtpServer, commonPort, emailTitle, htmlPath=None,
                attachPathList=None):
    multiPart = MIMEMultipart()
    multiPart['From'] = sender
    multiPart['To'] = ','.join(receiverList)
    subject = emailTitle
    multiPart['Subject'] = Header(subject, "utf-8")
    if os.path.isfile(htmlPath):
        if os.path.exists(htmlPath):
            pass
        else:
            raise IOError("htmlPath not exist")
    else:
        raise IOError("html path is not file..")
    emailBody = MIMEText(_text=open(htmlPath, 'rb').read(), _subtype='html', _charset="utf-8")
    multiPart.attach(emailBody)
    if isinstance(attachPathList, list):
        for attachPath in attachPathList:
            if os.path.exists(attachPath):
                pass
            else:
                raise IOError("attachPath not exist")
    else:
        raise TypeError("expected type is list,but get {}".format(type(attachPathList).__name__))
    for attachPath in attachPathList:
        if os.path.splitext(attachPath)[-1] == ".log":
            attach = MIMEText(open(attachPath, 'rb').read(), 'base64', 'utf-8')
            attach["Content-Type"] = 'application/octet-stream'
            attach["Content-Disposition"] = 'attachment; filename="Interface_test.log"'  # filename not strict
            multiPart.attach(attach)
        if os.path.splitext(attachPath)[-1] == ".png":
            fp = open(attachPath, 'rb')
            msgImage = MIMEImage(fp.read(), _subtype='octet-stream')
            fp.close()
            msgImage.add_header('Content-Disposition', 'attachment', filename="attach.png")
            multiPart.attach(msgImage)
    smtp = smtplib.SMTP(timeout=30)
    try:
        smtp.connect(host=smtpServer, port=commonPort)
        smtp.login(user, emailPwd)
        smtp.sendmail(sender, receiverList, multiPart.as_string())
    except smtplib.SMTPException as e:
        print("send fail", e)
    else:
        print("success")
    finally:
        try:
            smtp.quit()
        except smtplib.SMTPException:
            print("{}".format('quit fail'))
        else:
            print("{}".format('quit success'))


if __name__ == '__main__':
    main()
