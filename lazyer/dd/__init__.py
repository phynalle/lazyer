from functools import wraps
from six import viewitems

from lazyer.dd import tdl
from lazyer.dd.template import FunctionTemplate, make, SkeletonTemplate, Template
from lazyer.exceptions import EmptyTemplate


def define_keyword_template(template_string):
    return tdl.parse(template_string)


_k = define_keyword_template


def define_template(*args):
    if not args:
        raise EmptyTemplate

    templates = []
    for arg in args:
        if isinstance(arg, str):
            arg = define_keyword_template(arg)
        elif isinstance(arg, (tuple, list)):
            arg = define_template(*arg)
        elif isinstance(arg, Template):
            pass
        elif callable(arg):
            arg = FunctionTemplate(arg)
        templates.append(arg)
    if len(templates) == 1:
        return templates[0]
    return SkeletonTemplate(templates)


_t = define_template


class SelectElse(object):
    pass


else_ = SelectElse


def select(key, switch):
    key_tpl = _t(key)
    switch = {k: _t(tpl) for k, tpl in viewitems(switch)}

    @wraps(select)
    def wrapper(data, ctx={}):
        k = key_tpl(data, ctx)
        if k in switch:
            return make(switch[k], data, ctx)
        if else_ in switch:
            return make(switch[else_], data, ctx)
        return None
    return _t(wrapper)
