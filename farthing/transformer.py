import ast

class FunctionTraceTransformer(ast.NodeTransformer):
    def __init__(self, trace_func_name):
        self.funcs = []
        self._trace_func_name = trace_func_name
        self._func_stack = []
    
    def visit_FunctionDef(self, node):
        func_index = len(self.funcs)
        self.funcs.append(node)
        self._func_stack.append(func_index)
        try:
            node = self.generic_visit(node)
            nodes = _NodeFactory(node)
        
            node.body.insert(0, nodes.Assign(
                [nodes.Name(_tracer_name(func_index), nodes.Store())],
                nodes.call(
                    func=nodes.Name(self._trace_func_name, ast.Load()),
                    args=[nodes.Num(func_index)],
                )
            ))
            node.body.append(self._generate_trace_returns_call(nodes, func_index, self._generate_none(nodes)))
            
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
        return nodes.Expr(
            nodes.call(
                func=nodes.Attribute(nodes.Name(_tracer_name(func_index), nodes.Load()), "trace_return", nodes.Load()),
                args=[value],
            )
        )


class _NodeFactory(object):
    def __init__(self, source_node):
        self._source_node = source_node
    
    def __getattr__(self, name):
        def create_node(*args, **kwargs):
            return ast.copy_location(getattr(ast, name)(*args, **kwargs), self._source_node)
        
        return create_node
    
    def call(self, func, args):
        return self.Call(func=func, args=args, keywords=[], starargs=None, kwargs=None)


def _tracer_name(func_index):
    return "__farthing_tracer_{0}".format(func_index)
