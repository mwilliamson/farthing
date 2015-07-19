import contextlib
import sys
import builtins
import os


@contextlib.contextmanager
def override_argv(argv):
    original_argv = sys.argv[:]
    original_path_0 = sys.path[0]
    try:
        sys.argv[:] = argv
        sys.path[0] = os.path.dirname(argv[0])
        yield
    finally:
        sys.argv[:] = original_argv
        sys.path[0] = original_path_0


@contextlib.contextmanager
def prioritise_module_finder(finder):
    sys.meta_path.insert(0, finder)
    try:
        yield
    finally:
        sys.meta_path.remove(finder)


@contextlib.contextmanager
def add_builtin(key, value):
    setattr(builtins, key, value)
    try:
        yield
    finally:
        delattr(builtins, key)
