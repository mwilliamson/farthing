from .entries import FileLocation


def func_args(func):
    return func.args.args + func.args.kwonlyargs


def find_return_annotation_location(fileobj, func):
    lines = fileobj.readlines()
    func_location = FileLocation(func.lineno, func.col_offset)
    args_start_location = _seek(lines, func_location, "(")
    # TODO: handle nested parens
    args_end_location = _seek(lines, args_start_location, ")")
    return FileLocation(args_end_location.lineno, args_end_location.col_offset + 1)


def _seek(lines, location, char):
    # TODO: handle going on to next line
    line = lines[location.lineno - 1]
    col_offset = line.index(char, location.col_offset + 1)
    return FileLocation(location.lineno, col_offset)
