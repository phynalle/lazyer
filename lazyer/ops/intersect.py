from builtins import zip
from lazyer import Node, Pair
from lazyer.exceptions import DuplicatedKey, NodeException

class Intersect(Node):
    def __init__(self, *nodes):
        if len(nodes) < 2:
            raise NodeException('not enough nodes')
        for node in nodes:
            assert isinstance(node, Node)
        self.nodes = nodes
        self.accs = [{} for _ in nodes]
        self.keys = []
        self.is_intersected = False

    def _intersect(self):
        if self.is_intersected:
            return
        for i, (acc, node) in enumerate(zip(self.accs, self.nodes)):
            for key, val in node:
                if key in acc:
                    raise DuplicatedKey('node: {}'.format(i))
                if i == 0:
                    self.keys.append(key)
                acc[key] = val
        self.is_intersected = True

    def try_next_pair(self):
        if not self.keys:
            raise StopIteration
        values = []
        key = self.keys.pop()
        for acc in self.accs:
            if key not in acc:
                return None
            values.append(acc.pop(key, None))
        return Pair(key, values)

    def next_pair(self):
        self._intersect()
        pair = self.try_next_pair()
        while pair is None:
            pair = self.try_next_pair()
        return pair
