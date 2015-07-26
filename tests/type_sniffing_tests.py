from nose.tools import istest, assert_equal

from farthing import types
from farthing.type_sniffing import describe_type_of


@istest
def type_of_int_is_class_of_int():
    assert_equal(types.Class("builtins", "int"), describe_type_of(42))


@istest
def type_of_empty_list_is_list_of_any():
    assert_equal(types.list_(types.any_), describe_type_of([]))


@istest
def type_of_list_of_ints_is_list_of_ints():
    assert_equal(types.list_(types.describe(int)), describe_type_of([42]))

