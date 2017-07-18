from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from base_node import BaseNode


class Repeater(BaseNode):
    def __init__(self, selector, values = None, start = None, end=None, end_regex=None, sleep_seconds = 0,  **kwargs):
        super(Repeater, self).__init__(**kwargs)
        self.selector = selector
        self.sleep_seconds = sleep_seconds
        self.start = start
        self.end = end
        self.end_regex = end_regex

        if type(values) in [str, unicode]:
            import cPickle as pickle
            with open(values,'rb') as file:
                self.values = pickle.load(file)
        elif values:
            self.values = values
        elif start and end and type(end) is int:
            self.values = range(start, end + 1)
        elif not end or not start or type(end) not in [str, unicode] or not end_regex:
            raise Exception("Error: Undefined values field.")
        else:
            pass

    def execute(self, driver):
        if self.start and self.end and self.end_regex and type(self.end) in [str, unicode]:
            import re
            element_present = EC.presence_of_element_located((By.XPATH, self.selector.format(self.end)))
            time.sleep(self.sleep_seconds)
            WebDriverWait(driver, 60).until(element_present)
            elem = driver.find_element_by_xpath(self.end)
            exps = re.findall(self.end_regex, elem.text)
            if len(exps) > 0:
                self.values = range(self.start, int(exps[-1]))
            else:
                raise Exception("Error: Regex did not match anything.")

        for value in self.values:

            if "{0}" in self.selector:
                element_present = EC.presence_of_element_located((By.XPATH, self.selector.format(value)))
                WebDriverWait(driver, 60).until(element_present)
                driver.find_element_by_xpath(self.selector.format(value)).click()
            else:
                element_present = EC.presence_of_element_located((By.XPATH, self.selector))
                WebDriverWait(driver, 60).until(element_present)
                driver.find_element_by_xpath(self.selector).send_keys(value)

            for child in self.children:
                child.execute(driver)