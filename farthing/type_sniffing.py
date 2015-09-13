from . import types
from .supertype import common_super_type


def describe_type_of(value):
    type_ = type(value)
    if issubclass(type_, list):
        return _describe_list(value)
    elif issubclass(type_, dict):
        return _describe_dict(value)
    elif issubclass(type_, tuple):
        return _describe_tuple(value)
    elif callable(value) and hasattr(value, "_farthing_func_index"):
        return types.callable_ref(value._farthing_func_index)
    else:
        return types.describe(type_)


def _describe_list(value):
    return types.List(_describe_values(value))
    

def _describe_dict(value):
    if len(value) == 0:
        key_type = value_type = types.any_
    else:
        key_type, value_type = map(_describe_values, zip(*value.items()))
    return types.Dict(key_type, value_type)


def _describe_tuple(value):
    return types.Tuple(tuple(map(describe_type_of, value)))


def _describe_values(values):
    if len(values) == 0:
        return types.any_
    else:
        return common_super_type(map(describe_type_of, values))
