from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from copy import deepcopy

from base_node import BaseNode
from config import Config


class Link(BaseNode):
    def __init__(self, link, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = "link_value"
        super(Link, self).__init__(**kwargs)
        self.link = link

    def execute(self, driver):
        _current_url = driver.current_url

        element_present = EC.presence_of_element_located((By.XPATH, self.link))
        WebDriverWait(driver, 60).until(element_present)
        links = [link.get_attribute("href") for link in driver.find_elements_by_xpath(self.link)]

        for link in links:
            driver.get(link)
            for child in self.children:
                for data in child.execute(driver):
                    data[self.name] = link
                    yield data
        # go back to the original driver url
        driver.get(_current_url)