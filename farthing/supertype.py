import abc
import inspect

from .types import union, is_list, List, is_dict, Dict, any_, is_class, describe


def common_super_type(types):
    types = set(filter(None, types))
    if not types:
        return None
    
    if len(types) == 1:
        return union(types)
    
    _discard_empty_collection_types(is_list, List(any_), types)
    _discard_empty_collection_types(is_dict, Dict(any_, any_), types)
    
    complete_base = _find_complete_base(types)
    if complete_base is not None:
        return complete_base
    
    if len(types) > 3:
        base = _find_common_base_class(types)
        if base is not None:
            return describe(base)
    
    if all(map(is_list, types)):
        return List(common_super_type(list_type.element for list_type in types))

    return union(types)


def _discard_empty_collection_types(is_collection, empty_collection_type, types):
    if sum(map(is_collection, types)) > 1:
        types.discard(empty_collection_type)

def _find_complete_base(types):
    if all(map(is_class, types)):
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


def _find_common_base_class(types):
    if all(map(is_class, types)):
        concrete_types = [type_.type for type_ in types]
        bases_for_each_type = [
            inspect.getmro(type_)
            for type_ in concrete_types
        ]
        common_bases = set(bases_for_each_type[0]).intersection(*bases_for_each_type[1:])
        # Use MRO to get the most specific common base
        ordered_common_bases = [
            base
            for bases in bases_for_each_type
            for base in bases
            if base in common_bases
        ]
        if ordered_common_bases:
            return next(iter(ordered_common_bases))
    return object
    

def _is_complete_base(types, base):
    return all(
        issubclass(type_, base) and _same_public_attributes(type_, base)
        for type_ in types
    )

def _same_public_attributes(first, second):
    return _public_attributes(first) == _public_attributes(second)

def _public_attributes(type_):
    return tuple(filter(_is_public, dir(type_)))

def _is_public(name):
    if name.startswith("__") and name.endswith("__"):
        return True
    elif name.startswith("_"):
        return False
    else:
        return True
