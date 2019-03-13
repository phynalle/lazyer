from lazyer import Node
from lazyer.exceptions import NodeException

class Chain(Node):
    def __init__(self, *nodes):
        if len(nodes) < 2:
            raise NodeException('not enough nodes')
        self.nodes = list(nodes)
        self.current_node = None

    def try_next_pair(self):
        if self.current_node is None:
            if not self.nodes:
                raise StopIteration
            self.current_node = self.nodes.pop(0)
        try:
            return self.current_node.next_pair()
        except StopIteration:
            self.current_node = None
            return None

    def next_pair(self):
        pair = self.try_next_pair()
        while pair is None:
            pair = self.try_next_pair()
        return pair
