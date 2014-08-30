import ast

from . import __version__

from .parser import rebuild_ast
from .traverse import identify_called_functions


class BannedFunctionChecker(object):
    """Check for outlawed functions"""
    name = 'flakey'
    version = __version__
    _error_tmpl = "{code} {func} is banned"
    functions = {
        'datetime.datetime.now': 'B101',
        'datetime.datetime.utcnow': 'B102',
    }

    def __init__(self, tree, filename=None):
        self.tree = rebuild_ast(tree)
        self.filename = filename

    def run(self):
        for line_number, column, func_name in identify_called_functions(self.tree):
            if func_name in self.functions.keys():
                yield line_number, column, self._error_tmpl.format(code=self.functions[func_name], func=func_name), type(self)
