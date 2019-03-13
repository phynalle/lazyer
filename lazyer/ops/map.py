from lazyer import Node, Pair
from lazyer.exceptions import AlreadyMapped

class Map(Node):
    def __init__(self, node, func):
        self.node = node
        self.func = func

    def next_pair(self):
        key, val = self.node.next_pair().tup
        if key is not None:
            raise AlreadyMapped
        key, val = self.func(val)
        return Pair(key, val)
