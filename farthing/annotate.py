import itertools

from .ast_util import func_args


def annotate(log):
    for path, entries in _grouped(log, lambda entry: entry.location.path):
        _annotate_file(path, entries)


def _annotate_file(path, entries):
    for location, func_entries in _grouped(entries, lambda entry: entry.location):
        _annotate_function(path, list(func_entries))


def _annotate_function(path, entries):
    source = _SourceFile(path)
    
    func = entries[0].func
    # TODO: rather than reversing, have _SourceFile keep track of insertions and handle appropriately
    for arg in reversed(func_args(func)):
        module, name = entries[0].args[arg.arg]
        source.insert((arg.lineno, arg.col_offset + len(arg.arg)), ": {0}".format(name))
    
    source.save()


class _SourceFile():
    def __init__(self, path):
        self.path = path
        with open(path) as source_file:
            self._lines = list(source_file.readlines())
    
    def insert(self, location, value):
        lineno, col_offset = location
        line_index = lineno - 1
        self._lines[line_index] = _str_insert(self._lines[line_index], col_offset, value)
    
    def save(self):
        with open(self.path, "w") as source_file:
            source_file.write("".join(self._lines))


def _str_insert(original, index, to_insert):
    return original[:index] + to_insert + original[index:]


def _grouped(values, key):
    return itertools.groupby(sorted(values, key=key), key=key)

