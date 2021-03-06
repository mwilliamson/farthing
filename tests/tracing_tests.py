import sys

from nose.tools import istest, assert_equal
from hamcrest import assert_that
import hamcrest as m

import farthing
from farthing.types import describe
from .util import program_with_module


@istest
def sys_argv_is_unchanged_by_running_trace():
    with program_with_module("") as program:
        original_argv = sys.argv[:]
        farthing.trace(argv=[program.run_path], trace_paths=[program.directory_path])
        assert_equal(original_argv, sys.argv)


@istest
def location_of_functions_is_stored():
    program_source = """
def repeat(x, y):
    return x * y

print(repeat("hello ", 3))
"""
    with program_with_module(program_source) as program:
        trace = farthing.trace(trace_paths=[program.directory_path], argv=[program.run_path])
        assert_that(trace, m.contains(m.has_properties({
            "location": m.has_properties({
                "path": program.module_path,
                "lineno": 2,
                "col_offset": 0
            }),
        })))


@istest
def type_of_positional_arguments_is_traced():
    program = """
def repeat(x, y):
    return x * y

print(repeat("hello ", 3))
"""
    trace = _run_and_trace(program)
    assert_that(trace, m.contains(m.has_properties({
        "location": m.has_properties({
            "lineno": 2,
            "col_offset": 0
        }),
        "args": m.has_entries({
            "x": describe(str),
            "y": describe(int),
        })
    })))


@istest
def type_of_keyword_only_arguments_is_traced():
    program = """
def repeat(x, *, y):
    return x * y

print(repeat("hello ", y=3))
"""
    trace = _run_and_trace(program)
    assert_that(trace, m.has_item(m.has_properties({
        "location": m.has_properties({
            "lineno": 2,
            "col_offset": 0
        }),
        "args": m.has_entries({
            "x": describe(str),
            "y": describe(int),
        })
    })))


@istest
def type_of_implicit_return_is_traced():
    program = """
def do_nothing():
    pass

print(do_nothing())
"""
    trace = _run_and_trace(program)
    assert_that(trace, m.has_item(m.has_properties({
        "location": m.has_properties({
            "lineno": 2,
            "col_offset": 0
        }),
        "returns": describe(type(None))
    })))

@istest
def type_of_return_with_implicit_value_is_traced():
    program = """
def do_nothing():
    return

print(do_nothing())
"""
    trace = _run_and_trace(program)
    assert_that(trace, m.has_item(m.has_properties({
        "location": m.has_properties({
            "lineno": 2,
            "col_offset": 0
        }),
        "returns": describe(type(None))
    })))


@istest
def type_of_return_with_explicit_value_is_traced():
    program = """
def answer():
    return 42

print(answer())
"""
    trace = _run_and_trace(program)
    assert_that(trace, m.has_item(m.has_properties({
        "location": m.has_properties({
            "lineno": 2,
            "col_offset": 0
        }),
        "returns": describe(int)
    })))


@istest
def returns_from_inner_and_outer_function_can_be_distinguished():
    program = """
def answer():
    def f():
        return 42
    return float(f())

print(answer())
"""
    trace = _run_and_trace(program)
    assert_that(trace, m.has_items(
        m.has_properties({
            "location": m.has_properties({
                "lineno": 2,
                "col_offset": 0
            }),
            "returns": describe(float)
        }),
        m.has_properties({
            "location": m.has_properties({
                "lineno": 3,
                "col_offset": 4
            }),
            "returns": describe(int)
        }),
    ))


@istest
def type_of_raised_exception_is_traced():
    program = """
def do_nothing():
    assert False

print(do_nothing())
"""
    trace = _run_and_trace(program)
    assert_that(trace, m.has_item(m.has_properties({
        "location": m.has_properties({
            "lineno": 2,
            "col_offset": 0
        }),
        "returns": None,
        "raises": describe(AssertionError)
    })))


def _run_and_trace(program_source):
    with program_with_module(program_source) as program:
        return farthing.trace(trace_paths=[program.directory_path], argv=[program.run_path])
