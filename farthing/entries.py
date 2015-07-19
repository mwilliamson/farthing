class TraceEntry(object):
    def __init__(self, func, args=None, returns=None):
        self.func = func
        self.args = args
        self.returns = returns

    def __repr__(self):
        return "TraceEntry({0}, args={1}, returns={2}".format(self.func, self.args, self.returns)
