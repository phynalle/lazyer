from lazyer import Node, Pair

class Filter(Node):
    def __init__(self, node, predicate):
        self.node = node
        self.predicate = func

    def next(self):
        pair = self.node.next()
        while not self.predicate(pair.k, pair.v):
            pair = self.node.next()
        return pair
