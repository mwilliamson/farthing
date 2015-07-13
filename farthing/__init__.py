import runpy
import sys
import os
import ast
from importlib.abc import MetaPathFinder, FileLoader
from importlib.machinery import ModuleSpec, PathFinder
from importlib.util import decode_source


__all__ = ["run"]


def run(argv):
    script = argv[2]
    script_directory_path = os.path.dirname(script)
    sys.path[0] = script_directory_path
    sys.meta_path.insert(0, Finder(argv[1]))
    sys.argv[:] = [argv[0]] + argv[3:]
    runpy.run_path(script, run_name="__main__")


class Finder(MetaPathFinder):
    def __init__(self, directory_path):
        self._directory_path = directory_path
    
    def find_spec(self, fullname, path, target=None):
        module_spec = PathFinder.find_spec(fullname, path, target)
        if module_spec and module_spec.has_location and self._is_in_directory(module_spec.origin):
            return ModuleSpec(fullname, Loader(fullname, module_spec.origin))
    
    def _is_in_directory(self, path):
        return os.path.commonprefix(list(map(os.path.normpath, [self._directory_path, path])))
    

class Loader(FileLoader):
    def get_source(self, fullname):
        with open(self.path, "rb") as source_file:
            return decode_source(source_file.read())
    
    def source_to_code(self, data, path):
        node = FunctionArgumentTracer().visit(ast.parse(data, path))
        return compile(node, path, 'exec')


class FunctionArgumentTracer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node = self.generic_visit(node)
        nodes = NodeFactory(node)
        
        node.body.insert(0, nodes.Expr(
            nodes.Call(
                func=nodes.Name("print", ast.Load()),
                args=[nodes.Str(node.name)],
                keywords=[],
                starargs=None,
                kwargs=None,
            )
        ))
        return node


class NodeFactory(object):
    def __init__(self, source_node):
        self._source_node = source_node
    
    def __getattr__(self, name):
        def create_node(*args, **kwargs):
            return ast.copy_location(getattr(ast, name)(*args, **kwargs), self._source_node)
        
        return create_node
