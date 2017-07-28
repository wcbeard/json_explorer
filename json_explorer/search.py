import re


def mk_match(key, regex=None, ignore_case=None):
    if not regex:
        return lambda str: key == str
    else:
        flag = re.IGNORECASE if ignore_case else 0
        pat = re.compile(key, flags=flag)
        return lambda s: pat.search(s)


def key_search(d, key, regex=False, sep=None, ignore_case=False):
    """Return path of nested dict keys of first match.
    """
    match = mk_match(key, regex=regex, ignore_case=ignore_case)

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


def key_search_all(d, key, regex=False, ignore_case=False):
    """Return path of nested dict keys of first match.
    """
    match = mk_match(key, regex=regex, ignore_case=ignore_case)

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
