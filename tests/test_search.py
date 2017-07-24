from json_explorer.search import key_search, key_search_all


def test_key_search():
    d = {
        'a': {
            'b': [1, 2, 3],
            'c': {'d': 1, 'e': 2, 'f': 3},
        },
        'g': 1,
        'h': 'ijklmnop',
        'q': [{'r': [{'s': 5}]}],
    }

    assert key_search(d, 'a', regex=False) == ['a']
    assert key_search(d, 'b', regex=False) == ['a', 'b']
    assert key_search(d, 'e', regex=False) == ['a', 'c', 'e']
    assert key_search(d, 's', regex=False) == ['q', 'r', 's']

    # Sep
    assert key_search(d, 's', regex=False, sep='/') == 'q/r/s'

    # regex
    assert key_search(d, r'[exyz]', regex=True, sep='') == 'ace'


def test_key_search_all():
    d = {
        'a': {
            'b': [1, 2, 3],
            'c': {'d': 1, 'e': 2, 'f': 3},
        },
        'gs': 1,
        'h': 'ijklmnop',
        'q': [{'rs': [{'s': 5}]}],
        't': ['u', 'v'],

    }
    assert set(key_search_all(d, '[aeiou]', regex=1)) == {'a', 'e'}
    assert set(key_search_all(d, '[a-z]s', regex=1)) == {'gs', 'rs'}
    assert not key_search_all(d, 'l')
    assert not key_search_all(d, 'u', regex=True), "Shouldn't find array elements"
