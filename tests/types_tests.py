from nose.tools import istest, assert_equal

from farthing import types


@istest
def type_of_int_is_class_of_int():
    assert_equal(types.Class("builtins", "int"), types.describe(int))
