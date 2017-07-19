
from base_node import BaseNode
from config import Config


class Root(BaseNode):
    def __init__(self, origin, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.origin = origin

    def execute(self, driver):
        driver.get(self.origin)

        result = Config()
        result.children = []
        for child in self.children:
            result.children.append(child.execute(driver))
        return result