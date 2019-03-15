from collections import defaultdict, OrderedDict
from six import viewitems, viewkeys
from builtins import zip
from lazyer import Node, Pair, no_init
from lazyer.exceptions import DuplicatedKey, NodeException

class Join(Node):
    def __init__(self, left, right, mode):
        self.left = left
        self.right = right
        self.left_init = no_init
        self.right_init = no_init
        self.left_is_consumed = False
        self.left_vals = OrderedDict()
        self.gen_pair = iter(self.join_pair())
        if mode == 'inner':
            pass
        elif mode == 'left_outer':
            self.left_outer()
        elif mode == 'right_outer':
            self.right_outer()
        elif mode == 'full':
            self.full()
        else:
            raise NodeException('Unsupported mode')

    def left_outer(self):
        self.right_init = None
        return self

    def right_outer(self):
        self.left_init = None
        return self

    def full(self):
        self.set_left_outer()
        self.set_right_outer()
        return self

    def _consume_left(self):
        if self.left_is_consumed:
            return
        for key, val in self.left:
            self.left_vals.setdefault(key, []).append(val)
        self.left_is_counsumed = True

    def join_pair(self):
        # reference link:
        # https://github.com/pytoolz/toolz/blob/2a6ef533854bd0bb383889071059f7ca3690c005/toolz/itertoolz.py#L812https://github.com/pytoolz/toolz/blob/2a6ef533854bd0bb383889071059f7ca3690c005/toolz/itertoolz.py#L812
        # NOTE: joins_left_outer is used for the optimization.
        joins_left_outer = self.right_init is not no_init
        if joins_left_outer:
            right_keys = set()
        for key, right_val in self.right:
            if joins_left_outer:
                right_keys.add(key)
            try:
                left_vals = self.left_vals[key]
                for left_val in left_vals:
                    yield Pair(key, (left_val, right_val))
            except KeyError:
                if self.left_init is no_init:
                    yield Pair(key, (self.left_init, right_val))
        if joins_left_outer:
            for key, left_vals in viewitems(self.left_vals):
                if key in right_keys:
                    continue
                for left_val in left_vals:
                    yield Pair(key, (left_vals, self.right_init))

    def next_pair(self):
        self._consume_left()
        return next(self.gen_pair)
