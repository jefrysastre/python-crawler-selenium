from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

from .base_node import BaseNode
from .config import Config


class Repeater(BaseNode):

    def __init__(self, selector, values=None, start=None, end=None, end_regex=None, reset_initial_state=True, clickable=False, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = "repeater_value"
        super(Repeater, self).__init__(**kwargs)
        self.selector = selector
        self.start = start
        self.end = end
        self.end_regex = end_regex
        self.reset_initial_state = reset_initial_state
        self.clickable = clickable
        self._current_value = 0

        if type(values) in [str]:
            import cPickle as pickle
            with open(values, 'rb') as file:
                self.values = pickle.load(file)
        elif values:
            self.values = values
        elif start and end and type(end) is int:
            self.values = range(start, end + 1)
        elif not end or not start or type(end) not in [str] or not end_regex:
            raise Exception("Error: Undefined values field.")
        else:
            pass

    def execute(self, driver):
        time.sleep(self.sleep_seconds)

        _current_url = driver.current_url

        has_just_one_result_page = False

        if self.start and self.end and self.end_regex and type(self.end) in [str]:
            import re

            try:
                element_present = EC.presence_of_element_located((By.XPATH, self.selector.format(self.end)))
                WebDriverWait(driver, 20).until(element_present)
            except TimeoutException:
                has_just_one_result_page = True
                self.values = [1]

            if not has_just_one_result_page:
                elem = driver.find_element_by_xpath(self.end)
                exps = re.findall(self.end_regex, elem.text)
                if len(exps) > 0:
                    self.values = range(self.start, int(exps[-1]) + 1)
                else:
                    raise Exception("Error: Regex did not match anything.")

        _count_current_value = len(self.values)
        while self._current_value < _count_current_value:
            if not self.clickable:
                if not has_just_one_result_page:
                    if "{0}" in self.selector:
                        element_present = EC.presence_of_element_located((By.XPATH, self.selector.format(self.values[self._current_value])))
                        WebDriverWait(driver, 60).until(element_present)
                        elem = driver.find_element_by_xpath(self.selector.format(self.values[self._current_value]))
                        driver.execute_script("arguments[0].scrollIntoView();", elem)
                        elem.click()
                    else:
                        element_present = EC.presence_of_element_located((By.XPATH, self.selector))
                        WebDriverWait(driver, 60).until(element_present)
                        elem = driver.find_element_by_xpath(self.selector)
                        driver.execute_script("arguments[0].scrollIntoView();", elem)
                        elem.send_keys(self.values[self._current_value])

            _count_current_index = len(self.children)
            while self._current_index < _count_current_index:
                for data in self.children[self._current_index].execute(driver):
                    data[self.name] = str(self.values[self._current_value])
                    yield data
                self._current_index += 1

            if self.clickable:
                element_present = EC.presence_of_element_located((By.XPATH, self.selector))
                WebDriverWait(driver, 60).until(element_present)
                elem = driver.find_element_by_xpath(self.selector)
                driver.execute_script("arguments[0].scrollIntoView();", elem)
                time.sleep(1)
                elem.click()

            self._current_index = 0
            self._current_value += 1

            if self.reset_initial_state:
                driver.get(_current_url)

        self._current_index = 0
        self._current_value = 0

    def get_state(self):
        result = super(Repeater, self).get_state()
        result["value"] = self._current_value
        return result

    def set_state(self, state):
        self._current_value = state["value"]
        super(Repeater, self).set_state(state)
