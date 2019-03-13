from lazyer import Node, Pair

class Inspect(Node):
    def __init__(self, node, func, interval):
        self.node = node
        self.func = func
        self.interval = interval
        self.current = 0

    def try_inspect(self, pair):
        if self.interval < 1:
            return
        if self.current == 0:
            self.func(pair.k, pair.v)
        self.current = (self.current + 1) % self.interval

    def next_pair(self):
        pair = self.node.next_pair()
        self.try_inspect(pair)
        return pair
