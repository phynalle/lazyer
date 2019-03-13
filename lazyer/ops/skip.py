from collections import defaultdict
from lazyer import Node, Pair

class Skip(Node):
    def __init__(self, node, n):
        self.node = node
        self.num_skips = n
        self.counts = defaultdict(int)

    def try_next_pair(self):
        pair = self.node.next_pair()
        if self.counts[pair.k] < self.num_skips:
            self.counts[pair.k] += 1
            return None
        return pair

    def next_pair(self):
        pair = self.try_next_pair()
        while pair is None:
            pair = self.try_next_pair()
        return pair
