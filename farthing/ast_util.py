import ast

from .locations import FileLocation


def func_args(func):
    return func.args.args + func.args.kwonlyargs


def load_funcs(path):
    with open(path) as source_file:
        return dict(
            (_node_location(node), node)
            for node in ast.walk(ast.parse(source_file.read()))
            if isinstance(node, ast.FunctionDef)
        )


def _node_location(node):
    return FileLocation(getattr(node, "lineno", None), getattr(node, "col_offset", None))


def find_return_annotation_location(fileobj, func):
    lines = fileobj.readlines()
    reader = _SourceReader(lines)
    
    reader.seek(func.body[0].lineno, func.body[0].col_offset)
    while reader.peek_previous() != ")":
        reader.move_previous()
    
    return reader.location()


class _SourceReader(object):
    def __init__(self, lines):
        self._lines = lines
    
    def seek(self, lineno, col_offset):
        self._lineno = lineno
        self._col_offset = col_offset
    
    def move_previous(self):
        self._col_offset -= 1
        if self._col_offset == 0:
            self._lineno -= 1
            self._col_offset = len(self._line())
    
    def peek_previous(self):
        return self._line()[self._col_offset - 1]
    
    def _line(self):
        return self._lines[self._lineno - 1]
    
    def location(self):
        return FileLocation(self._lineno, self._col_offset)
