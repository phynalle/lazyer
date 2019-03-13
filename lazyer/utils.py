def includes(keys):
    keys = set(keys)
    def func(key, val):
        return key in keys
    return func


def excludes(keys):
    keys = set(keys)
    def func(key, val):
        return key not in keys
    return func


def identity(x):
    return x


def value_is_not_none(key, val):
    return val is not None


def first(a, b):
    return a


def second(a, b):
    return b


def select_key(kv):
    k, _ = kv
    return k


def select_value(kv):
    _, v = kv
    return v


def swap(tup):
    a, b = tup
    return b, a


def encode(val):
    if isinstance(val, (tuple, set, list)):
        return ' '.join(encode(e) for e in val)
    return str(val)

def true(*args):
    return True

def false(*args):
    return False
