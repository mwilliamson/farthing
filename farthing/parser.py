import ast


def parse(source, filename):
    node = ast.parse(source, filename)
    _PathNodeTransformer(filename).visit(node)
    return node
    

class _PathNodeTransformer(ast.NodeTransformer):
    def __init__(self, path):
        self._path = path
    
    def visit(self, node):
        node.path = self._path
        return self.generic_visit(node)
