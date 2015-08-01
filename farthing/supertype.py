from .types import union, is_list, List, any_


def common_super_type(types):
    types = set(types)
    if len(types) == 1:
        return next(iter(types))
    elif all(map(is_list, types)):
        types.remove(List(any_))
        if len(types) == 1:
            return next(iter(types))

    return union(types)
