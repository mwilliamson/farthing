import sys
import contextlib
import os

import tempman
from nose.tools import istest, assert_equal
from hamcrest import assert_that
import hamcrest as m

import farthing


@istest
def sys_argv_is_unchanged_by_running_trace():
    with _program_with_module("") as program:
        original_argv = sys.argv[:]
        farthing.trace(program.directory_path, [program.run_path])
        assert_equal(original_argv, sys.argv)



@istest
def type_of_arguments_is_traced():
    program = """
def repeat(x, y):
    return x * y

print(repeat("hello ", 3))
"""
    with _program_with_module(program) as program:
        trace = farthing.trace(program.directory_path, [program.run_path])
        assert_that(trace, m.contains(m.has_properties({
            "func": m.has_properties({
                "lineno": 2,
                "col_offset": 0
            }),
            "args": m.has_entries({
                "x": str,
                "y": int
            })
        })))
    


@contextlib.contextmanager
def _program_with_module(module):
    with tempman.create_temp_dir() as directory:
        run_path = os.path.join(directory.path, "run.py")
        module_path = os.path.join(directory.path, "main.py")
        
        with open(run_path, "w") as run_file:
            run_file.write("import main")
        with open(module_path, "w") as module_file:
            module_file.write(module)
        
        yield _Program(directory.path, run_path)


class _Program(object):
    def __init__(self, directory, run_path):
        self.directory_path = directory
        self.run_path = run_path
