import contextlib
import os

import tempman

@contextlib.contextmanager
def program_with_module(module):
    with tempman.create_temp_dir() as directory:
        program = _Program(directory.path)
        
        with open(program.run_path, "w") as run_file:
            run_file.write("import main")
        with open(program.module_path, "w") as module_file:
            module_file.write(module)
        
        yield program



class _Program(object):
    def __init__(self, directory):
        self.directory_path = directory
        self.run_path = os.path.join(directory, "run.py")
        self.module_path = os.path.join(directory, "main.py")
