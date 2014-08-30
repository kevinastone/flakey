from astroid.manager import AstroidManager

from astroid.builder import AstroidBuilder
from astroid.rebuilder import TreeRebuilder


def rebuild_ast(tree, modname='', package=False):
    manager = AstroidManager()
    builder = AstroidBuilder(manager)
    rebuilder = TreeRebuilder(manager)
    module = rebuilder.visit_module(tree, modname=modname, package=package)
    module._from_nodes = rebuilder._from_nodes
    module._delayed_assattr = rebuilder._delayed_assattr
    module = builder._post_build(module, 'utf8')
    return module
