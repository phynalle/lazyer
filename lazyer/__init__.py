import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

class NoInitializer(object):
    pass

class Pair(object):
    def __init__(self, key, value):
        self._key = key
        self._val = value

    @property
    def k(self):
        return self._key

    @property
    def v(self):
        return self._val


    @property
    def tup(self):
        return self.k, self.v


class Node(object):
    def next(self):
        raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        pair = self.next()
        if pair is None:
            raise StopIteration
        return (pair.k, pair.v)

    def transform(self, func):
        from lazyer.ops import Transform
        return Transform(self, func)

    def map(self, func):
        from lazyer.ops import Map
        return Map(self, func)

    def unmap(self):
        from lazyer.ops import Unmap
        return Unmap(self)

    def reduce(self, func, initializer=NoInitializer):
        from lazyer.ops import Reduce
        return Reduce(self, func, initializer)

    def filter(self, predicate):
        from lazyer.ops import Filter
        return Filter(self, predicate)

    def join(self, *nodes):
        from lazyer.ops import Join
        return Join(self, *nodes)

    def sort(self):
        from lazyer.ops import Sort
        return Sort(self)

    def partition(self, func):
        from lazyer.ops import Partition
        partition = Partition(self, func)
        return partition.forwards
