# Author: Eric Buss <ebuss@ualberta.ca> 2016


def remove_name(ast, name):
    """
    Remove all tokens with a given name along with all their sub tokens
    :param ast: The ast to walk
    :param name: The name of the token to remove
    :return: The new ast
    """
    return recursive_filter(lambda t: not (hasattr(t, 'name') and name in t.name), ast)


def recursive_filter(fn, node):
    """
    Return a filtered list that is filtered recursively at every sublist.
    :param fn: The filter function
    :param node: The starting node
    :return: The filtered node
    """
    if isinstance(node, list):
        return list(filter(fn, [recursive_filter(fn, n) for n in node]))
    if hasattr(node, 'definition'):
        node.definition = list(filter(fn, [recursive_filter(fn, n) for n in node.definition]))
    return node


def pass_through(intermediate):
    """
    A dummy function that simply returns its provided intermediate
    :param intermediate: The intermediate
    :return: The intermediate
    """
    return intermediate


def promote_nested(src, cmd, left, right):
    """
    Remove a given command and promote its nested arguments to its place in a string.
    :param src: The source where the promotion will occur
    :param cmd: The command to remove
    :param left: A symbol representing the left side of the argument
    :param right: A symbol representing the right side of the argument
    :return: The source with the changes made
    """
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