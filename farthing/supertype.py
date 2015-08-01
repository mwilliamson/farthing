from .types import union, is_list, List, is_dict, Dict, any_


def common_super_type(types):
    types = set(types)
    
    _discard_empty_collection_types(is_list, List(any_), types)
    _discard_empty_collection_types(is_dict, Dict(any_, any_), types)

    return union(types)


def _discard_empty_collection_types(is_collection, empty_collection_type, types):
    if sum(map(is_collection, types)) > 1:
        types.discard(empty_collection_type)
