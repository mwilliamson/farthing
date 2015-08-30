import collections

from .ast_util import func_args, find_return_annotation_location
from .locations import create_location, Location
from .iterables import grouped
from .pep484 import format_type
from .guess import guess_types


def annotate(all_entries):
    insertions = []
    for location, func, type_ in guess_types(all_entries):
        insertions += _annotate_function(location.path, func, type_)
    
    for path, insertions_for_file in grouped(insertions, lambda insertion: insertion.location.path):
        _insert_strings(path, insertions_for_file)


def _annotate_function(path, func, type_):
    # TODO: investigate libraries that will allow editing of nodes while preserving concrete syntax
    insertions = []
    
    for (arg_name, arg_type), arg in zip(type_.args, func_args(func)):
        if arg.annotation is None:
            location = create_location(path, arg.lineno, arg.col_offset + len(arg.arg))
            insertions.append(_arg_annotation_insertion(location, arg_type))
    
    return_type_annotation = _return_type_annotation(path, func, type_.returns)
    if return_type_annotation is not None:
        insertions.append(return_type_annotation)
    
    return insertions
    

def _return_type_annotation(path, func, return_type):
    if return_type is None or func.returns is not None:
        return None
    
    with open(path) as source_file:
        location = Location(path, find_return_annotation_location(source_file, func))
    return _return_annotation_insertion(location, return_type)
    

def _arg_annotation_insertion(location, type_):
    return _Insertion(location, ": {0}".format(format_type(type_)))

def _return_annotation_insertion(location, type_):
    return _Insertion(location, " -> {0}".format(format_type(type_)))


_Insertion = collections.namedtuple("_Insertion", ["location", "value"])


def _insert_strings(path, insertions):
    with open(path) as source_file:
        lines = list(source_file.readlines())
    
    insertions = sorted(insertions, key=lambda insertion: insertion.location, reverse=True)
    
    for insertion in insertions:
        line_index = insertion.location.lineno - 1
        col_offset = insertion.location.col_offset
        lines[line_index] = _str_insert(lines[line_index], col_offset, insertion.value)
    
    with open(path, "w") as source_file:
        source_file.write("".join(lines))


def _str_insert(original, index, to_insert):
    return original[:index] + to_insert + original[index:]

