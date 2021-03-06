import os
from importlib.abc import MetaPathFinder, FileLoader
from importlib.machinery import PathFinder
from importlib.util import decode_source, spec_from_loader

from . import parser
from .paths import is_in_any_directory


class Finder(MetaPathFinder):
    def __init__(self, directory_paths, transformer):
        self._directory_paths = list(map(os.path.abspath, directory_paths))
        self._transformer = transformer
        
    
    def find_spec(self, fullname, path, target=None):
        module_spec = PathFinder.find_spec(fullname, path, target)
        if module_spec and module_spec.has_location and self._is_in_directory(module_spec.origin):
            loader = Loader(fullname, module_spec.origin, self._transformer)
            is_package = os.path.basename(module_spec.origin).lower() == "__init__.py"
            return spec_from_loader(fullname, loader, origin=module_spec.origin, is_package=is_package)
    
    def _is_in_directory(self, path):
        return is_in_any_directory(self._directory_paths, path)
    

class Loader(FileLoader):
    def __init__(self, fullname, path, transformer):
        super().__init__(fullname, path)
        self._transformer = transformer
    
    def get_source(self, fullname):
        with open(self.path, "rb") as source_file:
            return decode_source(source_file.read())
    
    def source_to_code(self, data, path):
        node = self._transformer.transform(path, parser.parse(data, path))
        return compile(node, path, 'exec')
