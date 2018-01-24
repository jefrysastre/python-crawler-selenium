from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from .base_node import BaseNode
from .config import Config



class Form(BaseNode):
    def __init__(self, submit, fields,  **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = "form_value"
        super(Form, self).__init__(**kwargs)
        self.fields = fields.__dict__
        self.submit = submit

    def execute(self, driver):
        for key, value in self.fields.items():

            element_present = EC.presence_of_element_located((By.XPATH, key))
            WebDriverWait(driver, 60).until(element_present)
            elem = driver.find_element_by_xpath(key)

            driver.execute_script("arguments[0].scrollIntoView();", elem)

            if value == "*":
                elem.click()
            else:
                elem.send_keys(value)
        
        elem = None
        
        for i in range(len(self.submit)):
            try:
                elem = driver.find_element_by_xpath(self.submit[i])
                
                driver.execute_script("arguments[0].scrollIntoView();", elem)
                
                break
            except NoSuchElementException:
                pass
        
        if elem is not None:
            elem.click()
        
        _count_current_index = len(self.children)
        while self._current_index < _count_current_index:
            for data in self.children[self._current_index].execute(driver):
                data[self.name] = self.fields
                yield data
            self._current_index += 1
        self._current_index = 0
