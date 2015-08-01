import collections


def describe(type_):
    return Class(type_.__module__, type_.__name__)


def union(values):
    return Union(frozenset(values))


Class = collections.namedtuple("Class", ["module", "name"])
Union = collections.namedtuple("Union", ["values"])
Any = collections.namedtuple("Any", [])
any_ = Any()
list_ = List = collections.namedtuple("List", ["element"])
dict_ = Dict = collections.namedtuple("Dict", ["key", "value"])


def is_list(type_):
    return isinstance(type_, List)


def is_dict(type_):
    return isinstance(type_, Dict)
