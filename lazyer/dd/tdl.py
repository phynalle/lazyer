import os
import operator
from lark import Lark, Transformer
from lazyer.dd.template import DataAccessTemplate


def load_parser():
    filename = os.path.join(os.path.dirname(__file__), 'tdl.lark')
    with open(filename) as f:
        return Lark(f.read(), start='keyword', parser='earley')


PARSER = load_parser()


def in_(a, b):
    return operator.contains(b, a)


def not_in(a, b):
    return not in_(a, b)


ops = {
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '>=': operator.ge,
    '<=': operator.le,
    '!=': operator.ne,
    'in': in_,
    'notin': not_in,
    'is': operator.is_,
    'isnot': operator.is_not,
    'not': operator.not_,
}


def parse(s):
    return parse_keyword(PARSER.parse(s))


def parse_expr(tree, parent_keyword=None):
    assert tree.data == 'expr'
    matches = tree.children
    if matches[0].data == 'number':
        number = matches[0].children[0].value
        return int(number)
    elif matches[0].data == 'string':
        s = matches[0].children[0].value
        return s[1:-1]
    elif matches[0].data == 'keyword':
        return parse_keyword(matches[0], parent_keyword=parent_keyword)


def parse_keyword(tree, parent_keyword=None):
    assert tree.data == 'keyword'
    idx = 0
    children = tree.children

    parent = None
    if children[idx].data == 'keyword':
        parent = parse_keyword(children[idx], parent_keyword=parent_keyword)
        idx += 1
    keyword = children[idx].children[0].value
    idx += 1
    try:
        filter_ = parse_cond(children[idx], parent_keyword=parent)
    except IndexError:
        filter_ = None
    return DataAccessTemplate(keyword, parent=parent, filter_=filter_)


def parse_cond(tree, parent_keyword=None):
    assert tree.data in ['unary_cond', 'binary_cond']
    if tree.data == 'unary_cond':
        op = parse_op(tree.children[0])
        first = parse_expr(tree.children[1], parent_keyword=parent_keyword)
        return op(first)
    else:
        op = parse_op(tree.children[1])
        first = parse_expr(tree.children[0], parent_keyword=parent_keyword)
        second = parse_expr(tree.children[2], parent_keyword=parent_keyword)
        return op(first, second)


def parse_op(token):
    # "<"|">"|"=="|">="|"<="|"<>"|"!="|"in"|"not" "in"|"is"|"is" "not"
    assert token.type in ['UNARY_OP', 'BINARY_OP']
    return ops[token.value]
