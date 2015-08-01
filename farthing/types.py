import collections


def describe(type_):
    return Class(type_.__module__, type_.__name__, type_)


def union(values):
    values = frozenset(values)
    if len(values) == 1:
        return next(iter(values))
    else:
        return Union(values)


Class = collections.namedtuple("Class", ["module", "name", "type"])
Union = collections.namedtuple("Union", ["values"])
Any = collections.namedtuple("Any", [])
any_ = Any()
list_ = List = collections.namedtuple("List", ["element"])
dict_ = Dict = collections.namedtuple("Dict", ["key", "value"])


def is_list(type_):
    return isinstance(type_, List)


def is_dict(type_):
    return isinstance(type_, Dict)
