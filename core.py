# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import re
import subprocess


# Module Imports


import logger
import fileutil
import pyxamopts
import templater
import weaver
import populationmixer
import exporter


# Global Variables


DEPENDENCIES = []# ['pdflatex'] !!!!!!!!!! uncomment for running !!!!!!!!!!
SOLUTIONS = '_solutions'


# Utility Methods


def pyxam(cmdl_options):
    """
    The core pyxam process, will process the provided options and weave, parse, mix, and export exam files.
    This is the highest level view of full pyxam process.

    :param cmdl_options: The process options, this should either be an instance of PyxamOptions or a the namespace of
    an ArgumentParser initialized by pyxamopts.init_arg_parser
    :return: None
    """
    pyxamopts.is_opts(cmdl_options)
    if cmdl_options.logging: logger.DEBUG = logger.LEVEL.INFO
    check_dependencies()
    buffer = ''
    try:
        buffer = fileutil.read(cmdl_options.template)
        fileutil.make_cwd(cmdl_options.template)
    except FileNotFoundError:
        exit('Could not find template file: ' + cmdl_options.template)
    except IsADirectoryError:
        exit('Template file is a directory: ' + cmdl_options.template)
    except PermissionError:
        exit('Template file is a directory: ' + cmdl_options.template)
    # Check Options
    logger.log('core.pyxam', 'Checking options')
    options = templater.pre_process(buffer)
    options = pyxamopts.check(options)
    options = pyxamopts.check(cmdl_options, options)
    # Build Base Files
    logger.log('core.pyxam', 'Building base files')
    fileutil.make_temp(options.temp)
    fileutil.write_temp(options.title, buffer)
    # Weave and parse
    logger.log('core.pyxam', 'Weaving and parsing files')
    for n in range(options.number):
            name = options.title + index(n, options)
            buffer = fileutil.read_temp(options.title)
            buffer = templater.pimport(buffer, options.sample)
            buffer = templater.clean(buffer)
            buffer = templater.parse_constant(buffer, 'VERSION', index(n, options))
            buffer = templater.parse_constant(buffer, 'TITLE', options.title)
            fileutil.write_temp(name, buffer)
            weaver.weave(name, options.matplotlib, options.figure, options.shell)
            if options.solutions:
                fileutil.write_temp(name + SOLUTIONS + '.tex', make_solutions(fileutil.read_temp(name + '.tex')))
            logger.log('core.pyxam', 'Finished (' + str(n + 1) + '/' + str(options.number) + ')')
    fileutil.remove(fileutil.TEMP + '/' + options.title)
    # Mix and export
    logger.log('core.pyxam', 'Mixing and exporting')
    populationmixer.mix(options.population)
    fileutil.make_out(options.out)
    exporter.switch(options.format)
    # Cleanup
    logger.log('core.pyxam', 'Cleaning up')
    fileutil.remove(options.figure)
    fileutil.remove_temp()


def index(n, options):
    """
    Return the str representation of the number.
    Returns an uppercase letter if the options.alphabetize flag is set

    :param n: The number to index
    :param options: The options to
    :return: The str representation of n
    """
    if options.alphabetize:
        return str(chr(n + ord('A')))
    return str(n + 1)


def check_dependencies():
    """
    Checks that all processes DEPENDENCIES are runnable subprocesses.

    Exits the program if a process is missing

    :return: None
    """
    logger.log('core.check_dependencies', 'Checking dependencies')
    for process in DEPENDENCIES:
        try:
            subprocess.check_output([process, '--version'])
        except OSError:
            exit(process + ' could not be found. Please install to continue.')


def make_solutions(buffer):
    """
    Add the answers argument to the \documentclass command.
    If other arguments exist it will be added to the list otherwise the argument box will be added.
    The original buffer is not changed

    :param buffer: The buffer to add the answers argument to
    :return: The new solution_buffer
    """
    # regex with look behind for escaped commands, see templater.tex_match for more details
    solution_buffer = re.sub(r'(?:^|[^\\])(?:\\\\)*\\documentclass\[', r'\documentclass[answers,', buffer)
    solution_buffer = re.sub(r'(?:^|[^\\])(?:\\\\)*\\documentclass{', r'\documentclass[answers]{', solution_buffer)
    return solution_buffer
