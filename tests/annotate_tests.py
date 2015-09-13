import os

from nose.tools import istest, assert_equal

from .util import program_with_module, create_temp_dir
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
    assert_equal(typed_program, _annotate_source(program))


@istest
def can_pass_trace_paths_for_files_instead_of_directories():
    source = """
def repeat(x, y):
    return x * y

print(repeat("hello ", 3))
"""
    typed_program = """
def repeat(x: str, y: int) -> str:
    return x * y

print(repeat("hello ", 3))
"""
    with program_with_module(source) as program:
        farthing.run_and_annotate(trace_paths=[program.module_path], argv=[program.run_path])
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
    assert_equal(typed_program, _annotate_source(program))


@istest
def function_arguments_to_higher_order_functions_are_traced():
    program = """
def map_ints(func, elements):
    return list(map(func, elements))

def half_int(value):
    return value / 2.0

print(map_ints(half_int, [1, 2, 3]))
"""
    typed_program = """
def map_ints(func: Callable[[int], float], elements: List[int]) -> List[float]:
    return list(map(func, elements))

def half_int(value: int) -> float:
    return value / 2.0

print(map_ints(half_int, [1, 2, 3]))
"""
    assert_equal(typed_program, _annotate_source(program))


@istest
def can_trace_files_without_annotating_them():
    # TODO: WIP
    return
    # We trace increment so that we know its type as its passed into twice
    twice = """
def twice(func, value):
    return func(func(value))
"""
    typed_twice = """
def twice(func: Callable[[int], int], value: int):
    return func(func(value))
"""
    increment = """
def increment(value):
    return value + 1
"""
    run = """
import twice
import increment
print(twice(increment, 40))
"""
    files = {
        "run.py": run,
        "twice.py": twice,
        "increment.py": increment,
    }
    with create_temp_dir(files) as directory:
        farthing.run_and_annotate(
            trace_paths=[os.path.join(directory.path, "twice.py")],
            argv=[os.path.join(directory.path, "run.py")])
        assert_equal(typed_twice, _read_file(os.path.join(directory.path, "twice.py")))


@istest
def no_infinite_loop_if_function_is_passed_to_itself():
    program = """
def strange(func):
    return 42

print(strange(strange))
"""
    typed_program = """
def strange(func: Callable[[Callable], int]) -> int:
    return 42

print(strange(strange))
"""
    assert_equal(typed_program, _annotate_source(program))


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
    assert_equal(typed_program, _annotate_source(program))


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
    assert_equal(typed_program, _annotate_source(program))


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
    assert_equal(typed_program, _annotate_source(program))


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
    assert_equal(typed_program, _annotate_source(program))


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
    assert_equal(typed_program, _annotate_source(program))


@istest
def properties_are_typed():
    program = """
class Box(object):
    @property
    def value(self):
        return 42

print(Box().value)
"""
    typed_program = """
class Box(object):
    @property
    def value(self) -> int:
        return 42

print(Box().value)
"""
    assert_equal(typed_program, _annotate_source(program))


def _annotate_source(source):
    with program_with_module(source) as program:
        farthing.run_and_annotate(trace_paths=[program.directory_path], argv=[program.run_path])
        return _read_file(program.module_path)


def _read_file(path):
    with open(path) as f:
        return f.read()
