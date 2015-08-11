from nose.tools import istest, assert_equal

from farthing import types


@istest
def union_of_one_type_is_that_type():
    assert_equal(types.describe(int), types.union([types.describe(int)]))


@istest
def unions_are_order_agnostic():
    assert_equal(
        types.union([types.describe(str), types.describe(int)]),
        types.union([types.describe(int), types.describe(str)])
    )


@istest
def unions_are_flattened():
    assert_equal(
        types.union([types.describe(int), types.describe(str), types.describe(float)]),
        types.union([types.describe(int), types.union([types.describe(str), types.describe(float)])])
    )
