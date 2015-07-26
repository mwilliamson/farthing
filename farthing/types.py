import collections


def describe(type_):
    return Class(type_.__module__, type_.__name__)


def union(values):
    return Union(set(values))


Class = collections.namedtuple("Class", ["module", "name"])
Union = collections.namedtuple("Union", ["values"])
