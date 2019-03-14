from lazyer import Node, Pair

class Filter(Node):
    def __init__(self, node, predicate):
        self.node = node
        self.predicate = predicate

    def next_pair(self):
        pair = self.node.next_pair()
        while not self.predicate(pair.v):
            pair = self.node.next_pair()
        return pair
