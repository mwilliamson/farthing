from nose.tools import istest, assert_equal

from farthing import types
from farthing.pep484 import format_type


@istest
def none_is_formatted_as_none_instead_of_none_type():
    assert_equal("None", format_type(types.describe(type(None))))


@istest
def builtin_is_formatted_as_name_of_builtin():
    assert_equal("int", format_type(types.describe(int)))


@istest
def union_uses_union_class_with_getitem():
    type_ = types.union([types.describe(type(None)), types.describe(int)])
    assert_equal("Union[None, int]", format_type(type_))


@istest
def any_uses_any_value():
    assert_equal("Any", format_type(types.any_))


@istest
def list_uses_list_class_from_pep_484():
    assert_equal("List[int]", format_type(types.List(types.describe(int))))


@istest
def dict_uses_dict_class_from_pep_484():
    assert_equal("Dict[int, str]", format_type(types.Dict(types.describe(int), types.describe(str))))
