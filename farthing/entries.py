class TraceEntry(object):
    def __init__(self, func, args=None):
        self.func = func
        self.args = args
        self.returns = None
        self.raises = None

    def __repr__(self):
        return "TraceEntry({0}, args={1}, returns={2}, raises={3}".format(self.func, self.args, self.returns, self.raises)
