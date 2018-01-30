from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from copy import deepcopy
import time

from .base_node import BaseNode
from .config import Config


class Link(BaseNode):
    def __init__(self, link, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = "link_value"
        super(Link, self).__init__(**kwargs)
        self.link = link
        self._current_link = 0

    def execute(self, driver):
        time.sleep(self.sleep_seconds)

        _current_url = driver.current_url

        try:
            element_present = EC.presence_of_element_located((By.XPATH, self.link))
            WebDriverWait(driver, 20).until(element_present)
        except TimeoutException:
            return
        
        links = [link.get_attribute("href") for link in driver.find_elements_by_xpath(self.link)]
        
        links.sort()
        
        _count_link = len(links)
        while self._current_link < _count_link:
            driver.get(links[self._current_link])
            _count_current_index = len(self.children)
            while self._current_index < _count_current_index:
                for data in self.children[self._current_index].execute(driver):
                    data[self.name] = links[self._current_link]
                    yield data
                self._current_index += 1

            self._current_index = 0
            self._current_link += 1
        # go back to the original driver url

        self._current_index = 0
        self._current_link = 0
        driver.get(_current_url)

    def get_state(self):
        result = super(Link, self).get_state()
        result["link"] = self._current_link
        return result

    def set_state(self, state):
        self._current_link = state["link"]
        super(Link, self).set_state(state)
