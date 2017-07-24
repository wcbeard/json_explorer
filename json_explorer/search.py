import re


def key_search(d, key, regex=False, sep=None):
    """Return path of nested dict keys of first match.
    """
    if not regex:
        match = lambda str: key == str
    else:
        match = lambda s, pat=re.compile(key): pat.search(s)

    def search(d, trail=None):
        if isinstance(d, dict):
            matches = [k for k in d if match(k)]
            if matches:
                return trail + matches[:1]
            submatches = filter(None, (search(v, trail=trail + [k]) for k, v in d.items()))

            if submatches:
                return submatches[0]
            return []
        elif isinstance(d, list):
            iter_matches = filter(
                None, [search(e, trail=trail) for e in d
                       if isinstance(e, (dict, list))])
            if iter_matches:
                return iter_matches[0]

    path = search(d, trail=[])
    if sep is not None:
        return sep.join(path)
    return path


def key_search_all(d, key, regex=False):
    """Return path of nested dict keys of first match.
    """
    if not regex:
        match = lambda str: key == str
    else:
        match = lambda s, pat=re.compile(key): pat.search(s)
    retmatch = lambda x: [x] if match(x) else []

    def search(d, res=None):  # => [str]
        if isinstance(d, dict):
            matches = [e for k, v in d.items()
                       for e in (retmatch(k) + search(v, res=None))]
            return matches
        elif isinstance(d, list):
            iter_matches = filter(
                None, [e2 for e1 in d
                       if isinstance(e1, (dict, list))
                       for e2 in search(e1, res=res)])
            return iter_matches
        return []

    return search(d, res=[])


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
