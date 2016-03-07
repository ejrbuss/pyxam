# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import random
import fileutil
import options
import bang
import shlex
import os


# Plugin signature
plugin = {
    'name': 'commands config',
    'author': 'ejrbuss',
    'description': 'Loads the default command set'
}


def arguments(args):
    """
    Load args as though they were command line options.
    """
    options.load_options(shlex.split(args))
    return ''


def expression(args):
    """
    Run a python expression and echo the result
    """
    return '<%= ' + args + '%>'


def silent_expression(args):
    """
    Run a python expression silently
    """
    return '<% ' + args + '%>'


def verbatim(args):
    """
    Run a python block and return a verbatim copy of the code
    """
    return '\n<<echo=True>>=\n' + args + '\n@'


def block(args):
    """
    Run a python block silently
    """
    return '\n<<echo=False>>=\n' + args + '\n@'


def figure(args):
    """
    Insert a python figure
    """
    return '\n<<fig=True,echo=False>>=' + args + '\n@'


def question_import(args):
    """
    Insert a question
    """
    n, imports, import_string = int(args.split(' ')[0]), [], ''
    os.chdir(os.path.dirname(options.state.template()))
    for file in args.split('|'):
        if os.path.isfile(file):
            imports.append(fileutil.read(file))
        if os.path.isdir(file):
            for name in os.listdir():
                imports.append(fileutil.read(file + '/' + name))
    os.chdir(options.state.tmp())
    random.shuffle(imports)
    while n > 0 and imports:
        import_string += imports.pop(0)
        n -= 1
    if n > 0:
        logging.warning('Tried to import ' + str(n) + ' more questions than were available')
    return import_string


def define(args):
    """
    Define a constant
    """
    name = args.split(' ')[0]
    value = args.replace(name, '', 1)
    logging.info('Defined ' + name + ' as ' + value)
    bang.add_command(name, lambda x : eval(value))
    return ''


def load():
    # Load commands
    bang.add_command('args', arguments)
    bang.add_command('expr', expression)
    bang.add_command('sexpr', silent_expression)
    bang.add_command('verb', verbatim)
    bang.add_command('block', block)
    bang.add_command('fig', figure)
    bang.add_command('import', question_import)
    bang.add_command('def', define)
    define('student_name $tudent__name')
    define('student_number $tudent__number')
    # Return signature
    return plugin


def unload():
    pass