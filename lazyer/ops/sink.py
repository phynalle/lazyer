from lazyer import Node, Pair

class Sink(Node):
    def __init__(self, gen):
        self.gen = gen

    def next_pair(self):
        return Pair(None, next(self.gen))
