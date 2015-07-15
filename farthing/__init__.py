import runpy
import sys
import os
import uuid
import builtins
import multiprocessing
import inspect
import contextlib

from . import importing
from .transformer import FunctionTraceTransformer


__all__ = ["run"]


def run(trace_path, argv):
    trace(trace_path, argv)

def trace(trace_path, argv):
    parent_connection, child_connection = multiprocessing.Pipe(False)
    process = multiprocessing.Process(target=_trace_subprocess, args=(trace_path, argv, child_connection))
    process.start()
    process.join()
    if parent_connection.poll():
        return parent_connection.recv()
    else:
        raise Exception("subprocess exited without sending trace")

def _trace_subprocess(trace_path, argv, pipe):
    with _override_argv(argv):
        transformer = FunctionTraceTransformer(_trace_func_name)
        finder = importing.Finder(trace_path, transformer)
        with _prioritise_module_finder(finder):
            trace = []
            
            def trace_func(func_index):
                func = transformer.funcs[func_index]
                frame_record = inspect.stack()[1]
                frame = frame_record[0]
                actual_arg_types = dict(
                    _read_arg_type(frame, arg)
                    for arg in (func.args.args + func.args.kwonlyargs)
                )
                
                trace.append(TraceEntry(func, actual_arg_types))
            
            with _add_builtin(_trace_func_name, trace_func):
                runpy.run_path(argv[0], run_name="__main__")
            pipe.send(trace)


def _read_arg_type(frame, arg_node):
    actual_arg = frame.f_locals[arg_node.arg]
    actual_arg_type = type(actual_arg)
    return arg_node.arg, (actual_arg_type.__module__, actual_arg_type.__name__)


@contextlib.contextmanager
def _override_argv(argv):
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
def _prioritise_module_finder(finder):
    sys.meta_path.insert(0, finder)
    try:
        yield
    finally:
        sys.meta_path.remove(finder)


@contextlib.contextmanager
def _add_builtin(key, value):
    setattr(builtins, key, value)
    try:
        yield
    finally:
        delattr(builtins, key)


class TraceEntry(object):
    def __init__(self, func, args):
        self.func = func
        self.args = args


_trace_func_name = str(uuid.uuid4())

