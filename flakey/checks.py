import ast

from . import __version__


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, *targets):
        self.targets = set(targets)
        self.import_froms = {}
        self.matches = []

    def visit_Import(self, node):
        for name in node.names:
            self.import_froms[name.asname or name.name] = None

    def visit_ImportFrom(self, node):
        for name in node.names:
            self.import_froms[name.asname or name.name] = node.module

    def get_full_name(self, node):
        parts = []
        while node:
            if getattr(node, 'id', None):
                parts.append(node.id)
                break
            else:
                parts.append(node.attr)
                node = node.value
        parts.reverse()
        if parts[0] in self.import_froms:
            parts.insert(0, self.import_froms[parts[0]])
        return '.'.join(parts)

    def visit_Call(self, node):
        name = self.get_full_name(node.func)
        full_name = '.'.join(pkg for pkg in [self.import_froms.get(name, None), name] if pkg)
        if full_name in self.targets:
            self.matches.append((node, full_name))


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
