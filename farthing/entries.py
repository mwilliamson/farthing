from .ast_util import load_func


class TraceEntry(object):
    def __init__(self, location, func, args=None):
        self.location = location
        self.func = func
        self.args = args
        self.returns = None
        self.raises = None

    def __repr__(self):
        return "TraceEntry({0}, args={1}, returns={2}, raises={3}".format(self.func, self.args, self.returns, self.raises)
    
    def to_tuple(self):
        return (self.location, self.args, self.returns, self.raises)
    
    @staticmethod
    def from_tuple(value):
        location, args, returns, raises = value
        func = load_func(location)
        entry = TraceEntry(location, func, args)
        entry.returns = returns
        entry.raises = raises
        return entry
