# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import argparse


# Module Imports


import logger
import exporter
import populationmixer


# PyxamOptions Class


class PyxamOptions:

    def __init__(self):
        """
        Sets options to default values.

        :return: None
        """
        # Paths
        self.template = 'in'
        self.out = 'out'
        self.temp = 'temp'
        self.figure = 'figures'
        # Evaluated
        self.number = 1
        self.sample = 1
        self.recompilation = 1
        self.title = 'exam'
        self.format = 'pdf'
        self.shell = 'python'
        self.method = 'sequence'
        self.population = None
        # Flags
        self.solutions = False
        self.alphabetize = False
        self.rearrange = False
        self.clean = False
        self.interactive = False
        self.logging = False
        self.debug = False


# Utility Methods


def check(opts, defaults=PyxamOptions()):
    """
    Compares opts to defaults, if opts is not None then defaults is updated to opts value.

    :param opts: The options to check
    :param defaults: The default options, by default a fresh PyxamOPtions instance
    :return: The updated defaults
    """
    if opts is None: return defaults
    if opts.template is not None: defaults.template = opts.template
    if opts.out is not None: defaults.out = opts.out
    if opts.temp is not None: defaults.temp = opts.temp
    if opts.figure is not None: defaults.figure = opts.figure
    if opts.number is not None: defaults.number = opts.number
    if opts.sample is not None: defaults.sample = opts.sample
    if opts.recompilation is not None: defaults.recompilations = opts.recompilation
    if opts.title is not None: defaults.title = opts.title
    if opts.format is not None: defaults.format = opts.format
    if opts.shell is not None: defaults.shell = opts.shell
    if opts.method is not None: defaults.method = opts.method
    if opts.population is not None: defaults.population = opts.population
    if opts.solutions is not None: defaults.solutions = opts.solutions
    if opts.alphabetize is not None: defaults.alphabetize = opts.alphabetize
    if opts.rearrange is not None: defaults.rearrange = opts.rearrange
    if opts.clean is not None: defaults.clean = opts.clean
    if opts.interactive is not None: defaults.interactive = opts.interactive
    if opts.logging is not None: defaults.logging = opts.logging
    if opts.debug is not None: defaults.debug = opts.debug
    return defaults


def add_option(name, flag, help, parser, type=str):
    """
    Add an option with an argument to an ArgumentParser.
    The default value of the option will be set to None and the nargs to '?'.

    :param name: The name of the option
    :param flag: The flag for the option
    :param help: The help message for the option
    :param parser: The ArgumentParser to add the option to
    :param type: The argument type
    :return: None
    """
    parser.add_argument(flag, '--' + name, nargs='?', type=type, help=help, default=None)


def add_flag(name, flag, help, parser):
    """
    Add a flag to an ArgumentParser.
    The default value of the flag will be None.

    :param name: The name of the flag
    :param flag: The flag
    :param help: The help message for the option
    :param parser: The ArgumentParser to add the flag to
    :return: None
    """
    parser.add_argument(flag, '--' + name, action='store_true', help=help, default=None)


def init_arg_parser(args):
    """
    Initialize an ArgumentParser with PyxamOptions options and flags and return parsed namespace.

    :param args: The arguments to parse
    :return: The namespace of the parsed arguments
    """
    # Create parser
    parser = argparse.ArgumentParser(usage = 'pyxam.py [OPTIONS] template', description='Parses latex files to produce exams in various formats.')
    # Required arg
    parser.add_argument('template', nargs=1, help='Template file location')
    # Optional args
    add_option('out', '-o', 'Output directory', parser)
    add_option('temp', '-T', 'Temporary file directory', parser)
    add_option('shell', '-S', 'Code parsing shell', parser)
    add_option('title', '-t', 'Title of the exam', parser)
    add_option('number', '-n', 'Number of exams to generate', parser, int)
    add_option('format', '-f', 'Format of the exam: ' + str(exporter.FORMAT_LIST), parser)
    add_option('sample', '-N', 'Default sample size', parser, int)
    add_option('recompilation', '-r', 'The number of times the LaTeX file will be recompiled', parser, int)
    add_option('figure', '-F', 'Figures directory', parser)
    add_option('method', '-m', 'Exam selection method: ' + str(populationmixer.METHOD_LIST), parser)
    add_option('population', '-p', 'Population csv file', parser)
    # Flags
    add_flag('solutions', '-s', 'Enable solution files', parser)
    add_flag('alphabetize', '-a', 'Alphabetize exam enumeration', parser)
    add_flag('rearrange', '-R', 'Enable multiple choice shuffling', parser)
    add_flag('clean', '-c', 'Clean questions and newlines', parser)
    add_flag('interactive', '-i', 'Enable LaTeX calls interactive', parser)
    add_flag('logging', '-l', 'Enable logging', parser)
    add_flag('debug', '-d', 'Enable debug mode', parser)
    #Parse
    options = parser.parse_args(args)
    # Check for list encapsulated template str
    if not isinstance(options.template, str):
        options.template = options.template[0]
    return options


def is_opts(opts):
    """
    Check if options can be successfully parsed and are safe to use.

    Exits the program if the options fail to parse

    :param opts: The options to parse
    :return: None
    """
    try:
        args = 'template:\t\t' + str(opts.template) + '\n'
        args = args + 'out:\t\t\t' + str(opts.out) + '\n'
        args = args + 'temp:\t\t\t' + str(opts.temp) + '\n'
        args = args + 'figure:\t\t\t' + str(opts.figure) + '\n'
        args = args + 'number:\t\t\t' + str(opts.number) + '\n'
        args = args + 'sample:\t\t\t' + str(opts.sample) + '\n'
        args = args + 'recompilation\t' + str(opts.recompilation) + '\n'
        args = args + 'title:\t\t\t' + str(opts.title) + '\n'
        args = args + 'format:\t\t\t' + str(opts.format) + '\n'
        args = args + 'shell:\t\t\t' + str(opts.shell) + '\n'
        args = args + 'method:\t\t' + str(opts.method) + '\n'
        args = args + 'population:\t\t' + str(opts.population) + '\n'
        args = args + 'solutions:\t\t' + str(opts.solutions) + '\n'
        args = args + 'alphabetize:\t' + str(opts.alphabetize) + '\n'
        args = args + 'rearrange:\t\t' + str(opts.rearrange) + '\n'
        args = args + 'clean:\t\t\t' + str(opts.clean) + '\n'
        args = args + 'interactive:\t' + str(opts.interactive) + '\n'
        args = args + 'logging:\t\t' + str(opts.logging) + '\n'
        args = args + 'debug:\t\t' + str(opts.debug) + '\n'
        logger.log('pyxam.opts', 'Options provided (None will become default):\n' + args)
        return opts
    except:
        # Exit if the options cannot be parsed and the user does not want to proceed with default options
        print(' * Warning * The options provided to pyxam could not be parsed')
        if input('Continue with default options? (y/n) ') == 'y':
            return PyxamOptions()
        else:
            exit('Cancelling operation.')