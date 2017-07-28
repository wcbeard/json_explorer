class AttrDict_(dict):
    """Dict with attribute access of keys.
    >>> d = AttrDict(k='v')
    >>> d.k
    'v'
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


def attr_dict(d, only_keys=True):
    which_dict = AttrDict if only_keys else AttrDict_
    return recurse_attr(d, dict_func=which_dict)
    # a = AttrDict(d)
    # show_only_keys = d.pop('_show_only_keys', True)

    # if show_only_keys:
    #     return d
    # return AttrDict_(d)
