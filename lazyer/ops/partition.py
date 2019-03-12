from lazyer import Node, Pair

class Partition(Node):
    def __init__(self, node, func, n):
        self.node = node
        self.func = func

    def next(self):
        pass

# a, b, c = x.partition(func, 3)
#
# func(key, value, sinks):
#     a, b, c = sinks
#     a.sink
#
