from functools import wraps


def call_packed(f):
    @wraps(f)
    def wrapper(*args):
        return f(args)
    return wrap


def call_unpacked(f):
    @wraps(f)
    def wrapper(args):
        return f(*args)
    return wrap

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


def swap(a, b):
    return b, a


def select_key(kv):
    # return kv[0]
    return call_unpacked(first)(kv)


def select_value(kv):
    # return kv[1]
    return call_unpacked(second)(kv)


def true(*args):
    return True


def false(*args):
    return False


def encode(val):
    if isinstance(val, (tuple, set, list)):
        return ' '.join(encode(e) for e in val)
    return str(val)
