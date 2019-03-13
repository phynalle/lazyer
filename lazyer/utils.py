def includes(keys):
    def func(key, val):
        return key in keys


def excludes(keys):
    def func(key, val):
        return key not in keys
