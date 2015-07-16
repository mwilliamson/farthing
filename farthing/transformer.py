import ast


class FunctionTraceTransformer(ast.NodeTransformer):
    def __init__(self, trace_func_name):
        self.funcs = []
        self._trace_func_name = trace_func_name
        self._func_stack = []
    
    def visit_FunctionDef(self, node):
        func_index = len(self.funcs)
        self._func_stack.append(func_index)
        try:
            node = self.generic_visit(node)
            nodes = _NodeFactory(node)
        
            node.body.insert(0, self._generate_trace_call(nodes, "args", func_index))
            node.body.append(self._generate_trace_returns_call(nodes, func_index, self._generate_none(nodes)))
            
            self.funcs.append(node)
            
            return node
        finally:
            self._func_stack.pop()
    
    
    def visit_Return(self, node):
        func_index = self._func_stack[-1]
        nodes = _NodeFactory(node)
        if node.value is None:
            return [
                self._generate_trace_returns_call(nodes, func_index, self._generate_none(nodes)),
                node
            ]
        else:
            return [
                nodes.Assign([nodes.Name("__stash", nodes.Store())], node.value),
                self._generate_trace_returns_call(nodes, func_index, nodes.Name("__stash", nodes.Load())),
                nodes.Return(nodes.Name("__stash", nodes.Load()))
            ]
    
    def _generate_none(self, nodes):
        return nodes.Name("None", nodes.Load())
    
    
    def _generate_trace_returns_call(self, nodes, func_index, value):
        return self._generate_trace_call(nodes, "returns", func_index, returns=value)
        
    
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

