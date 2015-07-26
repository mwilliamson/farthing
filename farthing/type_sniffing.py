from . import types
from .supertype import common_super_type


def describe_type_of(value):
    type_ = type(value)
    if issubclass(type_, list):
        if len(value) == 0:
            return types.List(types.any_)
        else:
            return types.List(common_super_type(map(describe_type_of, value)))
    else:
        return types.describe(type_)
