class BaseNode(object):
    def __init__(self,node_mapping, children=[], name="node_element", sleep_seconds = 0, **kwargs):
        self.node_mapping = node_mapping
        self.children = []
        self.name = name
        self.sleep_seconds = sleep_seconds
        self._current_index = 0
        for child in children:
            self.children.append(self.parse(child))

    def parse(self, config):
        return self.node_mapping[config._type](
            node_mapping=self.node_mapping,
            **config.__dict__)

    def get_state(self):
        return {
            "index": self._current_index,
            "children": [child.get_state() for child in self.children]
        }

    def set_state(self, state):
        self._current_index = state["index"]
        for index, child in enumerate(self.children):
            child.set_state(state["children"][index])