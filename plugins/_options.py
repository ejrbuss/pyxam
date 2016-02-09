from options import add_option
from options import get_help
from options import state
from pyxam import welcome
from formatter import _formats

plugin = {
        'name': 'option config',
        'author': 'ejrbuss',
        'description': 'The default options for pyxam'
    }


def load():
    #          NAME           FLAG    DESCRIPTION                            DEFAULT     TYPE
    add_option('out',         '-o',   'Set the output directory',            'out',      str)
    add_option('tmp',         '-tmp', 'Set the temporary directory',         'tmp',      str)
    add_option('figure',      '-fig', 'Set the figure directory',            'fig',      str)
    add_option('number',      '-n',   'Set the number of exams to generate', 1,          int)
    add_option('title',       '-t',   'The title of the exam',               'exam',     str)
    add_option('format',      '-f',   'The export format',                   'tex',      str)
    add_option('shell',       '-shl', 'The shell used to weave the exam',    'python',   str)
    add_option('method',      '-m',   'The selection method for CSVs',       'sequence', str)
    add_option('population',  '-p',   'The class list CSV',                  None,       str)
    add_option('solutions',   '-s',   'Enable soultions',                    False,      bool)
    add_option('alphabetize', '-a',   'Enabled lettered versioning',         False,      bool)
    add_option('debug',       '-d',   'Disable file cleanup',                False,      bool)

    if add_option('help',     '-h',   'Show a help message',                 False,      bool):
        div = '-' * max(len(line) for line in get_help().split('\n'))
        print('\n'.join([div, 'Pyxam Options'.center(len(div)), div, get_help(), div]))

    elif add_option('version','-v',   'Show the version number',             False,      bool):
        if state.api():
            welcome(None)

    elif add_option('list',   '-ls',  'List all available formats',          False,      bool):
        formats = set(fmt['extensions'][0] for key, fmt in _formats.items())
        for fmt in set(formats):
            print(_formats[fmt]['extensions'][0] + ':\n\t' + _formats[fmt]['description'] +
                  '\n\n\t' + '\n\t'.join(label + ': ' + token.regex for label, token in _formats[fmt]['format'].items()))

    else:
        return plugin
    exit()


def unload():
    pass




