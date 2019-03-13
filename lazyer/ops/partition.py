from lazyer import Node, Pair
from lazyer.ops import Forward

class Partition(Node):
    def __init__(self, node, func, n):
        self.node = node
        self.func = func
        self.forwards = (BufferedForward(self) for _ in range(n))

    def next(self):
        self.func(key, value, self.forwards)


class BufferedForward(Forward):
    def __init__(self, node):
        super(BufferedForward, self).__init__(node)
        self.buffer = []

    def next(self):
        while self.is_empty():
            self.node.next()
        return self.buffer.pop(0)

    def append(self, *pair):
        self.buffer.extend(pair)

    def is_empty(self):
        return bool(self.buffer)
