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
import logging
from SpiderTool import Browser
from loggingtool import loggingtool
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/.." % cur_dir)

from lib.util import error_result
from lib.util import normal_result
from lib.get_phone import get_phone
from lib.get_verification_code import get_code


class Qxb(object):
    def __init__(self, proxies=None, headless=True,
                 timeout=20, executable_path=None,
                 browser_type=None, username=None, password=None):
        headless = bool(headless)
        timeout = int(timeout)
        self.username = username
        self.password = password
        if executable_path == "None":
            executable_path = None
        self.browser = Browser.Browser(proxies=proxies, headless=headless, timeout=timeout,
                                       executable_path=executable_path,
                                       browser_type=browser_type)
        self.browser.browser.set_window_size(1366, 768)

    def close(self):
        self.browser.close()

    def regist(self, url, firstname="Lee", lastname="Jack", wait_time=10):
        try:
            self.browser.get(url=url)
            self.browser.wait_for_element_loaded("btn-block", By.CLASS_NAME)
            regist_btn = self.browser.find_element("btn-block", By.CLASS_NAME)

            input_ = self.browser.find_elements("input-flat", By.CLASS_NAME)
            code_btn = self.browser.find_element("btn-lg", By.CLASS_NAME)
            self.browser.send_keys(input_[0], self.username)
            time.sleep(0.5)
            self.browser.click_elem(code_btn)
            # 等待验证码
            ticks = 0
            code = "1"
            while code == "1":
                code = get_code(self.username)
                if code == "1":
                    time.sleep(5)
                    ticks += 5
                elif code == "0":
                    result = {"username": self.username, "password": self.password, "url": url,
                              "msg": "regist defeatly", "error": "Verification-code Error"}
                    return error_result(result)

                if ticks >= 60:
                    result = {"username": self.username, "password": self.password, "url": url,
                              "msg": "regist defeatly", "error": "Verification-code Timeout"}
                    return error_result(result)
            self.browser.send_keys(input_[1], code)
            self.browser.send_keys(input_[2], self.password)
            self.browser.click_elem(regist_btn)

            self.browser.wait_for_element_loaded("user-name", By.CLASS_NAME)

            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "regist successfully", "Cookie": self.browser.browser.get_cookies()}
            return normal_result(result)
        except Exception as e:
            result = {"username": self.username, "password": self.password, "url": url,
                      "msg": "regist defeatly", "error": str(e)}
            return error_result(result)


def test_regist():
    url = "https://www.qixin.com/auth/regist"
    username = get_phone()
    password = "Qxb" + username
    qxb = Qxb(browser_type="Chrome", headless=False, username=username, password=password,
              timeout=20)
    print(qxb.regist(url=url))


if __name__ == '__main__':
    test_regist()
