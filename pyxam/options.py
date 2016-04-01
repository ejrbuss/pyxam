# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module options

This module handles the command line arguments for Pyxam which act as global state for the entire program.
"""
import util
import functools


class OptionError(Exception):
    """
    Error wrapper for Exceptions that occur within the options module.
    """
    pass

# A Map of all current compile functions
state = util.Map()

# A Map of all current options
_compiled = {}

# A map of all unique current options
_unique = {}

# A list of yet to be compiled options
_hanging = []


def clear():
    """
    Clear all compiled, unique, and hanging options.
    """
    global state, _compiled, _unique, _hanging
    state = util.Map()
    _compiled = {}
    _unique = {}
    _hanging = []


def compile_(option, value=None):
    """
    Set the value field of an option with the correct type and/or retrieve the compiled value of the option.
    The compiled value is the default if no value hs been provided by the current or past callers.

    :param option: The option to compile
    :param value: The value to try and set, when None the value is not set
    :return: The compiled value
    """
    if value is not None:
        try:
            # Cast to type
            option.value = option.type_(value)
        except:
            raise OptionError('Type mismatch expected {} received {}'.format(option.type_.__name__, value))
    return option.default if option.value is None else option.value


def add_option(name, flag, description, default, type_, value=None):
    """
    Add an option.

    :param name: The name of the option
    :param flag: The flag for the option
    :param description: A description of the option
    :param default: The default value of the option
    :param type_: The type of the option
    :param value: A value, defaults to None
    :return: The value of the option after parsing any hanging options
    """
    option = util.Map({
        'name': name,
        'flag': flag,
        'description': description,
        'default': default,
        'type_':type_,
        'value': value
    })
    state.update({name: functools.partial(compile_, option)})
    _compiled.update({flag: option, '-' + name: option, '--' + name: option})
    _unique.update({name: option})
    # Load any hanging options
    load_options([])
    return state[name]()


def load_options(options):
    """
    Load options provided as a list in command line syntax.

    :param options: A list of options to load
    """
    global _hanging
    _hanging, collector = _hanging + options, []
    while _hanging:
        if _hanging[0] in _compiled:
            flag = _hanging.pop(0)
            compile_(_compiled[flag], True if _compiled[flag].type_ is bool else _hanging.pop(0))
        else:
            collector.append(_hanging.pop(0))
    _hanging += collector


def load_template():
    """
    Load the template option. Expects to be the last option loaded.
    """
    if len(_hanging) != 1:
        if not state.api():
            exit('No template file, type -h for help')
        raise OptionError('No template file')
    add_option('template', '', 'template file', _hanging.pop(0), str)


def get_help():
    """
    Get a string representing the help message for all options currently added.

    :return: The help string
    """
    name = max([len(v.name) for k, v in _unique.items()])
    flag = max([len(v.flag) for k, v in _unique.items()])
    return '\n'.join((' {0:<{name}}{1:<{flag}} {2:<{arg}}{3} '.format(
        option.name,
        option.flag,
  '[' + option.name + ']' if option.type_ is not bool else '',
        option.description.replace('\n', '\n' + ' ' * (2 * name + flag + 7)),
        name=name, flag=flag, arg=name + 2
    ) for key, option in _unique.items()))


def status():
    """
    Get a string with a table showing all options and their current value.

    :return: The status table
    """
    name = max([len(v.name) for k, v in _unique.items()]) + 1
    value = max([len(str(compile_(v))) for k, v in _unique.items()])
    out = '\n'.join((' {0:<{name}}{1} '.format(
        option.name,
        compile_(option),
        name=name,
    ) for key, option in _unique.items()))
    return 'STATUS TABLE'.center(name + value + 2, '=') + '\n Name{}Value\n{}\n{}\n{}'.format(
        ' ' * (name - len('Name')),
        '=' * (name + value + 2),
        out,
        '=' * (name + value + 2)
    )


def post(*args, **kwargs):
    """
    Send a string to be printed if in api mode. Will add a newline between different callers.
    """
    if not state.api():
        if not util.same_caller():
            print()
        print(*args, **kwargs)


def post_status():
    """
    Post the status table.
    """
    post(status())