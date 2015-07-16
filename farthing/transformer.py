import ast


class FunctionTraceTransformer(ast.NodeTransformer):
    def __init__(self, trace_func_name):
        self.funcs = []
        self._trace_func_name = trace_func_name
        self._func_stack = []
    
    def visit_FunctionDef(self, node):
        func_index = len(self.funcs)
        self._func_stack.append(node)
        try:
            node = self.generic_visit(node)
            nodes = _NodeFactory(node)
        
            node.body.insert(0, self._generate_trace_call(nodes, "args", func_index))
            node.body.append(self._generate_trace_call(nodes, "returns", func_index, returns=nodes.Name("None", nodes.Load())))
            
            self.funcs.append(node)
            
            return node
        finally:
            self._func_stack.pop()
    
    def _generate_trace_call(self, nodes, trace_type, func_index, **kwargs):
        return nodes.Expr(
            nodes.Call(
                func=nodes.Name(self._trace_func_name, ast.Load()),
                args=[nodes.Str(trace_type), nodes.Num(func_index)],
                keywords=[nodes.keyword(key, value) for key, value in kwargs.items()],
                starargs=None,
                kwargs=None,
            )
        )


class _NodeFactory(object):
    def __init__(self, source_node):
        self._source_node = source_node
    
    def __getattr__(self, name):
        def create_node(*args, **kwargs):
            return ast.copy_location(getattr(ast, name)(*args, **kwargs), self._source_node)
        
        return create_node

