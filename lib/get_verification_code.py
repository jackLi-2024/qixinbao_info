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
import re
import sys
import json
import requests


def get_code(phone):
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=01392656067d476e9c420d0778dbd440519f629f9701&itemid=2542&mobile=" + phone + "&release=1"
    response = requests.get(url).text
    if response == "3001":
        return "1"  # 继续等待
    elif '|' in response:
        if re.findall(r"[0-9]{1,}", response):
            return re.findall(r"[0-9]{1,}", response)[0]  # 返回验证码
        else:
            return "0"
    else:
        return "0"  # 错误代码
