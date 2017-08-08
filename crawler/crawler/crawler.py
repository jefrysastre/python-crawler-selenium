from selenium import webdriver

import nodes


class Crawler:
    def __init__(self, config):
        self.root = self.parse(config)
        self.get_state = lambda: self.root.get_state()
        self.set_state = lambda state: self.root.set_state(state)

    def parse(self, config):
        return nodes.node_mapping[config._type](
            node_mapping = nodes.node_mapping,
            **config.__dict__)

    def run(self):
        driver = webdriver.Chrome()
        for data in self.root.execute(driver):
            yield data
