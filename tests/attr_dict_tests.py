from __future__ import print_function, division
from ..attr_dict import AttrDict_, AttrDict, recurse_attr
from pytest import raises

d = {
    'a': {
        'b': [1, 2, 3],
        'c': {'d': 1, 'e': 2, 'f': 3},
    },
    'g': 1,
    'h': 'ijklmnop',
}


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b)


sdir = lambda x: set(dir(x))


def test_recurse_attr():
    d2 = recurse_attr(d)

    assert d2.a.c == {'d': 1, 'e': 2, 'f': 3}

    # Doesn't modify original
    with raises(AttributeError, message="'dict' object has no attribute 'a'"):
        d.a.c

    assert d2.g == 1
    assert isinstance(d2.h, str)


def test_dir():
    # Only keys as attrs
    d2 = recurse_attr(d, dict_func=AttrDict)
    assert sdir(d2) == set(d)

    # Extra dir attrs
    d3 = recurse_attr(d, dict_func=AttrDict_)
    assert jaccard(sdir(d3), (sdir(dict) | set(d))) > .9, (
        "Dir shouldn't have too much extra stuff")

    assert not (sdir(dict) | set(d)) - \
        sdir(d3), "dir needs keys and dict attrs"

# test_recurse_attr()
# test_dir()
