import cobble


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


@cobble.data
class Class(object):
    module = cobble.field()
    name = cobble.field()
    type = cobble.field()

@cobble.data
class Union(object):
    values = cobble.field()

@cobble.data
class Any(object):
    pass
any_ = Any()

@cobble.data
class List(object):
    element = cobble.field()
list_ = List

@cobble.data
class Dict(object):
    key = cobble.field()
    value = cobble.field()
dict_ = Dict

@cobble.data
class CallableRef(object):
    func_index = cobble.field()
callable_ref = CallableRef

@cobble.data
class Callable(object):
    args = cobble.field()
    returns = cobble.field()
callable_ = Callable

def is_list(type_):
    return isinstance(type_, List)


def is_dict(type_):
    return isinstance(type_, Dict)


def is_callable_ref(type_):
    return isinstance(type_, CallableRef)
