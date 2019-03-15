from builtins import zip
from lazyer import Node, Pair
from lazyer.exceptions import DuplicatedKey, NodeException

class Differ(Node):
    def __init__(self, *nodes):
        if len(nodes) < 2:
            raise NodeException('not enough nodes')
        for node in nodes:
            assert isinstance(node, Node)
        self.nodes = nodes
        self.accs = [{} for _ in nodes]
        self.excluded_keys = set()
        self.is_consumed = False

    def _consume(self):
        if self.is_consumed:
            return
        for node in self.nodes[1:]:
            for key, _ in node:
                self.excluded_keys.add(key)
        self.is_consumed = True

    def try_next_pair(self):
        pair = self.nodes[0].next_pair()
        if pair.k in self.excluded_keys:
            return None
        return pair

    def next_pair(self):
        self._consumed()
        pair = self.try_next_pair()
        while pair is None:
            pair = self.try_next_pair()
        return pair
