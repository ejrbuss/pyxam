# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module formatter

This module
"""
import re
import util
import config
import options
import filters
import fileutil
import collections

# TODO finish


class FormatError(Exception):
    """
    Exception wrapper for format errors
    """
    pass


def str_token(token):
    """

    :param token:
    :return:
    """
    if isinstance(token, list):
        return ''.join(str_token(t) for t in token)
    if isinstance(token, str):
        return token
    return '\n' + token.name + ':\n\t' + ''.join(str_token(child).replace('\n', '\n\t') for child in token.definition) + '\n'


formats = {}


def get_extension():
    """
    Get the file extension of the output format.

    :return: The output extension
    """
    return formats[options.state.format()]['extensions'][0]


def get_format(file):
    """
    Get the format of the given file. Format is based on file extension.

    :param file: The file to find the format of
    :return: The format of the given file
    """
    try:
        return formats[fileutil.get_extension(file)]
    except:
        raise FormatError('Unknown format')


def parse():
    """
    source to ast
    :return:
    """
    intermediates, parser = [], get_format(options.state.template())
    if not parser['format']:
        raise FormatError('This format is export only!')
    # Loop through all weaved files
    for file in fileutil.with_extension('.tex'):
        options.post('Using ' + parser['name'] + ' format to parse ' + file)
        intermediate = util.Map({
            'ast': [],
            'src': parser['parser_preprocessor'](fileutil.read(file)),
            'fmt': parser,
            'name': file.replace('.tex', '')
        })
        intermediate.ast = parse_tokens(intermediate.src, parser)
        for default_filter in config.default_filters:
            intermediate.ast = default_filter(intermediate.ast)
        intermediate = parser['parser_postprocessor'](intermediate)
        intermediates.append(intermediate)
        fileutil.write(options.state.cwd() + '/parsed-ast', ''.join(str_token(intermediate.ast)))
    options.post('Successfully parsed', parser['name'] + '.')
    return intermediates


def compose(intermediates):
    """
    ast to source
    :param intermediates:
    :return:
    """
    try:
        composer = formats[options.state.format()]
    except:
        raise FormatError('Unknown format')
    for intermediate in intermediates:
        composed = intermediate.src
        # If not already in native format
        if intermediate.fmt != composer:
            intermediate = composer['composer_preprocessor'](intermediate)
            fileutil.write(options.state.cwd() + '/composed-ast', ''.join(str_token(intermediate.ast)))
            composed = ''.join([pack(token, composer) for token in intermediate.ast]).strip()
        composed = composer['composer_postprocessor'](composed)
        fileutil.write(intermediate.name + '.cmp', composed)
    options.post('Successfully composed', composer['name'] + '.')


def pack(token, fmt):
    """
    Convert a token into a string using the following rules:
    - If the token name is contained in the format:
        - Append every pure string in that format
        - Append every tuple or list as the packed content of the token
    - If the token name is not contained in the format
        - Append the packed content of the token
    :param token:
    :param fmt:
    :return:
    """
    if isinstance(token, str):
        return token
    content = ''
    for symbol in (fmt['format'][token.name].definition[:-1] if token.name in fmt['format'] else [()]):
        if isinstance(symbol, str):
            content += symbol
        if isinstance(symbol, tuple) or isinstance(symbol, list):
            content += ''.join(pack(child, fmt) for child in token.definition)
            token.definition = []
    return content


def add_format(name,
               extensions,
               format,
               description='',
               parser_preprocessor=lambda _: _,
               parser_postprocessor=lambda _: _,
               composer_postprocessor=lambda _: _,
               composer_preprocessor=lambda _: _,
               left_paren=None,
               right_paren=None
):
    """

    :param name:
    :param extensions:
    :param description:
    :param format:
    :param parser_preprocessor:
    :param parser_postprocessor:
    :param composer_postprocessor:
    :param composer_preprocessor:

    :return:
    """
    format.update(collections.OrderedDict([
        ('pyxamnumerical', [':pyxam.numerical', '.']),
        ('pyxamcalculated', [':pyxam.calculated', '.'])
    ]))
    fmt = {
        'name': name,
        'extensions': extensions + [name],
        'description': description,
        'parser_preprocessor': parser_preprocessor,
        'parser_postprocessor': parser_postprocessor,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': composer_postprocessor,
        'left_paren': left_paren,
        'right_paren': right_paren,
        'format': format
    }
    formats.update(dict((extension, fmt) for extension in fmt['extensions']))
    fmt['format'] = collections.OrderedDict([
        (name, util.Map({'name': name, 'definition': definition})) for name, definition in fmt['format'].items()
    ])


def parse_tokens(src, fmt):
    """
    Convert a string source into an abstract syntax tree (ast). A format containing a list of valid
    tokens must be provided. Any string sequences that cannot be matched will be returned as
    raw characters
    :param src: The source to convert into an ast
    :param fmt: The format providing the tokens
    :return: The ast
    """
    ast, unmatched = [], src
    while unmatched:
        token, unmatched = match_token(unmatched, fmt)
        ast.append(token)
    return ast


def match_token(src, fmt):
    """
    Determine what token a specific string sequence begins with. If no token can be found in the given
    template a raw character is returned off the top.
    :param src: The string sequence
    :param fmt: The format providing the tokens
    :return: The matched token, The unmatched sequence
    """
    for token in fmt['format'].values():
        matched, unmatched = build_token(token, src, fmt)
        if matched is not None:
            return matched, unmatched
    return src[0], src[1:]


def build_token(token, src, fmt):
    """

    :param token:
    :param src:
    :param fmt:
    :param debug:
    :return:
    """
    definition, unmatched, packing = [], src, False
    for symbol in token.definition[:-1]:
        if packing:
            matched, parentheses = '', 0
            while packing:
                # No match
                if not unmatched:
                    return None, src
                # If token we don't care what parentheses level we are in
                elif isinstance(symbol, list):
                    for sub_token in symbol:
                        child, unmatched = build_token(fmt['format'][sub_token], unmatched, fmt)
                        if child is not None:
                            definition += parse_tokens(matched, fmt)
                            definition.append(child)
                            packing = False
                            break
                    else:
                        matched, unmatched = increment(matched, unmatched)
                # Move down a parentheses level
                elif fmt['left_paren'] is not None and unmatched.startswith(fmt['left_paren']):
                    parentheses += 1
                    matched, unmatched = increment(matched, unmatched)
                # If nested move back up a parentheses level
                elif parentheses != 0 and unmatched.startswith(fmt['right_paren']):
                    parentheses -= 1
                    matched, unmatched = increment(matched, unmatched)
                # If parentheses are not balanced consume character
                elif parentheses != 0:
                    matched, unmatched = increment(matched, unmatched)
                # If at the end of content
                elif isinstance(symbol, str) and unmatched.startswith(symbol):
                    definition += [matched] if filters.has_name(token, ['$', 'verb', 'comment']) else parse_tokens(matched, fmt)
                    unmatched = unmatched[len(symbol):]
                    packing = False
                # If not at the end of content
                elif isinstance(symbol, str):
                    matched, unmatched = increment(matched, unmatched)
                # No match
                else:
                    return None, src
        # If str
        elif isinstance(symbol, str) and unmatched.startswith(symbol):
            unmatched = unmatched[len(symbol):]
        # If token
        elif isinstance(symbol, list):
            for sub_token in symbol:
                child, unmatched = build_token(fmt['format'][sub_token], unmatched, fmt)
                if child is not None:
                    definition.append(child)
                    break
            else:
                return None, src
        # If content
        elif isinstance(symbol, tuple):
            packing = True
        # No match
        else:
            return None, src
    # If exited before packing
    if packing:
        matched, parentheses = '', 0
        while packing:
            # End of string
            if len(unmatched) == 0:
                definition += [matched] if ('$' or 'verbatim' or 'comment') in token.name else parse_tokens(matched, fmt)
                packing = False
            # Move down a parentheses level
            elif fmt['left_paren'] is not None and unmatched.startswith(fmt['left_paren']):
                parentheses += 1
                matched, unmatched = increment(matched, unmatched)
            # If nested move back up a parentheses level
            elif parentheses != 0 and unmatched.startswith(fmt['right_paren']):
                parentheses -= 1
                matched, unmatched = increment(matched, unmatched)
            # If parentheses are not balanced consume character
            elif parentheses != 0:
                matched, unmatched = increment(matched, unmatched)
            # If at the end of content
            elif re.match(r'^\s*(({})|$).*'.format(token.definition[-1]), unmatched, re.DOTALL):
                definition += [matched] if filters.has_name(token, ['$', 'verb', 'comment']) else parse_tokens(matched, fmt)
                packing = False
            # If not at the end of content
            else:
                matched, unmatched = increment(matched, unmatched)
    # Check if ending regex matches
    if unmatched == '' or re.match(r'^\s*(({})|$).*'.format(token.definition[-1]), unmatched, re.DOTALL):
        return util.Map({'name': token.name, 'definition': definition}), unmatched
    return None, src


def increment(matched, unmatched):
    """

    :param matched:
    :param unmatched:
    :return:
    """
    return matched + unmatched[0], unmatched[1:]









