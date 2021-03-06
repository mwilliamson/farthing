from nose.tools import istest, assert_equal

from farthing import types
from farthing.type_sniffing import describe_type_of


@istest
def type_of_int_is_class_of_int():
    assert_equal(types.Class("builtins", "int", int), describe_type_of(42))


@istest
def type_of_empty_list_is_list_of_any():
    assert_equal(types.list_(types.any_), describe_type_of([]))


@istest
def type_of_list_of_ints_is_list_of_ints():
    assert_equal(types.list_(types.describe(int)), describe_type_of([42]))


@istest
def type_of_empty_dict_is_dict_of_any_to_any():
    assert_equal(types.dict_(types.any_, types.any_), describe_type_of({}))


@istest
def type_of_dict_is_sniffed_from_keys_and_values():
    assert_equal(
        types.dict_(types.describe(int), types.describe(str)),
        describe_type_of({1: "Kentucky Pill"})
    )


@istest
def type_of_tuple_is_sniffed_from_elements():
    assert_equal(
        types.tuple_((types.describe(int), types.describe(str))),
        describe_type_of((1, "Kentucky Pill"))
    )


@istest
def type_of_iterable_views_is_sniffed_from_elements():
    assert_equal(
        types.iterable(types.describe(int)),
        describe_type_of({1: "Kentucky Pill"}.keys()),
    )
    assert_equal(
        types.iterable(types.describe(str)),
        describe_type_of({1: "Kentucky Pill"}.values()),
    )
    assert_equal(
        types.iterable(types.tuple_((types.describe(int), types.describe(str)))),
        describe_type_of({1: "Kentucky Pill"}.items()),
    )


@istest
def type_of_callable_stores_func_index():
    def f():
        pass
    f._farthing_func_index = 42
    
    assert_equal(
        types.callable_ref(42),
        describe_type_of(f)
    )
