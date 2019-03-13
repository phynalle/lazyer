from lazyer import Node, Pair
from lazyer.ops import Forward

class Partition(Node):
    def __init__(self, node, n, func):
        self.node = node
        self.func = func
        self.forwards = [BufferedForward(self) for _ in range(n)]

    def next_pair(self):
        key, val = self.node.next_pair().tup
        self.func(key, val, self.forwards)


class BufferedForward(Forward):
    def __init__(self, node):
        super(BufferedForward, self).__init__(node)
        self.buffer = []

    def next_pair(self):
        while self.is_empty():
            self.node.next_pair()
        return Pair(None, self.buffer.pop(0))

    def append(self, pair):
        self.buffer.append(pair)

    def extend(self, *pairs):
        self.buffer.extend(pairs)

    def is_empty(self):
        return not bool(self.buffer)
