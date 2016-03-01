# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import re
import filters
import collections
import libs
import options
import fileutil

# TODO cleanup
# TODO replace seperator with a better scheme


class FormatError(Exception):
    pass


class Token:

    def __init__(self, name, definition, fmt, regex=None):
        self.name = name
        self.definition = definition
        self.regex = unpack(definition, fmt) if regex is None else regex

    @classmethod
    def instance(cls, token, src, fmt):
        source = token.remove(src, fmt)
        definition = []
        if token.name == '$':
            return Token(token.name, [source], fmt, '')
        while source:
            child, source = match(fmt, source)
            definition.append(child)
        return Token(token.name, definition, fmt, '')

    def remove(self, source, format_):
        for symbol in self.definition[:-1]:
            source = filters.token_replace(symbol, source)
        return source

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
        stack = intermediate.src
        while stack:
            token, stack = match(parser, stack)
            intermediate.ast.append(token)
        # Remove comments
        intermediate.ast = filters.remove_name(intermediate.ast, 'comment')
        # Pop unknowns
        intermediate.ast = filters.pop_unknowns(intermediate.ast)
        # Transform questions
        intermediate.ast = filters.transform_questions(intermediate.ast)
        intermediate = parser['parser_postprocessor'](intermediate)
        intermediates.append(intermediate)
        fileutil.write('parsed-ast', str(''.join(str(token) for token in intermediate.ast)))
    return intermediates


def match(parser, src):
    """
    Match a string to the Tokens in a parser.
    If no Token is matched one character is returned as a pure string
    :param parser: The parser containing matchable tokens
    :param src: The string to match
    :return: The Token or pure string, The remaining unmatched string
    """
    for token in parser['format'].values():
        regex = filters.make_nested(token.regex, src)
        if re.match(regex, src, re.DOTALL):
            token_src = re.match(regex, src, re.DOTALL).group(0)
            return Token.instance(token, token_src, parser), src.replace(token_src, '', 1).strip()
    return src[0], src[1:]


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
            fileutil.write('composed-ast', str(intermediate.ast))
            composed = ''.join([pack(token, composer) for token in intermediate.ast]).strip()
            composed = composer['composer_postprocessor'](composed)
        fileutil.write('composed_' + str(n) + '.cmp', composed)
    logging.info('compose')


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


def add_format(fmt):
    """
    Check format signature before adding.
    Insert into formats at all valid extensions.
    Convert format list to Token list.
    :param fmt: The format map
    :return: None
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