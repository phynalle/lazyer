from lazyer import Node, Pair

class Sink(Node):
    def __init__(self, iterable):
        self.iterable = iter(iterable)

    def next_pair(self)i:
        return Pair(None, next(self.gen))
