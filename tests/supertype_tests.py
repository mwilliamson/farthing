import abc

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
def common_super_type_of_list_of_different_element_types_is_union_of_list_types():
    assert_equal(
        union([List(describe(int)), List(describe(str))]),
        common_super_type([List(describe(int)), List(describe(str))])
    )


@istest
def common_super_type_of_list_of_any_and_list_of_other_type_is_list_of_other_type():
    assert_equal(
        List(describe(int)),
        common_super_type([List(any_), List(describe(int))])
    )


@istest
def list_of_concrete_type_squashes_list_of_any_type_in_presence_of_other_types():
    assert_equal(
        union([List(describe(int)), describe(type(None))]),
        common_super_type([List(any_), List(describe(int)), describe(type(None))])
    )


@istest
def common_super_type_of_dict_of_different_element_types_is_union_of_dict_types():
    assert_equal(
        union([Dict(describe(int), describe(str)), Dict(describe(str), describe(int))]),
        common_super_type([Dict(describe(int), describe(str)), Dict(describe(str), describe(int))])
    )


@istest
def common_super_type_of_dict_of_any_to_any_and_other_dict_is_other_dict():
    assert_equal(
        Dict(describe(int), describe(str)),
        common_super_type([Dict(any_, any_), Dict(describe(int), describe(str))])
    )


@istest
def abstract_base_class_is_selected_as_type_if_all_types_are_instances_of_base_class():
    class Base(object):
        __metaclass__ = abc.ABCMeta
        
        @abc.abstractmethod
        def f(self):
            pass
    
    class A(Base):
        def f(self):
            pass
    
    class B(Base):
        def f(self):
            pass
    
    assert_equal(
        describe(Base),
        common_super_type([describe(A), describe(B)])
    )
