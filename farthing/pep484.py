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
    elif isinstance(type_, types.Callable):
        args = (format_type(arg_type) for arg, arg_type in type_.args)
        returns = format_type(type_.returns)
        return "Callable[[{0}], {1}]".format(", ".join(args), returns)
    elif isinstance(type_, types.CallableRef):
        return "Callable"
    else:
        return type_.name
