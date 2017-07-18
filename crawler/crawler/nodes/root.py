
from base_node import BaseNode


class Root(BaseNode):
    def __init__(self, origin, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.origin = origin

    def execute(self, driver):
        driver.get(self.origin)

        for child in self.children:
            child.execute(driver)