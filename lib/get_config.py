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
import ConfigParser


def get_parames(conf):
    config = ConfigParser.ConfigParser()
    config.read(conf)
    return config._sections


if __name__ == '__main__':
    print(get_parames("../conf/nike.conf"))
