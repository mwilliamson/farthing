from nose.tools import istest, assert_equal

from farthing.supertype import common_super_type
from farthing.types import union, describe, List, Dict, any_



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


@istest
def common_super_type_of_list_of_any_and_list_of_other_type_is_list_of_other_type():
    assert_equal(
        List(describe(int)),
        common_super_type([List(any_), List(describe(int))])
    )


@istest
def common_super_type_of_dict_of_any_to_any_and_other_dict_is_other_dict():
    assert_equal(
        Dict(describe(int), describe(str)),
        common_super_type([Dict(any_, any_), Dict(describe(int), describe(str))])
    )
