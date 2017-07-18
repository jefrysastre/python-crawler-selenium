class BaseNode(object):
    def __init__(self,node_mapping, children=[], **kwargs):
        self.node_mapping = node_mapping
        self.children = []
        for child in children:
            self.children.append(self.parse(child))

    def parse(self, config):
        return self.node_mapping[config._type](
            node_mapping=self.node_mapping,
            **config.__dict__)
