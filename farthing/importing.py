import os
import ast
from importlib.abc import MetaPathFinder, FileLoader
from importlib.machinery import ModuleSpec, PathFinder
from importlib.util import decode_source


class Finder(MetaPathFinder):
    def __init__(self, directory_path, transformer):
        self._directory_path = directory_path
        self._transformer = transformer
        
    
    def find_spec(self, fullname, path, target=None):
        module_spec = PathFinder.find_spec(fullname, path, target)
        if module_spec and module_spec.has_location and self._is_in_directory(module_spec.origin):
            return ModuleSpec(fullname, Loader(fullname, module_spec.origin, self._transformer))
    
    def _is_in_directory(self, path):
        return os.path.commonprefix(list(map(os.path.normpath, [self._directory_path, path])))
    

class Loader(FileLoader):
    def __init__(self, fullname, path, transformer):
        super().__init__(fullname, path)
        self._transformer = transformer
    
    def get_source(self, fullname):
        with open(self.path, "rb") as source_file:
            return decode_source(source_file.read())
    
    def source_to_code(self, data, path):
        node = self._transformer.transform(path, ast.parse(data, path))
        return compile(node, path, 'exec')
