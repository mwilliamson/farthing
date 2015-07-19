from nose.tools import istest, assert_equal

from .util import program_with_module
import farthing


@istest
def arguments_and_return_value_have_types_added_as_annotations():
    program = """
def repeat(x, y):
    return x * y

print(repeat("hello ", 3))
"""
    typed_program = """
def repeat(x: str, y: int) -> str:
    return x * y

print(repeat("hello ", 3))
"""
    with program_with_module(program) as program:
        farthing.run_and_annotate(program.directory_path, [program.run_path])
        assert_equal(typed_program, _read_file(program.module_path))


@istest
def existing_argument_annotations_are_retained():
    program = """
def repeat(x: object, y):
    return x * y

print(repeat("hello ", 3))
"""
    typed_program = """
def repeat(x: object, y: int) -> str:
    return x * y

print(repeat("hello ", 3))
"""
    with program_with_module(program) as program:
        farthing.run_and_annotate(program.directory_path, [program.run_path])
        assert_equal(typed_program, _read_file(program.module_path))


def _read_file(path):
    with open(path) as f:
        return f.read()


@istest
def no_return_value_annotation_is_added_if_no_return_type_information_is_available():
    program = """
def repeat(x, y):
    raise Exception()

print(repeat("hello ", 3))
"""
    typed_program = """
def repeat(x: str, y: int):
    raise Exception()

print(repeat("hello ", 3))
"""
    with program_with_module(program) as program:
        farthing.run_and_annotate(program.directory_path, [program.run_path])
        assert_equal(typed_program, _read_file(program.module_path))
