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


# TODO: split actual annotation from generation of types to remove duplication in tests
@istest
def types_can_be_union():
    program = """
def repeat(x, y):
    if y is None:
        y = 2
    return x * y

print(repeat("hello ", 3))
print(repeat("hello ", None))
"""
    typed_program = """
def repeat(x: str, y: Union[None, int]) -> str:
    if y is None:
        y = 2
    return x * y

print(repeat("hello ", 3))
print(repeat("hello ", None))
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


@istest
def existing_return_annotations_are_retained():
    program = """
def repeat(x, y) -> object:
    return x * y

print(repeat("hello ", 3))
"""
    typed_program = """
def repeat(x: str, y: int) -> object:
    return x * y

print(repeat("hello ", 3))
"""
    with program_with_module(program) as program:
        farthing.run_and_annotate(program.directory_path, [program.run_path])
        assert_equal(typed_program, _read_file(program.module_path))


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


@istest
def can_annotate_multiple_functions_in_one_file():
    program = """
def f(x):
    return x

def g(x):
    return x

print(f(2) + g(3))
"""
    typed_program = """
def f(x: int) -> int:
    return x

def g(x: int) -> int:
    return x

print(f(2) + g(3))
"""
    with program_with_module(program) as program:
        farthing.run_and_annotate(program.directory_path, [program.run_path])
        assert_equal(typed_program, _read_file(program.module_path))


@istest
def self_argument_is_not_annotated():
    program = """
class Repeater(object):
    def repeat(self, x, y):
        return x * y

print(Repeater().repeat("hello ", 3))
"""
    typed_program = """
class Repeater(object):
    def repeat(self, x: str, y: int) -> str:
        return x * y

print(Repeater().repeat("hello ", 3))
"""
    with program_with_module(program) as program:
        farthing.run_and_annotate(program.directory_path, [program.run_path])
        assert_equal(typed_program, _read_file(program.module_path))


def _read_file(path):
    with open(path) as f:
        return f.read()
