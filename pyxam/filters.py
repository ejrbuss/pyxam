# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module filters
This module provides helper functions for transforming a Pyxam parse tree.
"""
import lib_loader
import formatter
import logging
import base64
import re


#TODO finish


def has_name(token, name='', partial=True):
    return hasattr(token, 'name') and (name == token.name or (partial and name in token.name))


def remove_name(ast, name, partial=True):
    logging.info('Paritalfilter for "' + name + '"')
    return recursive_filter(lambda t: not has_name(t, name, partial), ast)


def recursive_filter(fn, node):
    """
    Filters a list and recursively filters any sublists attached to the node.
    :param fn: The filter function
    :param node: The starting node
    :return: the filtered node
    """
    if isinstance(node, list):
        return list(filter(fn, [recursive_filter(fn, n) for n in node]))
    if has_name(node):
        node.definition = list(filter(fn, [recursive_filter(fn, n) for n in node.definition]))
    return node


def apply_function(ast, fn, name='', partial=True):
    """
    Applies a transform function to all nodes of the tre that match the name given. The function is applied recursively
    to every part of the tree.
    :param ast: The tree to transform
    :param fn: The function to apply
    :param partial: TODO
    :return: the modified tre
    """
    for token in ast:
        if has_name(token, name, partial):
            fn(token)
        if has_name(token):
            apply_function(token.definition, fn, name)
    return ast


def pass_through(intermediate):
    """
    A dummy function that simply returns its provided intermediate.
    :param intermediate: The intermediate
    :return: the intermediate
    """
    logging.info('Pass through filter')
    return intermediate


def pop_unknowns(ast):
    """
    Replace every unknown token with the its definition tokens. This process is applied recursively and all popped
    tokens are also processed for unknowns
    :param ast: The tree whose unknowns are being popped
    :return: the modified tree
    """
    if ast is None:
        return
    new_ast = []
    for token in ast:
        if hasattr(token, 'name') and 'unknown' in token.name:
            new_ast += [popped for popped in token.definition if hasattr(popped, 'name') ]
        elif hasattr(token, 'definition'):
            token.definition = pop_unknowns(token.definition)
            new_ast += [token]
        else:
            new_ast += [token]
    if new_ast != ast and new_ast:
        return pop_unknowns(new_ast)
    return new_ast


def img64(ast):
    """
    Convert image file paths to base64 representations of those images.
    :param ast: The tree whose images will be converted
    :return: The modified tree
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
    Combine consecutive string tokens into a single string. Applied recursively.
    :param ast: The tree whose strings tokens are combined
    :return: The modified tree
    """
    new_ast = []
    buffer = ''
    for token in ast:
        if hasattr(token, 'definition'):
            if buffer.strip() != '':
                new_ast.append(buffer.strip())
                buffer = ''
            new_ast.append(token)
            if 'verb' not in token.name:
                token.definition = homogenize_strings(token.definition)
        else:
            buffer += token
    if buffer.strip() != '':
        new_ast.append(buffer.strip())
    return new_ast


def promote(ast, name):
    """
    Finds the first instance (based on a depth first search) of a token with the matching name.
    :param ast: The tree to be searched
    :param name: The token name to find
    :return: the subtree starting at the matching token
    """
    logging.info('Promotion filter for "' + name + '"')
    for token in ast:
        if hasattr(token, 'name') and token.name == name:
            return [token]
    return promote(sum([token.definition for token in ast if hasattr(token, 'definition')], []), name)


def wrap_lists(ast):
    """
    Wraps consecutive listitem tokens in a list token. Applied recursively.
    :param ast: The tree to be modified
    :return: The modified tree
    """
    new_ast = []
    buffer = []
    for token in ast:
        if hasattr(token, 'definition'):
            wrap_lists(token.definition)
        if hasattr(token, 'name') and 'listitem' in token.name:
            buffer.append(token)
        else:
            if buffer:
                new_ast.append(formatter.Token('list', buffer, None, ''))
                buffer = []
            new_ast.append(token)
    if buffer:
        new_ast.append(formatter.Token('list', buffer, None, ''))
    return new_ast


def untab_verb(ast):
    """
    :param ast: The tree to modify
    :return: the modified tree
    """
    def untab(token):
        lines = [line for line in token.definition[0].split('\n') if line != '\n']
        overwrite = False
        while not overwrite:
            clear = True
            for line in lines:
                clear = not len(line) > 0 and clear
                overwrite = overwrite or (len(line) > 0 and (line[0] != ' '))
            overwrite = overwrite or clear
            if not overwrite:
                lines = [line[1:] for line in lines if len(line) > 0]
        token.definition = ['\n'.join(lines)]
    return apply_function(ast, untab, 'verb')


def transform_questions(ast):
    """
    Performs a number of transformations to questions in the tree. These include converting shortanswer questions to
    numerical questions, multichoice questions to multiselect questions, and numerical questions to calculated
    questions. Applied recursively.
    :param ast: The tree to modify
    :return: the modified tree
    """
    for token in ast:
        if has_name(token, 'shortanswer'):
            check_tag(token)
        if has_name(token, 'multichoice'):
            to_multiselect(token)
        elif has_name(token):
            token.definition = transform_questions(token.definition)
    return ast


def check_tag(question):
    """
    Transforms shortanswer token definitions from
    ```
    solution:
        $:
            var = answer \pm tolerance
    ```
    to
    ```
    solution:
        answer
        tolerance:
            tolerance
    ```
    :param question: The question to transform
    """
    for token in question.definition:
        if has_name(token, 'solution'):
                if has_name(token.definition[0], 'pyxamnumerical', partial=False):
                    question.name = 'numerical'
                if has_name(token.definition[0], 'pyxamcalculated', partial=False):
                    question.name = 'calculated'


def to_multiselect(question):
    """
    Transforms multichoice token definitions from
    ```
    choices:
        correctchoice:
            choice
        correctchoice:
            choice
    ```
    to
    ```
    single: false
    choices:
        correctchoice:
            choice
        correctchoice:
            choice
    ```
    :param question: The question to transform
    """
    for token in question.definition:
        count = 0
        if has_name(token, 'choices'):
            for choice in token.definition:
                if has_name(choice, 'correctchoice'):
                    count += 1
        if count > 1:
            question.name = 'multiselect'
            logging.info('Converted multichoice question to multiselect')

