# Author: Eric Buss <ebuss@ualberta.ca> 2016
import process_list
import formatter
import fileutil
import options
import pyxam
import sys
import os


signature = 'option config', 'ejrbuss', 'The default options for pyxam'


def load():
    #                   NAME           FLAG    DESCRIPTION                            DEFAULT    TYPE
    options.add_option('out',         '-o',   'Set the output directory',            'out',      str)
    options.add_option('tmp',         '-tmp', 'Set the temporary directory',         'tmp',      str)
    options.add_option('figure',      '-fig', 'Set the figure directory',            'fig',      str)
    options.add_option('number',      '-n',   'Set the number of exams to generate', 1,          int)
    options.add_option('title',       '-t',   'The title of the exam',               'exam',     str)
    options.add_option('format',      '-f',   'The export format',                   'tex',      str)
    options.add_option('shell',       '-shl', 'The shell used to weave the exam',    'python',   str)
    options.add_option('method',      '-m',   'The selection method for CSVs',       'sequence', str)
    options.add_option('population',  '-p',   'The class list CSV',                  None,       str)
    options.add_option('alphabetize', '-a',   'Enable lettered versioning',          False,      bool)
    options.add_option('debug',       '-d',   'Disable file cleanup',                False,      bool)
    # Run once and produce solutions then run again widthout solutions
    if options.add_option('solutions',   '-s',   'Enable soultions',                 False,      bool):
        process_list.run_before('goodbye', rerun)
    # Display version number via the welcome message then exit
    if options.add_option('version','-v',   'Show the version number',             False,      bool):
        if options.state.api():
            pyxam.welcome()
    # Display a list of all available formats then exit
    elif options.add_option('list',   '-ls',  'List all available formats',          False,      bool):
        formats = set(fmt['extensions'][0] for key, fmt in formatter.formats.items())
        for fmt in set(formats):
            print(formatter.formats[fmt]['extensions'][0] + ':\n\t' + formatter.formats[fmt]['description'])
    # Display a help message then exit
    elif options.add_option('help',     '-h',   'Show a help message',                 False,      bool):
        div = '-' * max(len(line) for line in options.get_help().split('\n'))
        print('\n'.join([div, 'Pyxam Options'.center(len(div)), div, options.get_help(), div]))
    # Return signature
    else:
        return signature
    # Exit
    exit()


def rerun():
    args = list(arg for arg in sys.argv[1:] if arg not in ['-s', '-solutions', '--solutions'])
    pyxam.start(args, True)
    exit()


def unload():
    pass




