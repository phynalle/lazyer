from __future__ import division
import operator
from six import viewitems

class Here(object):
    pass


here = Here


def bind_here_to_obj(h, obj):
    if h is here:
        return obj
    return h


def apply_(func, *args, **kwargs):
    return ApplyTemplate(func, *args, **kwargs)


def make(t, d, ctx={}):
    if isinstance(t, Template):
        return t.make(d, ctx)
    return t


def override_unary(op):
    def func(template):
        return apply_(op, template)
    return func


def override_binary(op):
    def func(template, other):
        return apply_(op, template, other)
    return func


class Template(object):
    def __call__(self, data, ctx={}):
        return self.make(data, ctx)

    def make(self, data, ctx={}):
        raise NotImplemented

    def bind(self, func, *args, **kwargs):
        args = [bind_here_to_obj(arg, self) for arg in args]
        kwargs = {k: bind_here_to_obj(arg, self) for k, arg in viewitems(kwargs)}
        return apply_(func, *args, **kwargs)

    __lt__ = override_binary(operator.le)
    __gt__ = override_binary(operator.gt)
    __le__ = override_binary(operator.le)
    __ge__ = override_binary(operator.ge)
    __eq__ = override_binary(operator.eq)
    __ne__ = override_binary(operator.ne)
    __sub__ = override_binary(operator.sub)
    __add__ = override_binary(operator.add)
    __mul__ = override_binary(operator.mul)
    __truediv__ = override_binary(operator.truediv)
    __floordiv__ = override_binary(operator.floordiv)
    __mod__ = override_binary(operator.mod)
    __pow__ = override_binary(operator.pow)
    __rshift__ = override_binary(operator.rshift)
    __lshift__ = override_binary(operator.lshift)
    __and__ = override_binary(operator.and_)
    __or__ = override_binary(operator.or_)
    __xor__ = override_binary(operator.xor)
    __neg__ = override_unary(operator.neg)
    __pos__ = override_unary(operator.pos)
    __invert__ = override_unary(operator.invert)
    __not__ = override_unary(operator.not_)
    __getitem__ = override_binary(operator.getitem)
    __contains__ = override_binary(operator.contains)


class DataAccessTemplate(Template):
    def __init__(self, key, parent=None, filter_=None):
        self.key = key
        self.parent = parent
        self.filter = filter_

    def make(self, data, ctx={}):
        containers = (tuple, list, set)
        if self.parent is not None:
            data = make(self.parent, data, ctx)

        data_type = type(data)
        assert issubclass(data_type, (dict, *containers))
        if issubclass(data_type, containers):
            val = data_type(item[self.key] for item in data)
        else:
            val = data[self.key]

        val_type = type(val)
        if issubclass(val_type, containers):
            def generate():
                for item in val:
                    if self.filter is None or make(self.filter, item, ctx):
                        yield item
            val = val_type(generate())
        return val


class ApplyTemplate(Template):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def make(self, data, ctx={}):
        args = [make(arg, data, ctx) for arg in self.args]
        kwargs = {k: make(arg, data, ctx) for k, w in viewitems(self.kwargs)}
        return self.func(*args, **kwargs)


class VariableTemplate(Template):
    def __init__(self, var):
        self.var = var

    def make(self, data, ctx={}):
        return ctx[self.var]
