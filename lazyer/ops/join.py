import itertools
from lazyer import Node, Pair
from lazyer.exceptions import DuplicatedKey, NodeException

class Join(Node):
    def __init__(self, *nodes):
        if len(nodes) < 2:
            raise NodeException('not enough nodes')
        for node in nodes:
            assert isinstance(node, Node)
        self.nodes = nodes
        self.accs = [{} for _ in nodes]
        self.keys = []
        self.is_joined = False

    def join(self):
        if self.is_joined:
            return
        for i, (acc, node) in enumerate(itertools.izip(self.accs, self.nodes)):
            for key, val in node:
                if i == 0:
                    if key in acc:
                        raise DuplicatedKey
                    self.keys.append(key)
                acc[key] = val
        self.is_joined = True

    def try_next_pair(self):
        if not self.keys:
            raise StopIteration
        values = []
        key = self.keys.pop()
        values = [acc.pop(key) for acc in self.accs if key in acc]
        if len(values) != len(self.accs):
            return None
        return Pair(key, values)

    def next_pair(self):
        self.join()
        pair = self.try_next_pair()
        while pair is None:
            pair = self.try_next_pair()
        return pair
