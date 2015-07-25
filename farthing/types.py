import collections


def describe(type_):
    return type_.__module__, type_.__name__


def union(values):
    return Union(set(values))


Union = collections.namedtuple("Union", ["values"])
