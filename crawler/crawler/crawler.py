from selenium import webdriver

import crawler.nodes as nodes

class Crawler:
    def __init__(self, config, daemon_mode = False):
        self.root = self.parse(config)
        self.get_state = lambda: self.root.get_state()
        self.set_state = lambda state: self.root.set_state(state)
        if daemon_mode:
            self.driver = webdriver.PhantomJS()
        else:
            self.driver = webdriver.Chrome()

    def parse(self, config):
        return nodes.node_mapping[config._type](
            node_mapping = nodes.node_mapping,
            **config.__dict__)

    def run(self):
        for data in self.root.execute(self.driver):
            yield data
