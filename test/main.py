# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import Config

from crawler.crawler import Crawler

_path = os.path.dirname(os.path.abspath(__file__))
config = Config.load(_path+"/config/pit2.json")

crawler = Crawler(config)

state = None
for index, data in enumerate(crawler.run()):
    state = crawler.get_state()
    if index == 11:
        break
    print(data)

print("------------------------------------------------------------------------")
crawler2 = Crawler(config)
crawler2.set_state(state)

for index, data in enumerate(crawler.run()):
    print(data)
