import runpy
import uuid
import multiprocessing
import inspect
import traceback
import sys

from . import importing, runtime
from .transformer import FunctionTraceTransformer
from .entries import TraceEntry
from .locations import create_location
from .annotate import annotate
from .ast_util import func_args
from .types import describe as describe_type


__all__ = ["run"]


def run_and_annotate(trace_path, argv):
    trace_log = trace(trace_path, argv)
    annotate(trace_log)

def trace(trace_path, argv):
    parent_connection, child_connection = multiprocessing.Pipe(False)
    process = multiprocessing.Process(target=_trace_subprocess, args=(trace_path, argv, child_connection))
    process.start()
    
    trace = []
    while True:
        entry = parent_connection.recv()
        if entry == "END":
            process.join()
            return trace
        else:
            trace.append(TraceEntry.from_tuple(entry))

def _trace_subprocess(trace_path, argv, pipe):
    trace = _generate_trace(trace_path, argv)
    
    for entry in trace:
        pipe.send(entry.to_tuple())
    pipe.send("END")


def _generate_trace(trace_path, argv):
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
    
    return trace


class _FunctionTracer(object):
    def __init__(self, entry):
        self._entry = entry

    def trace_return(self, returns):
        self._entry.returns = describe_type(type(returns))
        return returns
    
    def trace_raise(self):
        raises = sys.exc_info()[1]
        self._entry.raises = describe_type(type(raises))
    

def _trace_entry(location, func, frame):
    actual_arg_types = dict(
        _read_arg_type(frame, arg)
        for arg in func_args(func)
    )
    
    return TraceEntry(location, func, args=actual_arg_types)

def _read_arg_type(frame, arg_node):
    actual_arg = frame.f_locals[arg_node.arg]
    return arg_node.arg, describe_type(type(actual_arg))


_trace_func_name = str(uuid.uuid4())

