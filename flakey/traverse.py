# coding: utf-8
from astroid import nodes, scoped_nodes


class NotFoundException(Exception):
    def __init__(self, node):
        super(NotFoundException, self).__init__("Unknown node at line ({line}:{col})".format(line=node.lineno, col=node.col_offset))


def lookup(node):
    if not isinstance(node, nodes.Name):
        return node
    frame = node.frame()
    while frame:
        if node.name in frame.locals:
            return frame.locals[node.name][0]
        frame = frame.parent
    raise NotFoundException(node)


def lookup_call(node, ctx):
    context = ctx[:]
    func_node = lookup(node.func)
    for return_node in func_node.nodes_of_class(nodes.Return):
        context = ctx[:]
        result = trace(return_node.value, context)
        if result:
            return result
    else:
        raise NotFoundException(func_node)


def lookup_assignment(node, ctx):
    ctx.pop()
    # return node.statement()
    assign = node.parent
    if isinstance(assign, nodes.Assign):
        return assign.value
    else:
        return node.infered()[0]
    # return assign.value


def trace(node, ctx=None):
    if ctx is None:
        ctx = []
    if isinstance(node, nodes.Getattr):
        ctx.append(node)
        # ctx.append(node.attrname)
        return trace(node.expr, ctx)
    elif isinstance(node, nodes.AssName):
        return trace(lookup_assignment(node, ctx), ctx)
    elif isinstance(node, nodes.Name):
        ctx.append(node)
        # ctx.append(node.name)
        return trace(lookup(node), ctx)
    elif isinstance(node, nodes.From):
        ctx.append(node)
        # ctx.append(node.modname)
        return ctx
    elif isinstance(node, nodes.Import):
        return ctx
    elif isinstance(node, scoped_nodes.Function) or isinstance(node, scoped_nodes.Lambda):
        return ctx
    elif isinstance(node, scoped_nodes.Class):
        return ctx
    elif isinstance(node, nodes.CallFunc):
        return lookup_call(node, ctx)
    else:
        raise NotFoundException(node)


def resolve(ctx):
    for node in ctx:
        if isinstance(node, nodes.Getattr):
            yield node.attrname
        elif isinstance(node, nodes.Name):
            yield node.name
        elif isinstance(node, nodes.From):
            yield node.modname


def identify_called_functions(root):
    fs = root.nodes_of_class(nodes.CallFunc)
    for f in fs:
        try:
            history = trace(f.func)
            symbols = list(resolve(history))
            full_name = '.'.join(reversed(symbols))
            yield (f.lineno, f.col_offset, full_name)
        except NotFoundException as ex:
            pass
