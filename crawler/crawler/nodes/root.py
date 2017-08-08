
from base_node import BaseNode
from config import Config


class Root(BaseNode):
    def __init__(self, origin, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = "origin"
        super(Root, self).__init__(**kwargs)
        self.origin = origin

    def execute(self, driver):
        driver.get(self.origin)

        for child in self.children:
            for data in child.execute(driver):
                data[self.name] = self.origin
                yield data
