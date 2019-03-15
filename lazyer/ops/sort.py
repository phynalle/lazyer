import heapq
from collections import defaultdict
from lazyer import Node, Pair

class Sort(Node):
    def __init__(self, node):
        self.node = node
        self.acc = defaultdict(list)
        self.keys = []
        self.is_sorted = False
        self.current = None

    def _sort(self):
        if self.is_sorted:
            return
        unique_keys = set()
        for key, val in self.node:
            if key not in unique_keys:
                unique_keys.add(key)
                self.keys.append(key)
            heapq.heappush(self.acc[key], val)
        self.is_sorted = True

    def try_next_pair(self):
        if self.current is None:
            if not self.keys:
                raise StopIteration
            key = self.keys.pop(0)
            if key not in self.acc:
                # Unreachable
                return None
            self.current = (key, self.acc.pop(key))
        key, values = self.current
        if not values:
            self.current = None
            return None
        return Pair(key, heapq.heappop(values))

    def next_pair(self):
        self._sort()
        pair = self.try_next_pair()
        while pair is None:
            pair = self.try_next_pair()
        return pair
