from selenium import webdriver

import nodes


class Crawler:
    def __init__(self, config):
        self.root = self.parse(config)

    def parse(self, config):
        return nodes.node_mapping[config._type](
            node_mapping = nodes.node_mapping,
            **config.__dict__)

    def run(self):
        driver = webdriver.Chrome()
        for data in self.root.execute(driver):
            yield data
