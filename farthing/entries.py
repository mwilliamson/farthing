import collections


class TraceEntry(object):
    def __init__(self, location, func, args=None):
        self.location = location
        self.func = func
        self.args = args
        self.returns = None
        self.raises = None

    def __repr__(self):
        return "TraceEntry({0}, args={1}, returns={2}, raises={3}".format(self.func, self.args, self.returns, self.raises)



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
