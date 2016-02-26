def remove_name(ast, name):
    return recursive_filter(lambda i: not (hasattr(i, 'name') and i.name.startswith(name)), ast)


def recursive_filter(fn, node):
    if isinstance(node, list):
        return list(filter(fn, [recursive_filter(fn, n) for n in node]))
    if hasattr(node, 'definition'):
        node.definition = list(filter(fn, [recursive_filter(fn, n) for n in node.definition]))
    return node


def promote_nested(src, cmd, left, right):
    i = 0
    while i < len(src):
        i += 1
        if src[i:].startswith(cmd + left):
            count = 1
            for j in range(len(src[i:]) - len(cmd + left)):
                k = i + j + len(cmd + left)
                if src[k] == left:
                    count += 1
                if src[k] == right:
                    count -= 1
                if count == 0:
                    src = src[:i] + src[i + len(cmd + left): k] + src[k:]
                    break
    return src