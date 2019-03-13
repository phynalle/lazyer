from lazyer import Node, Pair

class Inspect(Node):
    def __init__(self, node, func):
        self.node = node
        self.func = func

    def next_pair(self):
        pair = self.node.next_pair()
        self.func(pair.k, pair.v)
        return pair
