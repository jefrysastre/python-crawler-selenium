
from .base_node import BaseNode
from .config import Config


class Root(BaseNode):
    def __init__(self, origin, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = "origin"
        super(Root, self).__init__(**kwargs)
        self.origin = origin

    def execute(self, driver):
        driver.get(self.origin)

        _count_current_index = len(self.children)
        while self._current_index < _count_current_index:
            for data in self.children[self._current_index].execute(driver):
                data[self.name] = self.origin
                yield data
            self._current_index += 1
        self._current_index = 0
