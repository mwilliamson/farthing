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


Location = collections.namedtuple("Location", ["path", "lineno", "col_offset"])
