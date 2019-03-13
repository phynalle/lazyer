from lazyer import Node, Pair
from lazyer.ops import Forward

class Partition(Node):
    def __init__(self, node, n, func):
        self.node = node
        self.func = func
        self.forwards = [PartitionedForward(self) for _ in range(n)]

    def next_pair(self):
        key, val = self.node.next_pair().tup
        self.func(key, val, self.forwards)


class PartitionedForward(Forward):
    def __init__(self, partition):
        super(PartitionedForward, self).__init__(partition)
        self.buffer = []

    def next_pair(self):
        while self.is_empty():
            super(PartitionedForward, self).next_pair()
        return Pair(None, self.buffer.pop(0))

    def push(self, *pair):
        self.buffer.extend(pair)

    def is_empty(self):
        return not bool(self.buffer)
