import cobble

from . import types


def format_type(type_):
    return Formatter().visit(type_)


class Formatter(cobble.visitor(types.Type)):
    def visit_class(self, type_):
        if type_ == types.describe(type(None)):
            return "None"
        else:
            return type_.name
    
    def visit_union(self, type_):
        return "Union[{0}]".format(", ".join(sorted(map(format_type, type_.values))))
    
    def visit_any(self, type_):
        return "Any"
    
    def visit_list(self, type_):
        return "List[{0}]".format(format_type(type_.element))
    
    def visit_iterable(self, type_):
        return "Iterable[{0}]".format(format_type(type_.element))
    
    def visit_dict(self, type_):
        return "Dict[{0}, {1}]".format(format_type(type_.key), format_type(type_.value))
    
    def visit_tuple(self, type_):
        return "Tuple[{0}]".format(self._format_types(type_.elements))
    
    def visit_callable(self, type_):
        args = self._format_types(arg_type for arg_name, arg_type in type_.args)
        returns = format_type(type_.returns)
        return "Callable[[{0}], {1}]".format(args, returns)
        
    def visit_callable_ref(self, type_):
        return "Callable"

    def _format_types(self, types):
        return ", ".join(map(self.visit, types))
    
