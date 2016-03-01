# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import formatter
import re


MAX_NESTED = 16


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
    These tokens to are processed.
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
            question.type = 'multiselect'
            logging.info('Converted multichoice question to multiselect')


def make_nested(regex, src):
    """
    Transform a regex to deal with nested brackets. Handles {}, (), and [].
    Has a maximum depth of MAX_NESTED which can be specified at the top of the file.
    Warning depths past 100 are not supported by the python regex module.

    Minimum nesting is calculated by a heuristic approach, nesting equal to the number of brackets in the source
    string is assumed safe.

    Regex patterns that are modified are: \{(.*?)\} - \((.*?)\) - \[(.*?)\]


    :param regex: The regex to modify if necesary
    :param src: The source string
    :return: The modified regex
    """
    if '\{(.*?)\}' in regex:
        regex = regex.replace('\{(.*?)\}', '\{(([^{}]*)|($))*\}')
        for i in range(min(src.count('}'), MAX_NESTED)):
            regex = regex.replace('($)', '\{(([^{}]*)|($))*\}')
    elif '\((.*?)\)' in regex:
        regex = regex.replace('\((.*?)\)', '\((([^()]*)|($))*\)')
        for i in range(min(src.count(')'), MAX_NESTED)):
            regex = regex.replace('($)', '\((([^()]*)|($))*\)')
    elif '\[(.*?)\]' in regex:
        regex = regex.replace('\[(.*?)\]', '\[(([^[]]*)|($))*\]')
        for i in range(min(src.count(']'), MAX_NESTED)):
            regex = regex.replace('($)', '\[(([^[\]]*)|($))*\]')
    else:
        return regex
    return regex


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