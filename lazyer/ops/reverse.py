import heapq
from collections import defaultdict
from lazyer import Node, Pair

class Reverse(Node):
    def __init__(self, node):
        self.node = node
        self.elems = None
        self.is_collected = False

    def _collect(self):
        if self.is_collected:
            return
        self.elems = list(self.node)
        self.is_collected = True

    def try_next_pair(self):
        if not self.elems:
            raise StopIteration
        return Pair(*self.elems.pop())

    def next_pair(self):
        self._collect()
        return self.try_next_pair()
