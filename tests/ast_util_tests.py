import ast
import io

from nose.tools import istest, assert_equal

from farthing.locations import Location
from farthing.ast_util import find_return_annotation_location
from farthing import parser


@istest
class ReturnAnnotationLocationTests(object):
    @istest
    def returns_location_of_return_annotation_hole(self):
        source = """
def repeat(x, y):
    return x * y
"""

        assert_equal(_location(2, 16), _find_return_annotation_location(source))
        
    @istest
    def handles_function_with_no_arguments(self):
        source = """
def repeat():
    return
"""

        assert_equal(_location(2, 12), _find_return_annotation_location(source))
    
    @istest
    def handles_function_with_function_call_decorator(self):
        source = """
@cached()
def repeat():
    return x * y
"""

        assert_equal(_location(3, 12), _find_return_annotation_location(source))
    
    @istest
    def handles_nested_parens_in_function_signature(self):
        source = """
def repeat(x: (), y):
    return x * y
"""

        assert_equal(_location(2, 20), _find_return_annotation_location(source))
    
    @istest
    def handles_line_break_in_arguments(self):
        source = """
def repeat(x: (),
        y):
    return x * y
"""

        assert_equal(_location(3, 10), _find_return_annotation_location(source))
    
    @istest
    def handles_line_break_immediately_after_function_name(self):
        source = """
def repeat \\
        (x: (), y):
    return x * y
"""

        assert_equal(_location(3, 18), _find_return_annotation_location(source))


_filename = "main.py"


def _find_return_annotation_location(source):
    node = parser.parse(source, _filename)
    func = node.body[0]
    assert isinstance(func, ast.FunctionDef)
    return find_return_annotation_location(io.StringIO(source), func)


def _location(lineno, col_offset):
    return Location(_filename, lineno, col_offset)
