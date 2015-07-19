import runpy
import uuid
import multiprocessing
import inspect
import traceback
import sys

from . import importing, runtime
from .transformer import FunctionTraceTransformer
from .entries import TraceEntry, create_location
from .annotate import annotate
from .ast_util import func_args


__all__ = ["run"]


def run_and_annotate(trace_path, argv):
    trace_log = trace(trace_path, argv)
    annotate(trace_log)

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
    with runtime.override_argv(argv):
        transformer = FunctionTraceTransformer(_trace_func_name)
        finder = importing.Finder(trace_path, transformer)
        with runtime.prioritise_module_finder(finder):
            trace = []
            
            def trace_func(func_index):
                source_path, func = transformer.funcs[func_index]
                frame_record = inspect.stack()[1]
                frame = frame_record[0]
                
                location = create_location(source_path, func.lineno, func.col_offset)
                entry = _trace_entry(location, func, frame)
                trace.append(entry)
                return _FunctionTracer(entry)
            
            with runtime.add_builtin(_trace_func_name, trace_func):
                try:
                    runpy.run_path(argv[0], run_name="__main__")
                except:
                    # Swallow any errors
                    print(traceback.format_exc(), file=sys.stderr)
            pipe.send(trace)


class _FunctionTracer(object):
    def __init__(self, entry):
        self._entry = entry

    def trace_return(self, returns):
        self._entry.returns = _describe_type(type(returns))
        return returns
    
    def trace_raise(self):
        raises = sys.exc_info()[1]
        self._entry.raises = _describe_type(type(raises))
    

def _trace_entry(location, func, frame):
    actual_arg_types = dict(
        _read_arg_type(frame, arg)
        for arg in func_args(func)
    )
    
    return TraceEntry(location, func, args=actual_arg_types)

def _read_arg_type(frame, arg_node):
    actual_arg = frame.f_locals[arg_node.arg]
    return arg_node.arg, _describe_type(type(actual_arg))

def _describe_type(type_):
    return type_.__module__, type_.__name__


_trace_func_name = str(uuid.uuid4())

