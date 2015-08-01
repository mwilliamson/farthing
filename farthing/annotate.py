import collections

from .ast_util import func_args, find_return_annotation_location
from .locations import FileLocation
from .supertype import common_super_type
from .iterables import grouped
from .pep484 import format_type


def annotate(log):
    for path, entries in grouped(log, lambda entry: entry.location.path):
        _annotate_file(path, entries)


def _annotate_file(path, entries):
    insertions = []
    
    for location, func_entries in grouped(entries, lambda entry: entry.location):
        insertions += _annotate_function(path, list(func_entries))
    
    _insert_strings(path, insertions)


def _annotate_function(path, entries):
    # TODO: investigate libraries that will allow editing of nodes while preserving concrete syntax
    insertions = []
    
    func = entries[0].func
    # TODO: Use a more reliable mechanism for detecting self args
    for arg in filter(lambda arg: arg.annotation is None and arg.arg != "self", func_args(func)):
        type_ = common_super_type(entry.args[arg.arg] for entry in entries)
        location = FileLocation(arg.lineno, arg.col_offset + len(arg.arg))
        insertions.append(_arg_annotation_insertion(location, type_))
    
    return_type_annotation = _return_type_annotation(path, func, common_super_type(entry.returns for entry in entries))
    if return_type_annotation is not None:
        insertions.append(return_type_annotation)
    
    return insertions


def _return_type_annotation(path, func, return_type):
    if return_type is None or func.returns is not None:
        return None
    
    with open(path) as source_file:
        location = find_return_annotation_location(source_file, func)
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

