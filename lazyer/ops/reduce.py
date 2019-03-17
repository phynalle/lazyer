from six import viewkeys
from lazyer import no_init, Node, Pair

class Reduce(Node):
    def __init__(self, node, func, initializer):
        self.node = node
        self.func = func
        self.acc = {}
        self.keys = []
        self.initializer = initializer
        self.is_reduced = False

    def _reduce(self):
        if self.is_reduced:
            return
        for key, val in self.node:
            if key not in self.acc:
                self.keys.append(key)
                if self.initializer is no_init:
                    self.acc[key] = val
                    continue
                default = self.initializer
                if callable(default):
                    default = default()
                self.acc[key] = default
            self.acc[key] = self.func(self.acc[key], val)
        self.is_reduced = True

    def next_pair(self):
        self._reduce()
        if not self.keys:
            raise StopIteration
        k = self.keys.pop(0)
        v = self.acc.pop(k)
        return Pair(k, v)
