#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca> 2016
import functools
import libs.map


class OptionError(Exception):
    pass

# A Map of all current compile functions
state = libs.map.Map()
# A Map of all current options
_compiled = {}
# A list of not compiled options
_hanging = []


def clear():
    """
    Clear all compiled and hanging options.
    """
    global state, _compiled, _hanging
    state = libs.map.Map()
    _compiled = {}
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
    option = libs.map.Map({'name': name, 'flag': flag, 'description': description, 'default': default, 'type_':type_, 'value': value})
    state.update({name: functools.partial(compile_, option)})
    _compiled.update({flag: option, '-' + name: option, '--' + name: option})
    # Load any hanging options
    load_options([])
    return state[name]()


def load_options(options):
    """
    Load options provided as a list in command line syntax.
    :param options: A list of options to load
    :return: None
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
    :return: None
    """
    if len(_hanging) != 1:
        if not state.api():
            exit('No template file, type -h for help')
        raise OptionError('No template file')
    add_option('template', '', 'template file', _hanging.pop(0), str)
#TODO finish

def get_help():
    """
    Get a string representing the help message for all options currently added.
    :return: The help string
    """
    name = max([len(v.name) for k, v in _compiled.items() if k.startswith('--')])
    flag = max([len(v.flag) for k, v in _compiled.items() if k.startswith('--')])
    return '\n'.join((' {0:<{name}}{1:<{flag}} {2:<{arg}}{3} '.format(
        option.name,
        option.flag,
  '[' + option.name + ']' if option.type_ is not bool else '',
        option.description.replace('\n', '\n' + ' ' * (2 * name + flag + 7)),
        name=name, flag=flag, arg=name + 2
    ) for key, option in _compiled.items() if key.startswith('--')))


def post(*args, **kwargs):
    """

    :param o:
    :return:
    """
    if not state.api():
        print(*args, **kwargs)


def status():
    """

    :return:
    """
    name = max([len(v.name) for k, v in _compiled.items() if k.startswith('--')]) + 1
    value = max([len(str(compile_(v))) for k, v in _compiled.items() if k.startswith('--')])
    out = '\n'.join((' {0:<{name}}{1} '.format(
        option.name,
        compile_(option),
        name=name,
    ) for key, option in _compiled.items() if key.startswith('--')))
    return 'OPTIONS TABLE'.center(name + value, '=') + '\n Name{}Value\n{}\n{}\n{}\n'.format(
        ' ' * (name - len('Name')),
        '=' * (name + value),
        out,
        '=' * (name + value)
    )


def post_status():
    post(status())