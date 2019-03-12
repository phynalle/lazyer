from lazyer import Node, Pair

class Transform(Node):
    def __init__(self, node, func):
        self.node = node
        self.func = func

    def next(self):
        key, val = self.node.next().tup
        return Pair(key, self.func(val))
