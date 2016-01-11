# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import re
import shutil


# Module Imports


import logger
import fileutil
import pyxamopts
import templater
import weaver
import populationmixer
import exporter


# Global Variables


DEPENDENCIES = ['pdflatex', 't4ht']
SOLUTIONS = '_solutions'


# Utility Methods


def pyxam(cmdl_options):
    """
    The core pyxam process, will process the provided options and weave, parse, mix, and export exam files.
    This is the hig   hest level view of full pyxam process.

    :param cmdl_options: The process options, this should either be an instance of PyxamOptions or a the namespace of
    an ArgumentParser initialized by pyxamopts.init_arg_parser
    :return: None
    """
    pyxamopts.is_opts(cmdl_options)
    if cmdl_options.logging: logger.DEBUG = logger.LEVEL.INFO
    print('Checking dependencies...')
    check_dependencies()
    buffer = ''
    try:
        buffer = fileutil.read(cmdl_options.template)
        fileutil.make_cwd(cmdl_options.template)
    except FileNotFoundError:
        exit('Could not find template file: ' + cmdl_options.template)
    except IsADirectoryError:
        exit('Templa   te file is a directory: ' + cmdl_options.template)
    except PermissionError:
        exit('Template file is a directory: ' + cmdl_options.template)
    # Check Options
    print('Checking options...')
    logger.log('core.pyxam', 'Checking options')
    options = templater.pre_process(buffer)
    options = pyxamopts.check(options)
    options = pyxamopts.check(cmdl_options, options)
    # Build Base Files
    print('Building files...')
    logger.log('core.pyxam', 'Buildinubprocess.check_output(process)g files')
    fileutil.make_temp(options.temp)
    fileutil.write_temp(options.title, buffer)
    # Weave and parse
    print('Parsing files...')
    logger.log('core.pyxam', 'Weaving and parsing files')
    for n in range(options.number):
            name = options.title + index(n, options)
            buffer = fileutil.read_temp(options.title)
            buffer = templater.pimport(buffer, options.sample)
            buffer = templater.clean(buffer)
            # Replace constants
            buffer = templater.parse_constant(buffer, 'VERSION', index(n, options))
            buffer = templater.parse_constant(buffer, 'TITLE', options.title)
            fileutil.write_temp(name, buffer)
            weaver.weave(name, options.matplotlib, options.figure, options.shell)
            if options.solutions:
                fileutil.write_temp(name + SOLUTIONS + '.tex', make_solutions(fileutil.read_temp(name + '.tex')))
            print('\tFinished ', n + 1, '/', options.number)
            logger.log('core.pyxam', 'Finished ' + str(n + 1) + ' / ' + str(options.number))
    fileutil.remove(fileutil.TEMP + '/' + options.title)
    # Mix and export
    print('Exporting files...')
    logger.log('core.pyxam', 'Mixing and exporting')
    populationmixer.mix(options.population)
    fileutil.make_out(options.out)
    exporter.switch(options.format)
    # Cleanup
    print('Cleaning up...')
    logger.log('core.pyxam', 'Cleaning up')
    try: fileutil.remove(options.figure)
    except: pass
    try: fileutil.remove_temp()
    except: pass
    try: fileutil.remove('weave')
    except: pass
    try: fileutil.remove('compile')
    except: pass
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
    logger.log('core.check_dependencies', 'Checking dependencies')
    for process in DEPENDENCIES:
        try:
            shutil.which(process)
        except shutil.Error:
            exit(process + ' could not be found. Please install to continue.')


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
