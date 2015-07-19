import itertools
import collections

from .ast_util import func_args


def annotate(log):
    for path, entries in _grouped(log, lambda entry: entry.location.path):
        _annotate_file(path, entries)


def _annotate_file(path, entries):
    for location, func_entries in _grouped(entries, lambda entry: entry.location):
        _annotate_function(path, list(func_entries))


def _annotate_function(path, entries):
    insertions = []
    
    func = entries[0].func
    for arg in func_args(func):
        module, name = entries[0].args[arg.arg]
        location = _Location(arg.lineno, arg.col_offset + len(arg.arg))
        insertions.append(_Insertion(location, ": {0}".format(name)))
    
    _insert_strings(path, insertions)


_Insertion = collections.namedtuple("_Insertion", ["location", "value"])
_Location = collections.namedtuple("_Location", ["lineno", "col_offset"])


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

