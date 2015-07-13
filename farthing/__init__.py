import runpy
import sys
import os
import ast
from importlib.abc import MetaPathFinder, FileLoader
from importlib.machinery import ModuleSpec
from importlib.util import decode_source


__all__ = ["run"]


def run(path):
    directory_path = os.path.dirname(path)
    sys.path[0] = directory_path
    sys.meta_path.insert(0, Finder(directory_path))
    runpy.run_path(path)


class Finder(MetaPathFinder):
    def __init__(self, directory_path):
        self._directory_path = directory_path
    
    def find_spec(self, fullname, path, target=None):
        path_prefix = os.path.join(self._directory_path, *fullname.split("."))
        package_path = os.path.join(path_prefix, "__init__.py")
        module_path = path_prefix + ".py"
        
        for possible_path in [package_path, module_path]:
            if os.path.exists(possible_path):
                return ModuleSpec(fullname, Loader(fullname, possible_path))


class Loader(FileLoader):
    def get_source(self, fullname):
        with open(self.path, "rb") as source_file:
            return decode_source(source_file.read())
    
    def source_to_code(self, data, path):
        node = ast.parse(data, path)
        return compile(node, path, 'exec')
