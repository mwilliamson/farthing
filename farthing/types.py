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


class Type(object):
    pass

@cobble.data
class Class(Type):
    module = cobble.field()
    name = cobble.field()
    type = cobble.field()

@cobble.data
class Union(Type):
    values = cobble.field()

@cobble.data
class Any(Type):
    pass
any_ = Any()

@cobble.data
class List(Type):
    element = cobble.field()
list_ = List

@cobble.data
class Iterable(Type):
    element = cobble.field()
iterable = Iterable

@cobble.data
class Dict(Type):
    key = cobble.field()
    value = cobble.field()
dict_ = Dict

@cobble.data
class Tuple(Type):
    elements = cobble.field()
tuple_ = Tuple

@cobble.data
class CallableRef(Type):
    func_index = cobble.field()
callable_ref = CallableRef

@cobble.data
class Callable(Type):
    args = cobble.field()
    returns = cobble.field()
callable_ = Callable

def is_class(type_):
    return isinstance(type_, Class)

def is_list(type_):
    return isinstance(type_, List)


def is_dict(type_):
    return isinstance(type_, Dict)


def is_callable_ref(type_):
    return isinstance(type_, CallableRef)
