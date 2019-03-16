from lazyer.dd import tdl
from lazyer.dd.template import SkeletonTemplate
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
        templates.append(arg)
    if len(templates) == 1:
        return templates[0]
    return SkeletonTemplate(templates)


_t = define_template
