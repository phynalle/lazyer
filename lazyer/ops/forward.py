from lazyer import Node

class Forward(Node):
    def __init__(self, node):
        self.node = node

    def next_pair(self):
        return self.node.next_pair()
