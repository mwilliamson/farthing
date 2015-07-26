import collections


def describe_type_of(value):
    type_ = type(value)
    return describe(type_)


def describe(type_):
    return Class(type_.__module__, type_.__name__)


def union(values):
    return Union(set(values))


Class = collections.namedtuple("Class", ["module", "name"])
Union = collections.namedtuple("Union", ["values"])
