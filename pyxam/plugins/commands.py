# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin commands

Defines a default set of [bang](%/Modules/bang.html) commands to be used when prepossessing a template.
"""
import os
import bang
import shlex
import config
import random
import logging
import options
import fileutil

# command config by ejrbuss: The default command set
signature = 'command config', 'ejrbuss', 'the default command set'


def arguments(args):
    """
    Load args as though they were command line options. These take priority over command line options. This command will
    be replaced with an empty string. An example where the output format is set to pdf and the debug flag is enabled:
    ```
    # pyxam!args -f pdf -d
    ```
    """
    options.load_options(shlex.split(args))
    return ''


def expression(args):
    """
    Run a python expression and echo the result. An example hello world program:
    ```
    # pyxam!expr 'Hello World'
    ```
    """
    return '<%= ' + args + '%>'


def silent_expression(args):
    """
    Run a python expression silently. This can be used to set variables that are used later. An example:
    ```
    # pyxam!sexpr x = 3
    ```
    """
    return '<% ' + args + '%>'


def verbatim(args):
    """
    Run a python block and return a verbatim copy of the code. An example:
    ```
    /** pyxam!verb
        import time
        x = time.time()
    */
    ```
    Would be turned into:
    ```python
    verb:
        import time()
        x = time.time()
    ```
    And x would now store the current time which could be used by other commands.
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
    return '\n<<echo=False,fig=True>>=\n' + args + '\n@'


def question_import(args):
    """
    Insert a question
    """
    n, imports, import_string = int(shlex.split(args)[0]), [], shlex.split(args)[1]
    for file in import_string.split('|'):
        file = os.path.dirname(options.state.template()) + '/' + file
        if os.path.isfile(file):
            imports.append(fileutil.read(file))
        if os.path.isdir(file):
            for name in os.listdir():
                imports.append(fileutil.read(file + '/' + name))
    random.shuffle(imports)
    import_string = ''
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
    bang.add_command(name, lambda x : str(eval(value)))
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
    define('studentname "{}"'.format(config.student_name))
    define('studentnumber "{}"'.format(config.student_number))
    define('version "{}"'.format(config.version_number))
    if options.add_option('commands', '-cmd', 'Display all available commands', False, bool):
        print('\n'.join('pyxam!' + name + str(fn.__doc__).replace('\n', '\n    ') for name, fn in bang.commands.items()))
        exit()
    return signature


def unload():
    pass