from lazyer.dd import tdl


def define(template_string):
    return tdl.parse(template_string)


_t = define
