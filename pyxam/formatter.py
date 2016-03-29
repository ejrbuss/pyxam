# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module formatter
"""
import logging
import re
import filters
import collections
import libs
import options
import fileutil

# TODO cleanup
# TODO formatting


class FormatError(Exception):
    pass


class Token:

    def __init__(self, name, definition, fmt, regex=None):
        self.name = name
        self.definition = definition
        self.regex = unpack(definition, fmt) if regex is None else regex

    def package(self, fmt):
        try:
            return ''.join(pack(child, fmt) for child in self.definition)
        finally:
            self.definition = []

    def __repr__(self):
        return '\n' + self.name + ':\n\t' + ''.join(str(child).replace('\n', '\n\t') for child in self.definition) + '\n'


formats = {}


def get_extension():
    """
    Get the output extension
    :return: The output extension
    """
    return formats[options.state.format()]['extensions'][1]


def parse():
    """
    source to ast
    :return:
    """
    global formats
    intermediates = []
    try:
        parser = formats[options.state.template().split('.')[-1]]
    except:
        raise FormatError('Unknown format')
    for file in fileutil.with_extension('.tex'):
        logging.info('Using ' + parser['extensions'][0] + ' format to parse ' + options.state.template())
        intermediate = libs.map.Map({'ast': [], 'src': parser['parser_preprocessor'](fileutil.read(file)), 'fmt': parser})

        intermediate.ast = resolve(intermediate.src, parser)
        fileutil.write(options.state.cwd() + '/parsed-ast', str(''.join(str(token) for token in intermediate.ast)))
        # Remove comments
        intermediate.ast = filters.remove_partial(intermediate.ast, 'comment')
        # Pop unknowns
        intermediate.ast = filters.pop_unknowns(intermediate.ast)
        # Homogenize strings
        intermediate.ast = filters.homogenize_strings(intermediate.ast)
        # Transform questions
        intermediate.ast = filters.transform_questions(intermediate.ast)
        intermediate = parser['parser_postprocessor'](intermediate)
        intermediates.append(intermediate)
        fileutil.write(options.state.cwd() + '/parsed-ast', str(''.join(str(token) for token in intermediate.ast)))
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
    logging.info('Using ' + composer['extensions'][0] + ' format to compose ' + options.state.template())
    for n, intermediate in enumerate(intermediates):
        composed = intermediate.src
        # If not already in native format
        if intermediate.fmt != composer:
            intermediate = composer['composer_preprocessor'](intermediate)
            fileutil.write(options.state.cwd() + '/composed-ast', str(intermediate.ast))
            composed = ''.join([pack(token, composer) for token in intermediate.ast]).strip()
        composed = composer['composer_postprocessor'](composed)
        fileutil.write(options.state.cwd() + '/composed_' + str(n) + '.cmp', composed)


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
            content += token.package(fmt)
    return content


def add_format(name,
               extensions,
               format,
               description='',
               parser_preprocessor=filters.pass_through,
               parser_postprocessor=filters.pass_through,
               composer_postprocessor=filters.pass_through,
               composer_preprocessor=filters.pass_through
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
    if (
            'extensions' and 'description' and 'format' and
            'parser_preprocessor' and 'parser_postprocessor' and
            'composer_preprocessor' and 'composer_postprocessor'
    ) in fmt:
        formats.update(dict((extension, fmt) for extension in fmt['extensions']))
        fmt['format'] = collections.OrderedDict([(name, Token(name, defn, fmt['format'])) for name, defn in fmt['format'].items()])
    else:
        raise FormatError('Invalid signature for format')


def unpack(token, fmt, tail=False):
    """
    Convert format list to a regex using the following rules:
    - Convert pure strings to pure strings within the regex with all regex characters escapted
    - Convert empty tuples to non-greedy character grabbers (.*?)
    - Convert lists to recursively obtain the regex of the token contained within that list
    - Throw an error for any other input
    If a tail prefix the regex with a start of string whitespace regex and append a end of string or
    the last entry in the format list regex
    :param token: The token to build the regex for
    :param fmt: The reference format
    :param tail: Whether the regex should have a prefix and postfix applied
    :return: The regex
    """
    regex = r''
    for symbol in token[:-1]:
        if isinstance(symbol, tuple):
            regex += r'(.*?)' if len(symbol) < 1 else symbol[0]
        elif isinstance(symbol, str):
            regex += re.escape(symbol)
        elif isinstance(symbol, list):
            regex += unpack(fmt[symbol[0]], fmt, tail=True)
        else:
            raise FormatError('Cannot unpack token: ' + token)
    return regex if tail else (r'(^\s*' + regex + ')(?=\s*(' + token[-1] + ')|$)').replace('\ ', '\s*')


def resolve(src, fmt):
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
        token, unmatched = determine(unmatched, fmt)
        ast.append(token)
    return ast


def determine(src, fmt):
    """
    Determine what token a specific string sequence begins with. If no token can be found in the given
    template a raw character is returned off the top.
    :param src: The string sequence
    :param fmt: The format providing the tokens
    :return: The matched token, The unmatched sequence
    """
    for token in fmt['format'].values():
        matched, unmatched = check(token, src, fmt)
        if matched is not None:
            return matched, unmatched
    return src[0], src[1:]


def check(token, src, fmt, debug=False):
    """

    :param token:
    :param src:
    :param fmt:
    :param debug:
    :return:
    """
    definition, unmatched, post = [], src, False
    # Nested parentheses counter
    parens = 0
    if debug: print('SRC:\n',src)
    for symbol in token.definition[:-1]:
        if debug: print('\tPROCESSING SYMBOL:',symbol)
        # If post
        if post:
            # Matched content
            matched = ''
            # While there are unmatched characters
            while post:
                # No match
                if len(unmatched) == 0:
                    return None, src
                # If token
                elif isinstance(symbol, list):
                    for sub_token in symbol:
                        if debug: print('\t\t\tCHECKING SUBTOKEN: [', symbol[0], ']')
                        child, unmatched = check(fmt['format'][sub_token], unmatched, fmt)
                        if debug: print('\t\t\tRETURNED:',str(child).replace('\n', '\n\t\t\t\t'))
                        if child is not None:
                            if debug: print('\t\tEND OF POST',child)
                            definition += resolve(matched, fmt)
                            definition.append(child)
                            post = False
                            break
                    else:
                        matched += unmatched[0]
                        unmatched = unmatched[1:]
                # Move down a parentheses level
                elif 'left_paren' in fmt and unmatched.startswith(fmt['left_paren']):
                    if debug: print('\t\t\tCONSUMED:', unmatched[0])
                    parens += 1
                    matched += unmatched[0]
                    unmatched = unmatched[1:]
                # If nested move back up a parentheses level
                elif 'right_paren' in fmt and parens != 0 and unmatched.startswith(fmt['right_paren']):
                    if debug: print('\t\t\tCONSUMED:', unmatched[0])
                    parens -= 1
                    matched += unmatched[0]
                    unmatched = unmatched[1:]
                # If parentheses are not balanced consume character
                elif parens != 0:
                    matched += unmatched[0]
                    unmatched = unmatched[1:]
                # If at the end of content
                elif isinstance(symbol, str) and unmatched.startswith(symbol):
                    if debug: print('\t\tEND OF POST:',symbol)
                    definition += [matched] if \
                        '$' in token.name or \
                        'verb' in token.name or \
                        'comment' in token.name in token.name \
                        else resolve(matched, fmt)
                    unmatched = unmatched[len(symbol):]
                    post = False
                # If not at the end of content
                elif isinstance(symbol, str):
                    if debug: print('\t\t\tCONSUMED:', unmatched[0])
                    matched += unmatched[0]
                    unmatched = unmatched[1:]
                # No match
                else:
                    return None, src

        # If str
        elif isinstance(symbol, str) and unmatched.startswith(symbol):
            if debug: print('\t\tREMOVEING:',symbol)
            unmatched = unmatched[len(symbol):]
        # If token
        elif isinstance(symbol, list):
            for sub_token in symbol:
                if debug: print('\t\tCHECKING SUBTOKEN: [', sub_token, ']')
                child, unmatched = check(fmt['format'][sub_token], unmatched, fmt)
                if debug: print('\t\t\tRETURNED:',str(child).replace('\n', '\n\t\t\t'))
                if child is not None:
                    definition.append(child)
                    break
            else:
                return None, src
        # If content
        elif isinstance(symbol, tuple):
            if debug: print('\t\tENTERING POST')
            post = True
        # No match
        else:
            return None, src

    # If exited on post
    if post:
        # Nested parentheses counter
        parens = 0
        # Matched content
        matched = ''
        # While there are unmatched characters
        while post:
            # End of string
            if len(unmatched) == 0:
                definition += [matched] if ('$' or 'verbatim' or 'comment') in token.name else resolve(matched, fmt)
                post = False
            # Move down a parentheses lvel
            elif 'left_paren' in fmt and unmatched.startswith(fmt['left_paren']):
                parens += 1
                matched += unmatched[0]
                unmatched = unmatched[1:]
            # If nested move back up a parentheses level
            elif 'right_paren' in fmt and parens != 0 and unmatched.startswith(fmt['right_paren']):
                parens -= 1
                matched += unmatched[0]
                unmatched = unmatched[1:]
            # If parentheses are not balanced consume character
            elif parens != 0:
                matched += unmatched[0]
                unmatched = unmatched[1:]
            # If at the end of content
            elif re.match(r'^\s*(({})|$).*'.format(token.definition[-1]), unmatched, re.DOTALL):
                definition += [matched] if \
                        '$' in token.name or \
                        'verb' in token.name or \
                        'comment' in token.name in token.name \
                        else resolve(matched, fmt)
                post = False
            # If not at the end of content
            else:
                matched += unmatched[0]
                unmatched = unmatched[1:]
    # Check if ending regex matches
    if unmatched == '' or re.match(r'^\s*(({})|$).*'.format(token.definition[-1]), unmatched, re.DOTALL):
        return Token(token.name, definition, fmt, ''), unmatched
    return None, src











