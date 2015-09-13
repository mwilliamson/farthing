from .ast_util import func_args
from .supertype import common_super_type
from .iterables import grouped
from . import types


def guess_types(log):
    guesser = _Guesser(log)
    return guesser.guess_types()


class _Guesser(object):
    def __init__(self, all_entries):
        self._all_entries = all_entries
        self._in_progress = set()
        entries_grouped_by_function = (
            list(func_entries)
            for location, func_entries in grouped(all_entries, lambda entry: entry.location)
        )
        self._entries_by_func_index = dict(
            (func_entries[0].func._farthing_func_index, func_entries)
            for func_entries in entries_grouped_by_function     
        )
        
    def guess_types(self):
        for func_index, entries in self._entries_by_func_index.items():
            func = entries[0].func
            yield func, self._guess_function_type(func, entries)

    def _guess_function_type(self, func, entries):
        args = []
        for arg in func_args(func):
            type_ = self._common_super_type(entry.args[arg.arg] for entry in entries)
            args.append((arg.arg, type_))
        
        returns = self._common_super_type(entry.returns for entry in entries)
        return types.callable_(tuple(args), returns)
    
    def _common_super_type(self, types):
        return common_super_type(map(self._resolve_callable_ref, types))
    
    def _resolve_callable_ref(self, type_):
        if type_ in self._in_progress:
            return type_
        elif types.is_callable_ref(type_):
            self._in_progress.add(type_)
            try:
                return self._guess_function_type(
                    self._entries_by_func_index[type_.func_index][0].func,
                    self._entries_by_func_index[type_.func_index])
            finally:
                self._in_progress.remove(type_)
        else:
            return type_
