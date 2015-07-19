import io
import ast

from nose.tools import istest, assert_equal

from farthing.entries import FileLocation
from farthing.ast_util import find_return_annotation_location


@istest
class ReturnAnnotationLocationTests(object):
    @istest
    def returns_location_of_return_annotation_hole(self):
        source = """
def repeat(x, y):
    return x * y
"""

        assert_equal(FileLocation(2, 16), _find_return_annotation_location(source))
    
    @istest
    def handles_nested_parens_in_function_signature(self):
        source = """
def repeat(x: (), y):
    return x * y
"""

        assert_equal(FileLocation(2, 20), _find_return_annotation_location(source))
    
    @istest
    def handles_line_break_in_arguments(self):
        source = """
def repeat(x: (),
        y):
    return x * y
"""

        assert_equal(FileLocation(3, 10), _find_return_annotation_location(source))
    
    @istest
    def handles_line_break_immediately_after_function_name(self):
        source = """
def repeat \\
        (x: (), y):
    return x * y
"""

        assert_equal(FileLocation(3, 18), _find_return_annotation_location(source))


def _find_return_annotation_location(source):
    node = ast.parse(source)
    func = node.body[0]
    assert isinstance(func, ast.FunctionDef)
    return find_return_annotation_location(io.StringIO(source), func)
