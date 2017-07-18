from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from base_node import BaseNode


class Data(BaseNode):
    def __init__(self, fields, **kwargs):
        super(BaseNode, self).__init__()
        self.fields = fields.__dict__
        self.data = {}

    def execute(self, driver):
        for key, value in self.fields.items():
            element_present = EC.presence_of_element_located((By.XPATH, value))
            WebDriverWait(driver, 60).until(element_present)
            self.data[key] = driver.find_element_by_xpath(value).text

        for child in self.children:
            child.execute(driver)