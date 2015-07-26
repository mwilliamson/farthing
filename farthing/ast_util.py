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
    
    reader.seek(func.lineno, func.col_offset)
    reader.seek_char("(")
    depth = 1
    while depth > 0:
        character = next(reader)
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
    
    next(reader)
    return reader.location()


def _seek(lines, location, char):
    line = lines[location.lineno - 1]
    col_offset = line.index(char, location.col_offset + 1)
    return FileLocation(location.lineno, col_offset)

class _SourceReader(object):
    def __init__(self, lines):
        self._lines = lines
    
    def seek(self, lineno, col_offset):
        self._lineno = lineno
        self._col_offset = col_offset
    
    def seek_char(self, value):
        while self._char() != value:
            next(self)
    
    def __next__(self):
        if self._col_offset < len(self._line()) - 1:
            self._col_offset += 1
        else:
            self._lineno += 1
            self._col_offset = 0
        
        return self._char()
    
    def _line(self):
        return self._lines[self._lineno - 1]
    
    def _char(self):
        return self._line()[self._col_offset]
    
    def location(self):
        return FileLocation(self._lineno, self._col_offset)
