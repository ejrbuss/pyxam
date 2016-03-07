# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import formatter
import lib_loader
import base64
import re


def remove_name(ast, name):
    """
    Remove all tokens with a given name along with all their sub tokens
    :param ast: The ast to walk
    :param name: The name of the token to remove
    :return: The new ast
    """
    logging.info('Name filter for "' + name + '"')
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


def apply_function(ast, fn, name):
    """

    :param ast:
    :param fn:
    :param name:
    :return:
    """
    for token in ast:
        if hasattr(token, 'name') and token.name == name:
            token.definition[0] = fn(token.definition[0])
        if hasattr(token, 'definition'):
            apply_function(token.definition, fn, name)
    return ast

def pass_through(intermediate):
    """
    A dummy function that simply returns its provided intermediate
    :param intermediate: The intermediate
    :return: The intermediate
    """
    logging.info('Pass through filter')
    return intermediate


def pop_unknowns(ast):
    """
    Replace every unknown token with the its definition tokens.
    These tokens too are processed.
    :param ast: The ast whose unknowns are being popped
    :return: The modified ast
    """
    new_ast = []
    for token in ast:
        if hasattr(token, 'name') and 'unknown' in token.name:
            new_ast += [popped for popped in token.definition if hasattr(popped, 'name') ]
        elif hasattr(token, 'definition'):
            token.definition = pop_unknowns(token.definition)
            new_ast += [token]
        else:
            new_ast += [token]
    if new_ast != ast:
        return pop_unknowns(new_ast)
    return new_ast


def img64(ast):
    """
    Convert pdf file paths to base64 representations of those images.
    :param ast: The ast whose images will be modifed
    :return: The modified ast
    """
    for token in ast:
        if hasattr(token, 'definition'):
            img64(token.definition)
        if hasattr(token, 'name') and 'img' in token.name:
            with open(lib_loader.gs(token.definition[0]), 'rb') as data:
                token.definition = [base64.b64encode(data.read()).decode()]
    return ast


def homogenize_strings(ast):
    """
    Combine consecutive string tokens into a single string.
    :param ast: The ast whose strings tokens are combined
    :return: The modified ast
    """
    new_ast = []
    buffer = ''
    for token in ast:
        if hasattr(token, 'definition'):
            if buffer.strip() != '':
                new_ast.append(buffer.strip())
                buffer = ''
            new_ast.append(token)
            token.definition = homogenize_strings(token.definition)
        else:
            buffer += token
    if buffer != '':
        new_ast.append(buffer.strip())
    return new_ast


def promote(ast, name):
    """
    Return the first instance (based on a depth search) of a token as a new ast.
    :param ast: The ast to be searched
    :param name: The name of the token to promote
    :return: The modified ast
    """
    logging.info('Promotion filter for "' + name + '"')
    for token in ast:
        if hasattr(token, 'name') and token.name == name:
            return [token]
    return promote(sum([token.definition for token in ast if hasattr(token, 'definition')], []), name)


def transform_questions(ast):
    for token in ast:
        if hasattr(token, 'name') and 'shortanswer' in token.name:
            to_numerical(token)
        if hasattr(token, 'name') and 'multichoice' in token.name:
            to_multiselect(token)
        elif hasattr(token, 'definition'):
            token.definition = transform_questions(token.definition)
    return ast


def to_numerical(question):
    """
    Transforms shortanswer token definitions from
    solution:
        $:
            var = answer \pm tolerance

    to

    solution:
        answer
        tolerance:
            tolerance

    :param question: The question to transform
    :return: None
    """
    for token in question.definition:
        if hasattr(token, 'name') and 'solution' in token.name:
            for solution_token in token.definition:
                try:
                    parsed = re.match(r'(\w|\.)*\s*=\s*([\d.]*)\s*(\\pm\s*([\d.]*))?', solution_token.definition[0].strip())
                    token.definition = [parsed.group(2)]
                    question.name = 'numerical'
                    logging.info('Converted shortanswer question to numerical')
                    if parsed.group(4) is not None:
                        token.definition.append(formatter.Token('tolerance', [parsed.group(4)], None, ''))
                except:
                    return


def to_multiselect(question):
    """
    Transforms multichoice token definitions from
    choices:
        correctchoice:
            choice
        correctchoice:
            choice

    to
    single: false
    choices:
        correctchoice:
            choice
        correctchoice:
            choice

    :param question: The question to transform
    :return: None
    """
    for token in question.definition:
        count = 0
        if hasattr(token, 'name') and 'choices' in token.name:
            for choice in token.definition:
                if hasattr(choice, 'name') and 'correctchoice' in choice.name:
                    count += 1
        if count > 1:
            question.name = 'multiselect'
            logging.info('Converted multichoice question to multiselect')


def reverse_replace(src, old, new, count):
    """
    A reverse replace function.
    :param src: The source to replace
    :param old: The old string
    :param new: The new string
    :param count: The number of replacements
    :return: The replaced string
    """
    return new.join(src.rsplit(old, count))


def token_replace(symbol, src):
    """
    Performs the correct replace for a given token symbol on a string.
    :param symbol: The symbol to remove
    :param src: The token source
    :return: The replaced source
    """
    if isinstance(symbol, str):
        if ('}' or ']' or ')') == symbol:
            src = reverse_replace(src, symbol, '', 1)
        else:
            src = src.replace(symbol, '', 1)
    return src