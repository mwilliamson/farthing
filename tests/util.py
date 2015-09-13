import contextlib
import os

import tempman


_run_path = "run.py"
_main_path = "main.py"

@contextlib.contextmanager
def program_with_module(module):
    files = {_run_path: "import main", _main_path: module}
    with create_temp_dir(files) as directory:
        yield _Program(directory.path)


@contextlib.contextmanager
def create_temp_dir(files):
    with tempman.create_temp_dir() as directory:
        for path, contents in files.items():
            with open(os.path.join(directory.path, path), "w") as fileobj:
                fileobj.write(contents)
        
        yield directory



class _Program(object):
    def __init__(self, directory):
        self.directory_path = directory
        self.run_path = os.path.join(directory, _run_path)
        self.module_path = os.path.join(directory, _main_path)
