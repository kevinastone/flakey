# coding: utf-8
from astroid import nodes, scoped_nodes, YES


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
    trace(node.func, context)
    if context and isinstance(context[-1], scoped_nodes.Function):
        func_node = context[-1]
        for return_node in func_node.nodes_of_class(nodes.Return):
            sub_context = ctx[:]
            result = trace(return_node.value, sub_context)
            if result:
                return result
    return context


def lookup_assignment(node, ctx):
    ctx.pop()
    # return node.statement()
    assign = node.parent
    if isinstance(assign, nodes.Assign):
        return assign.value
    else:
        return node.infered()[0]
    # return assign.value


def trace(node, ctx=None):  # flake8: noqa
    if ctx is None:
        ctx = []
    if isinstance(node, nodes.Getattr):
        ctx.append(node)
        return trace(node.expr, ctx)
    elif isinstance(node, nodes.AssName):
        return trace(lookup_assignment(node, ctx), ctx)
    elif isinstance(node, nodes.Name):
        ctx.append(node)
        return trace(lookup(node), ctx)
    elif isinstance(node, nodes.From):
        ctx.append(node)
        return ctx
    elif isinstance(node, nodes.Import):
        return ctx
    elif isinstance(node, scoped_nodes.Function) or isinstance(node, scoped_nodes.Lambda):
        ctx.append(node)
        return ctx
    elif isinstance(node, scoped_nodes.Class):
        return ctx
    elif isinstance(node, nodes.CallFunc):
        return lookup_call(node, ctx)
    elif node is YES:
        return ctx
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


def identify_called_functions(root, func=None):
    fs = root.nodes_of_class(nodes.CallFunc)
    for f in fs:
        try:
            history = trace(lookup(f))
            symbols = list(resolve(history))
            full_name = '.'.join(reversed(symbols))
            yield (f.lineno, f.col_offset, full_name)
        except NotFoundException:
            pass
