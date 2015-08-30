import collections


def create_location(path, lineno, col_offset):
    return Location(path, lineno, col_offset)
    

Location = collections.namedtuple("Location", ["path", "lineno", "col_offset"])
