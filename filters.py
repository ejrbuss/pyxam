# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import formatter
import lib_loader
import base64
import re
import random


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
            fn(token)
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
        if hasattr(token, 'name') and 'numerical' in token.name:
            to_calculated(token)
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
                    parsed = re.match(r'(.*)=([^tolerance]*)(tolerance(.*))?', solution_token.definition[0].replace(' ', ''))
                    token.definition[0] = parsed.group(2)
                    question.name = 'numerical'
                    logging.info('Converted shortanswer question to numerical')
                    tolerance = parsed.group(4)
                    if tolerance is not None:
                        if tolerance.endswith('\\%'):
                            tolerance = str(float(parsed.group(2)) * (float(tolerance[:-2]) / 100.0))
                        token.definition.insert(1, formatter.Token('tolerance', [tolerance], None, ''))
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


def to_calculated(question):
    """
    Transforms numerical token definitions from
    solution:
        answer
        tolerance:
            tolerance

    to:
    solution:
        answer
        tolerance:
            tolerance
        params:
            param:
                name
                maximum:
                    value
                minimum:
                    value
                decimal:
                    value
                    formatter.Token('tolerance', [tolerance], None, ''))
    :param question:
    :return:
    """
    for token in question.definition:
        if hasattr(token, 'name') and 'solution' in token.name:
            definition = []
            dataset = []
            decimal = 0
            for where, condition in zip(token.definition, token.definition[1:]):
                if where == 'where':
                    try:
                        parsed = re.match(r'(.*)\[(.*)\]', condition.definition[0].replace(' ', ''))
                        items = parsed.group(2).split(',')
                        decimal = max(decimal, max([len(item.split('.')[1]) for item in items if '.' in item]))
                        items = [float(item) for item in items]
                        name = formatter.Token('paramname', [parsed.group(1).replace('{', '').replace('}', '')], None, '')
                        pmax = formatter.Token('parammax', [str(max(items))], None, '')
                        pmin = formatter.Token('parammin', [str(min(items))], None, '')
                        pdec = formatter.Token('paramdec', ['2'], None, '')
                        # Generate a random value
                        count = formatter.Token('itemcount', [str(len(items))], None, '')
                        pitems = formatter.Token('items', [], None, '')
                        for n, item in enumerate(items):
                            pitems.definition.append(formatter.Token('itemnumber', [str(n + 1)], None, ''))
                            pitems.definition.append(formatter.Token('itemvalue', [str(item)], None, ''))
                        dataset.append(formatter.Token('param', [name, pmax, pmin, pdec, count, pitems], None, ''))
                    except:
                        return
                elif not hasattr(where, 'name') or 'tolerance' in where.name:
                    definition.append(where)
            if dataset:
                for n, tolerance in enumerate(definition):
                    if hasattr(tolerance, 'name') and 'tolerance' in tolerance.name:
                        definition.insert(n + 1, formatter.Token('decimal', [str(decimal)], None, ''))
                question.name='calculated'
                logging.info('Converted numerical question to calculated')
                question.definition.append(formatter.Token('params', dataset, None, ''))
                token.definition = definition
                return