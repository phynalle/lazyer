from lazyer import Node
from lazyer.exceptions import NodeException

class Chain(Node):
    def __init__(self, *nodes):
        if len(nodes) < 2:
            raise NodeException('not enough nodes')
        self.nodes = nodes
        self.current_node = None

    def try_next(self):
        if current_node is None:
            if not self.nodes:
                raise StopIteration
            current_node = self.nodes.pop(0)
        try:
            return current_node.next()
        except StopIteration:
            current_node = None
            return None

    def next(self):
        pair = self.try_next()
        while pair is None:
            pair = self.try_next()
        return pair
