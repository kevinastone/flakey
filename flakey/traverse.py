# coding: utf-8
from astroid import nodes, scoped_nodes


class NotFoundException(Exception):
    def __init__(self, node):
        super(NotFoundException, self).__init__("Unknown node at line ({line}:{col})".format(line=node.lineno, col=node.col_offset))


def resolve(node, name):
    frame = node.frame()
    while frame:
        if name in frame.locals:
            return frame.locals[name][0]
        frame = frame.parent
    raise NotFoundException(node)


def traverse(node, ctx=None):
    if ctx is None:
        ctx = []
    if isinstance(node, nodes.Getattr):
        ctx.append(node.attrname)
        return traverse(node.expr, ctx)
    elif isinstance(node, nodes.AssName):
        assign = node.parent
        assert ctx[-1] == node.name
        ctx.pop()
        return traverse(assign.value, ctx)
    elif isinstance(node, nodes.Name):
        ctx.append(node.name)
        return traverse(resolve(node, node.name), ctx)
    elif isinstance(node, nodes.From):
        ctx.append(node.modname)
        return ctx
    elif isinstance(node, nodes.Import):
        return ctx
    elif isinstance(node, scoped_nodes.Function):
        return ctx
    elif isinstance(node, scoped_nodes.Class):
        return ctx
    elif isinstance(node, nodes.CallFunc):
        func_node = resolve(node.func, node.func.name)
        for return_node in func_node.nodes_of_class(nodes.Return):
            context = ctx[:]
            result = traverse(return_node.value, context)
            if result:
                return result
        else:
            raise NotFoundException(func_node)
    else:
        raise NotFoundException(node)


def identify_called_functions(root):
    fs = list(root.nodes_of_class(nodes.CallFunc))
    for f in fs:
        try:
            yield (f.lineno, f.col_offset, '.'.join(reversed(traverse(f.func))))
        except NotFoundException as ex:
            pass
