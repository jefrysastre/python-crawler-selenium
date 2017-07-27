from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from base_node import BaseNode
from config import Config


class Data(BaseNode):
    def __init__(self, fields, **kwargs):
        super(Data, self).__init__(**kwargs)
        self.fields = fields.__dict__
        self.data = {}

    def execute(self, driver):
        for key, value in self.fields.items():
            element_present = EC.presence_of_element_located((By.XPATH, value))
            WebDriverWait(driver, 60).until(element_present)
            self.data[key] = []
            for element in driver.find_elements_by_xpath(value):
                if element.tag_name == "a":
                    text = element.text
                    href = element.get_attribute("href")
                    
                    self.data[key].append({text: href})
                elif element.tag_name == "tr":
                    tds = [td.text for td in element.find_elements_by_tag_name('td')]
                    
                    self.data[key].append(tds)
                else:
                    self.data[key].append(element.text)
        
        result = Config()
        result.data = self.data
        result.children = []
        for child in self.children:
            result.children.append(child.execute(driver))
        return result