import collections


def describe(type_):
    return Class(type_.__module__, type_.__name__, type_)


def union(values):
    union_values = set()
    
    for value in values:
        if isinstance(value, Union):
            union_values |= value.values
        else:
            union_values.add(value)
    
    if len(union_values) == 1:
        return next(iter(union_values))
    else:
        return Union(frozenset(union_values))


Class = collections.namedtuple("Class", ["module", "name", "type"])
Union = collections.namedtuple("Union", ["values"])
Any = collections.namedtuple("Any", [])
any_ = Any()
list_ = List = collections.namedtuple("List", ["element"])
dict_ = Dict = collections.namedtuple("Dict", ["key", "value"])
callable_ref = CallableRef = collections.namedtuple("CallableRef", ["func_index"])

def is_list(type_):
    return isinstance(type_, List)


def is_dict(type_):
    return isinstance(type_, Dict)
