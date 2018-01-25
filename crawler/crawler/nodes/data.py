from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from .base_node import BaseNode
from .config import Config
from selenium.common.exceptions import TimeoutException


class Data(BaseNode):
    def __init__(self, fields, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = "data_value"
        super(Data, self).__init__(**kwargs)
        self.fields = fields.__dict__
        self.data = {}

    def execute(self, driver):
        time.sleep(self.sleep_seconds)
        
        for key, value in self.fields.items():
            self.data[key] = []
            
            try:
                element_present = EC.presence_of_element_located((By.XPATH, value))
                WebDriverWait(driver, 10).until(element_present)
            except TimeoutException:
                continue
            
            for element in driver.find_elements_by_xpath(value):
                if element.tag_name == "a":
                    text = element.text
                    href = element.get_attribute("href")
                    
                    self.data[key].append({text: href})
                elif element.tag_name == "tr":
                    tds = [td.text for td in element.find_elements_by_tag_name('td')]
                    
                    self.data[key].append(tds)
                elif element.tag_name == "input":
                    text = element.get_attribute("value")
                    
                    self.data[key].append(text)
                else:
                    self.data[key].append(element.text)

        if len(self.children) == 0:
            yield {
                self.name: self.data
            }
        else:
            _count_current_index = len(self.children)
            while self._current_index < _count_current_index:
                for data in self.children[self._current_index].execute(driver):
                    data[self.name] = self.data
                    yield data
                self._current_index += 1
            self._current_index = 0
