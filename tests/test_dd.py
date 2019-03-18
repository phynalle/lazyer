import pytest
from lazyer.dd import _t, else_, make, select

def test_template_access():
    mock = {
        'hello': 'world',
        'what': {
            'studio': 'awesome!',
            'the': 'heck',
        },
    }
    assert _t('hello').make(mock) == 'world'
    assert _t('what.studio').make(mock) == 'awesome!'
    assert _t('what.the').make(mock) == 'heck'
    with pytest.raises(KeyError):
        _t('nothing.in.the.data').make(mock)


def test_template_list_condition():
    mock = {'items': [
        {'id': 0, 'prototype_id': 'a'},
        {'id': 1, 'prototype_id': 'a'},
        {'id': 2, 'prototype_id': 'b'},
        {'id': 3, 'prototype_id': 'c'},
        {'id': 4, 'prototype_id': 'a'},
        {'id': 5, 'prototype_id': 'b'},
        {'id': 6, 'prototype_id': 'c'},
    ]}
    assert _t('items[id > #3].id').make(mock) == [4, 5, 6]


def test_select():
    selector = select('id', {
        'a': ('a', 'b'),
        'b': 'b',
        'c': 'c',
        else_: 'd',
    })

    mock1 = {'id': 'a', 'a': 'A', 'b': 'B', 'c': 'C'}
    assert selector(mock1) == ('A', 'B')
    mock2 = {'id': 'b', 'a': 'A', 'b': 'B', 'c': 'C'}
    assert selector(mock2) == 'B'
    mock3 = {'id': 'c', 'a': 'A', 'b': 'B', 'c': 'C'}
    assert selector(mock3) == 'C'
