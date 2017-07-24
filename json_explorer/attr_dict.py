class AttrDict_(dict):
    """Dict with attribute access of keys.
    >>> d = AttrDict(k='v')
    >>> d.k
    'v'

    Pass _show_only_keys=False as kw to show rest of dict
    attributes.
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict_, self).__init__(*args, **kwargs)
        self.__dict__ = self


class AttrDict(AttrDict_):
    def __dir__(self):
        return list(self)


def recurse_attr(d, dict_func=AttrDict):
    if isinstance(d, dict):
        return dict_func((k, recurse_attr(v, dict_func=dict_func)) for k, v in d.items())
    if isinstance(d, list):
        return [recurse_attr(e, dict_func=dict_func) for e in d]
    return d


# def attr_dict(*args, **kwargs):
#     d = AttrDict(*args, **kwargs)
#     show_only_keys = d.pop('_show_only_keys', True)

#     if show_only_keys:
#         return d
#     return AttrDict_(d)
