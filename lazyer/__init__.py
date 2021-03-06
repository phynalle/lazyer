import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from lazyer.utils import call_unpacked, identity, make_flattened_str, print_pair, true


class NoInitializer(object):
    pass


no_init = NoInitializer


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
    def next_pair(self):
        raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        pair = self.next_pair()
        if pair is None:
            raise StopIteration
        return (pair.k, pair.v)

    next = __next__

    def tee(self, n=2):
        from lazyer.ops import Tee
        return Tee(self, n).cloneds

    def transform(self, func):
        from lazyer.ops import Transform
        return Transform(self, func)

    def map(self, func=identity):
        from lazyer.ops import Map
        return Map(self, func)

    def remap(self, func):
        return self.unmap().map(call_unpacked(func))

    def unmap(self):
        from lazyer.ops import Unmap
        return Unmap(self)

    def reduce(self, func, initializer=no_init):
        from lazyer.ops import Reduce
        return Reduce(self, func, initializer)

    def unique(self, func=true):
        from lazyer.ops import Unique
        return Unique(self, func)

    def chain(self, *nodes):
        from lazyer.ops import Chain
        return Chain(self, *nodes)

    def filter(self, predicate):
        from lazyer.ops import Filter
        return Filter(self, predicate)

    def take(self, n):
        from lazyer.ops import Take
        return Take(self, n)

    def skip(self, n):
        from lazyer.ops import Skip
        return Skip(self, n)

    def join(self, node, outer='none'):
        from lazyer.ops import Join
        return Join(self, node, outer)

    def union(self, *nodes, **kwargs):
        if not kwargs.get('all', False):
            nodes = (node.unique() for node in nodes)
        return self.chain(*nodes)

    def intersect(self, *nodes):
        from lazyer.ops import Intersect
        return Intersect(self, *nodes)

    def differ(self, *nodes):
        from lazyer.ops import Differ
        return Differ(self, *nodes)

    def sort(self):
        from lazyer.ops import Sort
        return Sort(self)

    def reverse(self):
        from lazyer.ops import Reverse
        return Reverse(self)

    def partition(self, n, func):
        from lazyer.ops import Partition
        partition = Partition(self, n, func)
        return partition.forwards

    def inspect(self, func=print_pair, interval=1):
        from lazyer.ops import Inspect
        return Inspect(self, func, interval)

    def collect(self):
        from lazyer.utils import append
        return self.reduce(append, initializer=list).transform(tuple)

    def iterate(self):
        from lazyer.ops import Iterate
        return Iterate(self)

    def get(self, collection=dict):
        if collection is dict:
            return {k: v for k, v in self}
        else:
            return collection(v for _, v in self)

    def write(self, filename, encode=make_flattened_str):
        with open(filename, 'w') as f:
            for kv in self:
                f.write(encode(kv) + '\n')
