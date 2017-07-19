# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import Config

from crawler import Crawler

_path = os.path.dirname(os.path.abspath(__file__))
# config = Config.load(_path+"/config/tjrj.json")
config = Config.load(_path+"/config/cep.json")

crawler = Crawler(config)

data = crawler.run()

input("Press Enter to continue...")


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Firefox()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()


