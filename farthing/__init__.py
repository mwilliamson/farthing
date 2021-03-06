import runpy
import uuid
import multiprocessing
import traceback
import sys

from . import importing, runtime
from .transformer import FunctionTraceTransformer
from .entries import TraceEntry
from .locations import create_location
from .annotate import annotate
from .ast_util import func_args
from .type_sniffing import describe_type_of


__all__ = ["run"]


def run_and_annotate(**kwargs):
    pool = multiprocessing.Pool(processes=1)
    return pool.apply(_run_and_annotate_subprocess, kwds=kwargs)


def _run_and_annotate_subprocess(*, argv, annotate_paths, trace_paths):
    trace_log = _generate_trace(argv, annotate_paths + trace_paths)
    annotate(trace_log, annotate_paths)
    

def trace(*, argv, trace_paths):
    pool = multiprocessing.Pool(processes=1)
    entry_tuples = pool.apply(_trace_subprocess, args=(argv, trace_paths))
    return TraceEntry.from_tuples(entry_tuples)

def _trace_subprocess(argv, trace_paths):
    trace = _generate_trace(argv, trace_paths)
    return [entry.to_tuple() for entry in trace]


def _generate_trace(argv, trace_paths):
    with runtime.override_argv(argv):
        transformer = FunctionTraceTransformer(_trace_func_name)
        finder = importing.Finder(trace_paths, transformer)
        with runtime.prioritise_module_finder(finder):
            trace = []
            
            def trace_func(func_index):
                source_path, func = transformer.funcs[func_index]
                frame = sys._getframe(1)
                
                location = create_location(source_path, func.lineno, func.col_offset)
                entry = _trace_entry(location, func, frame)
                trace.append(entry)
                return _FunctionTracer(entry)
            
            def _farthing_assign_func_index(func_index):
                def assign(func):
                    func._farthing_func_index = func_index
                    return func
                    
                return assign
                
            extra_builtins = {
                _trace_func_name: trace_func,
                "_farthing_assign_func_index": _farthing_assign_func_index,
            }
            with runtime.add_builtins(extra_builtins):
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
        self._entry.returns = describe_type_of(returns)
        return returns
    
    def trace_raise(self):
        raises = sys.exc_info()[1]
        self._entry.raises = describe_type_of(raises)
    

def _trace_entry(location, func, frame):
    actual_arg_types = dict(
        _read_arg_type(frame, arg)
        for arg in func_args(func)
    )
    
    return TraceEntry(location, func, args=actual_arg_types)

def _read_arg_type(frame, arg_node):
    actual_arg = frame.f_locals[arg_node.arg]
    return arg_node.arg, describe_type_of(actual_arg)


_trace_func_name = str(uuid.uuid4())

