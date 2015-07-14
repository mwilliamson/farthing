import runpy
import sys
import os
import ast
import uuid
import builtins
import multiprocessing
import inspect

from . import importing


__all__ = ["run"]


def run(trace_path, argv):
    trace(trace_path, argv)

def trace(trace_path, argv):
    parent_connection, child_connection = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_trace_subprocess, args=(trace_path, argv, child_connection))
    process.start()
    trace = parent_connection.recv()
    process.join()
    return trace

def _trace_subprocess(trace_path, argv, pipe):
    original_argv = sys.argv[:]
    try:
        script_directory_path = os.path.dirname(argv[0])
        sys.path[0] = script_directory_path
        transformer = FunctionArgumentTracer()
        finder = importing.Finder(trace_path, transformer)
        sys.meta_path.insert(0, finder)
        try:
            sys.argv[:] = argv
            
            trace = []
            
            def trace_func(func_index):
                func = transformer.funcs[func_index]
                arg_names = [arg.arg for arg in func.args.args]
                frame_record = inspect.stack()[1]
                frame = frame_record[0]
                actual_args = [
                    frame.f_locals[name]
                    for name in arg_names
                ]
                actual_arg_types = list(map(type, actual_args))
                
                trace.append(TraceEntry(func, dict(zip(arg_names, actual_arg_types))))
            
            setattr(builtins, _trace_func_name, trace_func)
            try:
                runpy.run_path(argv[0], run_name="__main__")
            finally:
                delattr(builtins, _trace_func_name)
            pipe.send(trace)
            pipe.close()
        finally:
            sys.meta_path.remove(finder)
    finally:
        sys.argv[:] = original_argv
    

class TraceEntry(object):
    def __init__(self, func, args):
        self.func = func
        self.args = args


_trace_func_name = str(uuid.uuid4())

class FunctionArgumentTracer(ast.NodeTransformer):
    def __init__(self):
        self.funcs = []
    
    def visit_FunctionDef(self, node):
        node = self.generic_visit(node)
        nodes = NodeFactory(node)
        
        node.body.insert(0, nodes.Expr(
            nodes.Call(
                func=nodes.Name(_trace_func_name, ast.Load()),
                args=[nodes.Num(len(self.funcs))],
                keywords=[],
                starargs=None,
                kwargs=None,
            )
        ))
        
        self.funcs.append(node)
        
        return node


class NodeFactory(object):
    def __init__(self, source_node):
        self._source_node = source_node
    
    def __getattr__(self, name):
        def create_node(*args, **kwargs):
            return ast.copy_location(getattr(ast, name)(*args, **kwargs), self._source_node)
        
        return create_node
