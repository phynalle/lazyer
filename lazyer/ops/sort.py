from collections import defaultdict
from lazyer import Node, Pair

class Sort(Node):
    def __init__(self, node):
        self.node = node
        self.acc = defaultdict(list)
        self.keys = []
        self.is_sorted = False

    def sort(self):
        if self.is_sorted:
            return
        unique_keys = set()
        for key, val in self.node:
            if key not in unique_keys:
                self.unique_keys.add(key)
                self.keys.append(key)
            self.acc[key].append(val)
        for _, values in self.acc:
            values.sort()
        self.is_sorted = True

    def try_next(self):
        if not self.keys:
            raise StopIteration
        key = self.keys[0]
        if key not in self.acc:
            # Unreachable
            self.keys.pop(0)
            return None
        values = self.acc[key]
        if not values:
            self.keys.pop(0)
            return None
        return Pair(key, values.pop(0))

    def next(self):
        self.sort()
        pair = self.try_next()
        while pair is None:
            pair = self.try_next()
        return pair
