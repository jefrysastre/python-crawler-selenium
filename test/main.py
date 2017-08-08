# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import Config

from crawler.crawler import Crawler

_path = os.path.dirname(os.path.abspath(__file__))
config = Config.load(_path+"/config/tjrj.json")
# config = Config.load(_path+"/config/cep.json")

crawler = Crawler(config)

# data = crawler.run()

# data.dump("tjrj_output.json")


# def data_gen(start=0, count = 0):
#     if count < 6:
#         for i in data_gen(start, count+1):
#             yield "number = {0}, count = {1}".format(i,count)
#     for n in range(0,99):
#         yield  "number = {0}, count = {1}".format(n,count)

for data in crawler.run():
    print data

