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
import requests


def get_phone():
    url = "http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=01392656067d476e9c420d0778dbd440519f629f9701&itemid=2542"
    phone = requests.get(url).text.split('|')[1]
    return phone
