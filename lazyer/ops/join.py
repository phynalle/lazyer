from lazyer import Node, Pair
from lazyer.exceptions import DuplicatedKey, NodeException

class Join(Node):
    def __init__(self, *nodes):
        if len(nodes) < 2:
            raise NodeException('not enough nodes')
        self.nodes = nodes
        self.accs = [{} for _ in nodes]
        self.joined = False
        self.keys = []

    def join(self):
        if self.joined:
            return
        unique_keys = set()
        for acc, node in zip(self.accs, self.nodes):
            for key, val in node:
                if key not in unique_keys:
                    unique_keys.add(key)
                    self.keys.add(key)
                if key in acc:
                    raise DuplicatedKey
                acc[key] = val
        self.joined = True

    def try_next(self):
        if not self.keys:
            raise StopIteration
        values = []
        key = self.keys.pop()
        values = [acc.pop(key) for acc in self.accs if key in acc]
        if len(values) != len(self.accs):
            return None
        return Pair(key, values)

    def next(self):
        self.join()
        pair = self.try_next()
        while pair is None:
            pair = self.try_next()
        return pair
