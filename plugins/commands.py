# Author: Eric Buss <ebuss@ualberta.ca> 2016
import options
import bang
import shlex


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
    return '<<echo=True>>=\n' + args + '\n@'


def block(args):
    """
    Run a python block silently
    """
    return '<<echo=False>>=\n' + args + '\n@'


def figure(args):
    """
    Insert a python figure
    """
    return '<<fig=True,echo=False>>=' + args + '\n@'


def question_import(args):
    """
    Insert a question
    """
    return ''


def define(args):
    """
    Define a constant
    """
    name = args.split(' ')[0]
    bang.add_command(name, lambda x : eval(args.replace(name, '', 1)))
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
    # Return signature
    return plugin


def unload():
    pass