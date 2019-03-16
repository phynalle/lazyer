from lazyer import Node, Pair

class Iterate(Node):
    def __init__(self, node):
        self.node = node
        self.iterator = None

    def try_next_pair(self):
        if self.iterator is None:
            pair = self.node.next_pair()
            try:
                self.iterator = (pair.k, iter(pair.v))
            except TypeError:
                return pair
        try:
            key, it = self.iterator
            return Pair(key, next(it))
        except StopIteration:
            self.iterator = None
            return None

    def next_pair(self):
        pair = self.try_next_pair()
        while pair is None:
            pair = self.try_next_pair()
        return pair
