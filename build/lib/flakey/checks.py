import ast

from . import __version__


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, *targets):
        self.targets = set(targets)
        self.import_froms = {}
        self.matches = []

    # def visit_Import(self, node):
    #     for name in node.names:
    #         full_name = name
    #         if full_name in self.targets:
    #             self.import_froms[name.asname or name.name] = full_name

    def visit_ImportFrom(self, node):
        for name in node.names:
            full_name = "%s.%s" % (node.module, name.name)
            if full_name in self.targets:
                self.import_froms[name.asname or name.name] = full_name

    def visit_Call(self, node):
        if getattr(node.func, 'id', None) in self.import_froms:
            self.matches.append((node, self.import_froms[node.func.id]))


class BannedFunctionChecker(object):
    """Check for outlawed functions"""
    name = 'flakey'
    version = __version__
    _error_tmpl = "{code} {func} is banned"
    functions = {
        'django.utils.strip_tags': 'B201',
        'urllib.urlencode': 'B202',
    }
    
    def __init__(self, tree, filename=None):
        self.tree = tree

    def run(self):
        visitor = FunctionVisitor(*self.functions.keys())
        visitor.visit(self.tree)
        for node, func_name in visitor.matches:
            yield node.lineno, 0, self._error_tmpl.format(code=self.functions[func_name], func=func_name), type(self)
