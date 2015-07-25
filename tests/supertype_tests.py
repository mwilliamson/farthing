from nose.tools import istest, assert_equal

from farthing.supertype import common_super_type
from farthing.types import union, describe



@istest
def common_super_type_of_single_type_is_that_type():
    assert_equal(describe(int), common_super_type([describe(int)]))


@istest
def common_super_type_of_repeated_single_type_is_that_type():
    assert_equal(describe(int), common_super_type([describe(int), describe(int)]))


@istest
def common_super_type_of_types_with_none_is_union_with_none():
    assert_equal(
        union([describe(type(None)), describe(int)]),
        common_super_type([describe(type(None)), describe(int)])
    )
