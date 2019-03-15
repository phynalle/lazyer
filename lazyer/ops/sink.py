from lazyer import Node, Pair

class Sink(Node):
    def __init__(self, iterable):
        self.iterable = iter(iterable)

    def next_pair(self):
        return Pair(None, next(self.iterable))
