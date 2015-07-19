import itertools
import collections

from .ast_util import func_args
from .entries import FileLocation


def annotate(log):
    for path, entries in _grouped(log, lambda entry: entry.location.path):
        _annotate_file(path, entries)


def _annotate_file(path, entries):
    for location, func_entries in _grouped(entries, lambda entry: entry.location):
        _annotate_function(path, list(func_entries))


def _annotate_function(path, entries):
    # TODO: investigate libraries that will allow editing of nodes while preserving concrete syntax
    insertions = []
    
    func = entries[0].func
    for arg in filter(lambda arg: arg.annotation is None, func_args(func)):
        module, name = entries[0].args[arg.arg]
        location = FileLocation(arg.lineno, arg.col_offset + len(arg.arg))
        insertions.append(_arg_annotation_insertion(location, name))
    
    return_type_annotation = _return_type_annotation(path, func, entries[0].returns)
    if return_type_annotation is not None:
        insertions.append(return_type_annotation)
    
    _insert_strings(path, insertions)


def _return_type_annotation(path, func, return_type):
    if return_type is None or func.returns is not None:
        return None
    
    with open(path) as source_file:
        lines = source_file.readlines()
    
    func_location = FileLocation(func.lineno, func.col_offset)
    args_start_location = _seek(lines, func_location, "(")
    # TODO: handle nested parens
    args_end_location = _seek(lines, args_start_location, ")")
    location = FileLocation(args_end_location.lineno, args_end_location.col_offset + 1)
    
    return _return_annotation_insertion(location, return_type[1])

def _seek(lines, location, char):
    # TODO: handle going on to next line
    line = lines[location.lineno - 1]
    col_offset = line.index(char, location.col_offset + 1)
    return FileLocation(location.lineno, col_offset)
    

def _arg_annotation_insertion(location, annotation):
    return _Insertion(location, ": {0}".format(annotation))

def _return_annotation_insertion(location, annotation):
    return _Insertion(location, " -> {0}".format(annotation))


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


def _grouped(values, key):
    return itertools.groupby(sorted(values, key=key), key=key)

