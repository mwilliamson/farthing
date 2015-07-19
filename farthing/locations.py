import collections


def create_location(path, lineno, col_offset):
    return Location(path, FileLocation(lineno, col_offset))
    

class Location(collections.namedtuple("Location", ["path", "in_file"])):
    @property
    def lineno(self):
        return self.in_file.lineno
    
    @property
    def col_offset(self):
        return self.in_file.col_offset

FileLocation = collections.namedtuple("FileLocation", ["lineno", "col_offset"])
