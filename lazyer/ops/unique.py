from lazyer import Node, Pair

class Unique(Node):
    def __init__(self, node, func):
        self.node = node
        self.func = func
        self.keys = set()

    def try_next_pair(self):
        pair = self.node.next_pair()
        if pair.k in self.keys:
            return None
        if self.func(pair.k, pair.v):
            self.keys.add(pair.k)
        return pair

    def next_pair(self):
        pair = self.try_next_pair()
        while pair is None:
            pair = self.try_next_pair()
        return pair
