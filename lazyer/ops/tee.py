from lazyer import Node, Pair
from lazyer.exceptions import NodeException
from lazyer.ops.forward import Forward

class Tee(Node):
    def __init__(self, node, n):
        if n <= 0:
            raise NodeException('cannot create {} clones'.format(n))
        self.node = node
        self.cloneds = [Cloned(self) for _ in range(n)]

    def next_pair(self):
        pair = self.node.next_pair()
        for cloned in self.cloneds:
            cloned.push(pair)
        return pair


class Cloned(Forward):
    def __init__(self, clone):
        super(Cloned, self).__init__(clone)
        self.buffer = []

    def next_pair(self):
        if not self.buffer:
            super(Cloned, self).next_pair()
        return self.buffer.pop(0)

    def push(self, pair):
        self.buffer.append(pair)
