from nose.tools import istest, assert_equal

from farthing.supertype import common_super_type


@istest
def common_super_type_of_single_type_is_that_type():
    assert_equal(int, common_super_type([int]))
