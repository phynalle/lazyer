from builtins import zip
import pytest
from lazyer.exceptions import DuplicatedKey
from lazyer.ops import Sink
from lazyer.utils import swap

def source_range(*args):
    return Sink(range(*args))


def source_mapped(first, second, n):
    from operator import add
    from itertools import islice, cycle
    keys = islice(cycle(first), n)
    vals = islice(cycle(second), n)
    return Sink(zip(keys, vals)).map()


def source_abc_1234():
    return source_mapped('abc', (1, 2, 3, 4), 12)


def test_source():
    for i, pair in enumerate(source_range(10)):
        assert pair == (None, i)


def test_map():
    s = Sink(zip(range(100), range(100))).map(lambda v: (v[0], v[1] + 1))
    for k, v in s:
        assert k + 1 == v


def test_default_map():
    s = Sink(zip(map(str, range(100)), range(100))).map()
    for k, v in s:
        assert k == str(v)


def test_remap():
    expected = {'a': 0, 'b': 1, 'c': 2}
    s = Sink(zip(range(3), 'abc')).map()
    assert s.remap(swap).get() == expected


def test_unmap():
    s = Sink([('a', 1), ('b', 2), ('c', 3)]).map()
    expected = [('a', 1), ('b', 2), ('c', 3)]
    assert s.unmap().get(list) == expected


def test_tee():
    expected = list(range(10))
    for cloned in source_range(10).tee(3):
        assert cloned.get(list) == expected


def test_transform():
    expected = list(map(str, range(10)))
    assert source_range(10).transform(str).get(list) == expected


def test_reduce():
    from operator import add
    expected = {'a': 10, 'b': 10, 'c': 10}
    assert source_abc_1234().reduce(add).get() == expected


def test_unique():
    expected = {'a': 1, 'b': 2, 'c': 3}
    assert source_abc_1234().unique().get() == expected


def test_chain():
    chars = list('abc')
    nums = list(range(1, 4))
    marks = list('!@#')
    expected = chars + nums + marks
    assert Sink(chars).chain(Sink(nums), Sink(marks)).get(list) == expected


def test_filter():
    expected = [0, 2, 4, 6, 8]
    assert source_range(10).filter(lambda x: x % 2 == 0).get(list) == expected


def test_take():
    expected = [0, 1, 2]
    assert source_range(10).take(3).get(list) == expected


def test_skip():
    expected = [7, 8, 9]
    assert source_range(10).skip(7).get(list) == expected


def test_join_inner():
    a = source_mapped('abc', (1, 2, 3, 4), 4)
    b = source_mapped('bda', (5, 6, 7, 8), 4)
    expected = [('b', (2, 5)), ('a', (1, 7)), ('a', (4, 7)), ('b', (2, 8))]
    assert a.join(b).unmap().get(list) == expected


def test_join_left_outer():
    a = source_mapped('abc', (1, 2, 3, 4), 4)
    b = source_mapped('bda', (5, 6, 7, 8), 4)
    expected = [
            ('b', (2, 5)),
            ('a', (1, 7)),
            ('a', (4, 7)),
            ('b', (2, 8)),
            ('c', (3, None))]
    assert a.join(b).set_left().unmap().get(list) == expected


def test_join_right_outer():
    a = source_mapped('abc', (1, 2, 3, 4), 4)
    b = source_mapped('bda', (5, 6, 7, 8), 4)
    expected = [
            ('b', (2, 5)),
            ('d', (None, 6)),
            ('a', (1, 7)),
            ('a', (4, 7)),
            ('b', (2, 8))]
    assert a.join(b).set_right().unmap().get(list) == expected


def test_join_full():
    a = source_mapped('abc', (1, 2, 3, 4), 4)
    b = source_mapped('bda', (5, 6, 7, 8), 4)
    expected = [
            ('b', (2, 5)),
            ('d', (None, 6)),
            ('a', (1, 7)),
            ('a', (4, 7)),
            ('b', (2, 8)),
            ('c', (3, None))]
    assert a.join(b).set_full().unmap().get(list) == expected


def test_union():
    a = source_mapped('aba', (1, 2, 3), 3)
    b = source_mapped('bab', (4, 5, 6), 3)
    expected = {'a': [1, 3, 5], 'b': [2, 4, 6]}
    a.union(b).reduce(lambda a, b: a + [b], []).get() == expected


def test_intersect():
    a = source_mapped('aba', (1, 2, 3), 3).unique()
    b = source_mapped('bab', (4, 5, 6), 3).unique()
    expected = {'a': (1, 5), 'b': (2, 4)}
    assert a.intersect(b).get() == expected


def test_intersect_duplicated_key():
    a = source_mapped('aba', (1, 2, 3), 3)
    b = source_mapped('bab', (4, 5, 6), 3)
    with pytest.raises(DuplicatedKey):
        a.intersect(b).get()


def test_differ():
    a = source_mapped('abc', (1, 2, 3, 4), 12)
    b = source_mapped('b', (4, ), 1)
    c = source_mapped('c', (4, ), 1)
    expected = [('a', 1), ('a', 4), ('a', 3), ('a', 2)]
    assert a.differ(b, c).unmap().get(list) == expected


def test_iterate():
    a = source_mapped('a', ((1, 2, 3), ), 1)
    expected = [('a', 1), ('a', 2), ('a', 3)]
    assert a.iterate().unmap().get(list) == expected


def test_collect():
    a = source_mapped('ab', (1, 1, 2, 2, 3, 3), 6)
    expected = {
        'a': (1, 2, 3),
        'b': (1, 2, 3),
    }
    assert a.collect().get() == expected


def test_sort():
    import random
    vals = [random.choice(range(1000)) for _ in range(99)]
    expected = {k: tuple(sorted(vals[i] for i in range(j, 99, 3))) for j, k in enumerate('abc')}
    expected = {}
    for i, k in enumerate('abc'):
        expected[k] = tuple(sorted(vals[j] for j in range(i, 99, 3)))
    assert source_mapped('abc', vals, 99).sort().collect().get() == expected
