def includes(keys):
    def func(key, val):
        return key in keys


def excludes(keys):
    def func(key, val):
        return key not in keys

def encode(val):
    if isinstance(val, (tuple, set, list)):
        return ' '.join(encode(e) for e in val)
    return str(val)
