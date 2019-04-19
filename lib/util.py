#!/usr/bin/python
# coding:utf-8

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@Baidu.com.xxxxxx
===========================================
"""

import os
import sys
import json
import time
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header


def error_result(error_msg=None, error_code=-1):
    result = {
        "status": error_code,
        "response": error_msg
    }
    return result


def normal_result(data):
    result = {
        "status": 1,
        "response": data
    }
    return result


def write_file(filename="", data="", mode="a"):
    if type(data) != str:
        try:
            data = json.dumps(data, ensure_ascii=False).encode("utf8")
        except Exception as e:
            data = "No json data --> %s" % str(e)
    with open(filename, mode, 0) as f:
        f.write(data + "\n")
    return


def read_file(filename="", data="", mode="r"):
    with open(filename, mode) as f:
        lines = f.readlines()
    return lines


def mkdir_log(log):
    try:
        os.listdir(log)
    except:
        os.mkdir(log)


def result_to_file(result, log, data_type=""):
    today = time.strftime("%Y%m%d", time.gmtime(time.time()))
    mkdir_log("%s/%s" % (log, today))
    if result.get("status", "0") == 1:
        write_file("%s/%s/%s_success.txt" % (log, today, data_type), result)
        # with open("%s/%s/%s_success.txt" % (log, today, data_type),"a") as f:
        #     f.write(result + "\n")
    else:
        write_file("%s/%s/%s_defeat.txt" % (log, today, data_type), result)
        # with open("%s/%s/%s_defeat.txt" % (log, today, data_type),"a") as f:
        #     f.write(result + "\n")


class Email(object):
    """注意：文件名需加上扩展名，查看邮箱时浏览器可解析显示"""

    # 初始化邮件相关配置
    def __init__(self, email_smtpserver, email_port, email_sender, email_password, email_receiver,
                 email_subject):
        self.__smtpserver = email_smtpserver
        self.__smtport = email_port
        self.__sender = email_sender
        self.__password = email_password
        self.__receiver = email_receiver
        self.__subject = email_subject + "    " + \
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.__subject = Header(self.__subject, 'utf-8').encode()
        self.__msg = MIMEMultipart('mixed')
        self.__msg['Subject'] = self.__subject
        self.__msg['From'] = self.__sender
        self.__msg['To'] = ";".join(self.__receiver)

    # 附加文本内容
    def appendText(self, text):
        text_plain = MIMEText(text, 'plain', 'utf-8')
        self.__msg.attach(text_plain)

    # 附加图片 imgBytes:图片的二进制数据 imgName:图片名称
    def appendImage(self, imgBytes, imgName):
        image = MIMEImage(imgBytes)
        image.add_header('Content-Disposition', 'attachment', filename=imgName)
        self.__msg.attach(image)

    # 附加html htmlStr:字符串
    def appendHtml(self, htmlStr, htmlName):
        text_html = MIMEText(htmlStr, 'html', 'utf-8')
        text_html.add_header('Content-Disposition',
                             'attachment', filename=htmlName)
        self.__msg.attach(text_html)

    # 附加附件
    def appendAttachment(self, attachName):
        pass

    # 发送邮件
    def sendEmail(self):
        smtp = None
        try:
            smtp = smtplib.SMTP_SSL(self.__smtpserver, self.__smtport)
            smtp.login(self.__sender, self.__password)
            smtp.sendmail(self.__sender, self.__receiver,
                          self.__msg.as_string())

        except Exception as e:
            logging.exception(str(e))
        try:
            smtp.quit()
        except:
            pass


def test_email():
    pass


if __name__ == '__main__':
    test_email()
