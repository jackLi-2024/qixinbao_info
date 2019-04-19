#!/usr/bin/python
# coding:utf-8

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@Baidu.com.xxxxxx
===========================================
"""
import random
import time
import os
import sys
import json
import multiprocessing

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../.." % cur_dir)
from lib.get_config import get_parames
from src.qixinbao import Qxb
from lib.util import read_file
from lib.util import write_file
from lib.util import mkdir_log
from lib.get_phone import get_phone
from lib.util import result_to_file


def target(firstname, lastname, parames):
    url = random.choice(json.loads(parames.get("url").get("product")))
    browser_type = parames.get("browser").get("browser_type")
    executable_path = parames.get("browser").get("executable_path")
    headless = eval(parames.get("browser").get("headless"))
    timeout = parames.get("browser").get("timeout")
    log = parames.get("data").get("log")
    username = get_phone()
    password = "Qxb" + username
    proxies = None
    qxb = Qxb(browser_type=browser_type, headless=headless, username=username, password=password,
              timeout=timeout, proxies=proxies, executable_path=executable_path)
    result = qxb.regist(url=url)
    result_to_file(result, log, data_type="regist")
    qxb.close()


def run(conf):
    parames = get_parames(conf)
    work_num = parames.get("master").get("work_num", "2")
    firstname = parames.get("regist").get("firstname", "Lee")
    lastname = parames.get("regist").get("lastname", "Jack")
    regist_num = int(parames.get("master").get("regist_num", 10))
    pool = multiprocessing.Pool(int(work_num))
    for one in range(regist_num):
        pool.apply_async(target, args=(firstname, lastname, parames))
    pool.close()
    pool.join()


if __name__ == '__main__':
    run("./conf/qixinbao_conf.txt")
