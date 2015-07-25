from .types import union


def common_super_type(types):
    types = set(types)
    if len(types) == 1:
        return next(iter(types))
    else:
        return union(types)
