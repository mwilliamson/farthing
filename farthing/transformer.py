import ast


class FunctionTraceTransformer(ast.NodeTransformer):
    def __init__(self, trace_func_name):
        self.funcs = []
        self._trace_func_name = trace_func_name
    
    def visit_FunctionDef(self, node):
        node = self.generic_visit(node)
        nodes = _NodeFactory(node)
        
        node.body.insert(0, nodes.Expr(
            nodes.Call(
                func=nodes.Name(self._trace_func_name, ast.Load()),
                args=[nodes.Num(len(self.funcs))],
                keywords=[],
                starargs=None,
                kwargs=None,
            )
        ))
        
        self.funcs.append(node)
        
        return node


class _NodeFactory(object):
    def __init__(self, source_node):
        self._source_node = source_node
    
    def __getattr__(self, name):
        def create_node(*args, **kwargs):
            return ast.copy_location(getattr(ast, name)(*args, **kwargs), self._source_node)
        
        return create_node

