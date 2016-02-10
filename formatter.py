import logging
import re
from collections import OrderedDict
from libs.map import Map
from options import state
from fileutil import read
from fileutil import write
from fileutil import with_extension

# TODO cleanup


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
        while source:
            child, source = match(fmt, source)
            definition.append(child)
        return Token(token.name, definition, fmt, '')

    def remove(self, source, format_):
        for symbol in self.definition:
            if isinstance(symbol, str):
                source = source.replace(symbol, '')
        return source

    def package(self, fmt):
        try:
            return ''.join(pack(child, fmt) for child in self.definition)
        finally:
            self.definition = []

    def __repr__(self):
        return '\n' + self.name + ':\n\t' + ''.join(str(child).replace('\n', '\n\t') for child in self.definition)


_formats = {}


def replace(file):
    try:
        parser = _formats[state.format()]
    except:
        raise FormatError('Unknown format')


def get_extension():
    return _formats[state.format()]['extensions'][1]


def parse():
    global _formats
    intermediates = []
    try:
        parser = _formats[state.template().split('.')[-1]]
    except:
        raise FormatError('Unknown format')
    for file in with_extension('.tex'):
        logging.info('Using ' + parser['extensions'][0] + ' format to parse ' + state.template())
        intermediate = Map({'ast': [], 'src': parser['parser_preprocessor'](read(file)), 'fmt': parser})
        stack = intermediate.src
        while stack:
            token, stack = match(parser, stack)
            intermediate.ast.append(token)
        write('parsed-ast', str(''.join(str(token) for token in intermediate.ast)))
        intermediates.append(parser['parser_postprocessor'](intermediate))
    return intermediates


def match(parser, src):
    for token in parser['format'].values():
        if re.match(token.regex, src, re.DOTALL):
            token_src = re.match(token.regex, src, re.DOTALL).group(0)
            return Token.instance(token, token_src, parser), src.replace(token_src, '', 1).strip()
    return src[0], src[1:]


def compose(intermediates):
    try:
        composer = _formats[state.format()]
    except:
        raise FormatError('Unknown format')
    for n, intermediate in enumerate(intermediates):
        composed = intermediate.src
        if intermediate.fmt != composer:
            intermediate = composer['composer_preprocessor'](intermediate)
            write('composed-ast', str(intermediate.ast))
            composed = ''.join([pack(token, composer) for token in intermediate.ast])
            composed = composer['composer_postprocessor'](composed)
        write('composed_' + str(n) + '.cmp', composed)
    logging.info('compose')


def pack(token, fmt):
    if isinstance(token, str):
        return token
    if token.name == 'comment' or token.name.startswith('unknown'):
        return ''
    content = ''
    for symbol in (fmt['format'][token.name].definition[:-1] if token.name in fmt['format'] else [()]):
        if isinstance(symbol, str):
            content += symbol
        if isinstance(symbol, tuple) or isinstance(symbol, list):
            content += token.package(fmt)
    return content


def add_format(fmt):
    try:
            _formats.update(dict((extension, fmt) for extension in fmt['extensions']))
            fmt['format'] = OrderedDict([(name, Token(name, defn, fmt['format'])) for name, defn in fmt['format'].items()])
    except:
        raise FormatError('Invalid signature for format')


def unpack(token, fmt, tail=False):
    regex = r''
    for symbol in token[:-1]:
        if isinstance(symbol, tuple):
            regex += r'(.*?)'
        elif isinstance(symbol, str):
            regex += re.escape(symbol)
        elif isinstance(symbol, list):
            regex += unpack(fmt[symbol[0]], fmt, tail=True)
        elif isinstance(symbol, dict):
            regex += '(' + unpack(fmt[symbol['+']], fmt, tail=True) + ')+'
        else:
            raise FormatError('Cannot unpack token: ' + token)
    return regex if tail else (r'(^\s*' + regex + ')(?=\s*(' + token[-1] + ')|$)').replace('\ ', '\s*')