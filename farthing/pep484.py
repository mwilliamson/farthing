from . import types


def format_type(type_):
    if type_ == types.describe(type(None)):
        return "None"
    elif isinstance(type_, types.Union):
        return "Union[{0}]".format(", ".join(sorted(map(format_type, type_.values))))
    elif isinstance(type_, types.Any):
        return "Any"
    elif isinstance(type_, types.List):
        return "List[{0}]".format(format_type(type_.element))
    elif isinstance(type_, types.Dict):
        return "Dict[{0}, {1}]".format(format_type(type_.key), format_type(type_.value))
    else:
        return type_.name
