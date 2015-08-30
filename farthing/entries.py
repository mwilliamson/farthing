from .ast_util import load_funcs
from .iterables import grouped


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
    def from_tuples(values):
        values_by_file = grouped(values, key=lambda value: value[0].path)
        
        entries = []
        
        for path, values_in_file in values_by_file:
            funcs = load_funcs(path)
            for location, args, returns, raises in values_in_file:
                func = funcs[location]
                entry = TraceEntry(location, func, args)
                entry.returns = returns
                entry.raises = raises
                entries.append(entry)
        
        return entries
