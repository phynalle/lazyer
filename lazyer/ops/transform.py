from lazyer import Node, Pair

class Transform(Node):
    def __init__(self, node, func):
        self.node = node
        self.func = func

    def next_pair(self):
        key, val = self.node.next_pair().tup
        return Pair(key, self.func(val))
