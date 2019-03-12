from lazyer import Node, Pair
from lazyer.exceptions import NotMapped

class Unmap(Node):
    def __init__(self, node):
        self.node = node

    def next(self):
        kv = self.node.next().tup
        if kv[0] is None:
            raise NotMapped
        return Pair(None, kv)
