from lazyer import Node, Pair

class Source(Node):
    def __init__(self, iterable):
        self.iterable = iter(iterable)

    def next_pair(self):
        return Pair(None, next(self.iterable))
