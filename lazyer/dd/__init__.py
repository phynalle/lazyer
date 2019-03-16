from __future__ import division
from collections import Iterable
from functools import partial
from six import viewitems
import operator


class Here(object):
    pass

here = Here


def bind_here_to_obj(h, obj):
    if h is here:
        return obj
    return h


def make(t, d):
    if isinstance(t, Template):
        return t.make(d)
    return t


def _t(data):
    if isinstance(data, basestring):
        return DataAccessTemplate(data)
    if isinstance(data, Template):
        return data
    return NonDataAccessTemplate(data)


_ = _t


def define(struct):
    if isinstance(struct, tuple):
        struct = tuple(define(item) for item in struct)
    if isinstance(struct, list):
        struct = [define(item) for item in struct]
    if isinstance(struct, set):
        struct = {define(item) for item in struct}
    if isinstance(struct, dict):
        struct = {k: define(item) for k, item in viewitems(struct)}
    return _t(struct)


def apply_(func, *args, **kwargs):
    return ApplyTemplate(func, *args, **kwargs)


def override_unary(op):
    def func(template):
        return apply_(op, template)
    return func


def override_binary(op):
    def func(template, other):
        return apply_(op, template, other)
    return func


class Template(object):
    def make(self, data):
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

    def nonzero(self, data):
        return bool(self.make(data))


class DataAccessTemplate(Template):
    def __init__(self, key):
        self.keys = key.split('.')

    def make(self, data):
        for key in self.keys:
            data = data[key]
        return data


class NonDataAccessTemplate(Template):
    def __init__(self, template):
        self.template = template

    def make(self, data):
        template = self.template
        if isinstance(template, tuple):
            return tuple(make(item, data) for item in template)
        if isinstance(data, list):
            return [make(item, data) for item in template]
        if isinstance(data, set):
            return {make(item, data) for item in template}
        if isinstance(data, dict):
            return {k: make(item, data) for k, item in viewitems(template)}
        return make(template, data)


class ApplyTemplate(Template):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def make(self, data):
        args = [make(arg, data) for arg in self.args]
        kwargs = {k: make(arg, data) for k, w in viewitems(self.kwargs)}
        return self.func(*args, **kwargs)
