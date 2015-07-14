import runpy
import sys
import os
import uuid
import builtins
import multiprocessing
import inspect

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
    original_argv = sys.argv[:]
    try:
        script_directory_path = os.path.dirname(argv[0])
        sys.path[0] = script_directory_path
        transformer = FunctionTraceTransformer(_trace_func_name)
        finder = importing.Finder(trace_path, transformer)
        sys.meta_path.insert(0, finder)
        try:
            sys.argv[:] = argv
            
            trace = []
            
            def trace_func(func_index):
                func = transformer.funcs[func_index]
                frame_record = inspect.stack()[1]
                frame = frame_record[0]
                actual_arg_types = dict(
                    _read_arg_type(frame, arg)
                    for arg in func.args.args
                )
                
                trace.append(TraceEntry(func, actual_arg_types))
            
            setattr(builtins, _trace_func_name, trace_func)
            try:
                runpy.run_path(argv[0], run_name="__main__")
            finally:
                delattr(builtins, _trace_func_name)
            pipe.send(trace)
        finally:
            sys.meta_path.remove(finder)
    finally:
        sys.argv[:] = original_argv


def _read_arg_type(frame, arg_node):
    actual_arg = frame.f_locals[arg_node.arg]
    actual_arg_type = type(actual_arg)
    return arg_node.arg, (actual_arg_type.__module__, actual_arg_type.__name__)
    


class TraceEntry(object):
    def __init__(self, func, args):
        self.func = func
        self.args = args


_trace_func_name = str(uuid.uuid4())

