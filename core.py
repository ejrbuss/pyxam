# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import os
import re
import random
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


# List of dependencies
DEPENDENCIES = [['pdflatex', '--version'], ['ht']]
# File name extension for solutions
SOLUTIONS = '-solutions'
# In order to consistently generate exams
SEED = 12575220


# Utility Methods


def pyxam(parameter_options):
    """
    The core pyxam process, will process the provided options and weave, parse, mix, and export exam files.
    This is the hig   hest level view of full pyxam process.

    :param parameter_options: The process options, this should either be an instance of PyxamOptions or a the namespace of
    an ArgumentParser initialized by pyxamopts.init_arg_parser
    :return: None
    """
    # Seed random for all operations
    random.seed(SEED)
    # Get valid options
    parameter_options = pyxamopts.is_opts(parameter_options)
    # Set logger
    if parameter_options.logging:
        logger.DEBUG = logger.LEVEL.INFO
    # Check dependencies
    print('Checking dependencies...')
    check_dependencies()
    # Read in template and check for Exceptions
    buffer = ''
    try:
        buffer = fileutil.read(parameter_options.template)
        fileutil.make_cwd(parameter_options.template)
    except FileNotFoundError:
        exit('Could not find template file: ' + parameter_options.template)
    except IsADirectoryError:
        exit('Template file is a directory: ' + parameter_options.template)
    except PermissionError:
        exit('Template file is a directory: ' + parameter_options.template)
    except:
        exit('Unkown error when attempting to read template file: ' + parameter_options.template)
    # Check Options defaults -> template arguments -> parameter arguments
    print('Checking options...')
    options = templater.pre_process(buffer)
    options = pyxamopts.check(options)
    options = pyxamopts.check(parameter_options, options)
    # Build Base Files
    print('Building files...')
    fileutil.make_temp(options.temp)
    fileutil.write_temp(options.title, buffer)
    # Weave and parse
    print('Parsing files...')
    for n in range(options.number):
            # Import questions and clean file
            name = options.title + index(n, options)
            buffer = fileutil.read_temp(options.title)
            buffer = templater.pimport(buffer, options.sample)
            buffer = templater.clean(buffer)
            # Replace constants
            buffer = templater.parse_constant(buffer, 'VERSION', index(n, options))
            buffer = templater.parse_constant(buffer, 'TITLE', options.title)
            fileutil.write_temp(name, buffer)
            # Call Pweave on file
            weaver.weave(name, options.figure, options.shell)
            # Produce solutions file if necessary
            if options.solutions:
                fileutil.write_temp(name + SOLUTIONS + '.tex', make_solutions(fileutil.read_temp(name + '.tex')))
            # Finished processing file
            print('\tFinished ', n + 1, '/', options.number)
    fileutil.remove(fileutil.TEMP + '/' + options.title)
    # Mix and export
    print('Exporting files...')
    populationmixer.mix(options.population, options.method)
    fileutil.make_out(options.out)
    exporter.switch(options.format, options)
    # Cleanup
    print('Cleaning up...')
    if not options.debug:
        try: fileutil.remove(options.figure)
        except: pass
        try: fileutil.remove('weave')
        except: pass
        try: fileutil.remove('compile')
        except: pass
        try: fileutil.remove_temp()
        except: pass
    # Done
    print('Done!')


def index(n, options):
    """check if subprocess works
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
    for process in DEPENDENCIES:
        try:
            devnull = open(os.devnull)
            subprocess.call(process, stdout=devnull, stderr=devnull)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                exit(str(process) + ' could not be found. Please install to continue.')


def make_solutions(buffer):
    """
    Add the answers argument to the \documentclass command.
    If other arguments exist it will be added to the list otherwise the argument box will be added.
    The original buffer is not changed.

    :param buffer: The str to add the answers argument to
    :return: The new solution str
    """
    # regex with look behind for escaped commands, see templater.tex_match for more details
    solution_buffer = re.sub(r'(?:^|[^\\])(?:\\\\)*\\documentclass\[', r'\documentclass[answers,', buffer)
    solution_buffer = re.sub(r'(?:^|[^\\])(?:\\\\)*\\documentclass{', r'\documentclass[answers]{', solution_buffer)
    return solution_buffer