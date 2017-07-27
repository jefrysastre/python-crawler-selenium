# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import Config

from crawler import Crawler

_path = os.path.dirname(os.path.abspath(__file__))
config = Config.load(_path+"/config/tjrj.json")
# config = Config.load(_path+"/config/cep.json")

crawler = Crawler(config)

data = crawler.run()

data.dump("output.json")
