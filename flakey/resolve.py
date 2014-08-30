from astroid import nodes


def find(scope):
    return (f.func for f in scope.nodes_of_class(nodes.CallFunc))

def find_name(scope, func_node):
    node = func_node
    while node:
        if isinstance(node, nodes.Name):
            return node
        if isinstance(node, nodes.Getattr):
            node = node.expr
            continue
        else:
            return None


def resolve(name_node):
    scope, assignments = name_node.lookup(name_node.name)
    
