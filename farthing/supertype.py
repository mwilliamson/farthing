import abc
import inspect

from .types import union, is_list, List, is_dict, Dict, any_, Class, describe


def common_super_type(types):
    types = set(filter(None, types))
    if not types:
        return None
    
    _discard_empty_collection_types(is_list, List(any_), types)
    _discard_empty_collection_types(is_dict, Dict(any_, any_), types)

    if all(isinstance(type_, Class) for type_ in types):
        bases = set(
            base
            for type_ in types
            for base in inspect.getmro(type_.type)
            if getattr(base, "__metaclass__", None) == abc.ABCMeta
        )
        concrete_types = [type_.type for type_ in types]
        complete_bases = list(filter(lambda base: _is_complete_base(concrete_types, base), bases))
        if complete_bases:
            return describe(complete_bases[0])

    return union(types)


def _discard_empty_collection_types(is_collection, empty_collection_type, types):
    if sum(map(is_collection, types)) > 1:
        types.discard(empty_collection_type)

def _is_complete_base(types, base):
    return all(issubclass(type_, base) for type_ in types)
