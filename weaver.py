# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports

import os
import sys


# Module Imports


import pweave
import logger
import fileutil
import templater


def weave(path, matplotlib, figure, shell):
    """
    Parse and run Python code using Pweave.

    Exits if Pweave throws an Exceptions

    :param path: The path to the file to Pweave
    :param matplotlib: If True disables MatPlotLib
    :param figure: The name of the figure directory
    :param shell: The shell to use to parse
    :return: None
    """
    # Change instances of \Pexpr to <<%= >>
    buffer = fileutil.read_temp(path)
    unparsed = templater.tex_match(buffer, 'Pexpr', True)[::-1]
    for pair in unparsed:
        command = buffer[pair[0]:pair[1]]
        arg = templater.tex_match(command, 'Pexpr')
        arg = command[arg[0][0]:arg[0][1]]
        buffer = buffer[:pair[0]] + '<%= ' + arg + ' %>' + buffer[pair[1]:]
    fileutil.write_temp(path, buffer)
    old_stdout = sys.stdout
    sys.stdout = open(fileutil.TEMP + '/weave', 'w')
    try:
        try:
            pweave.weave(fileutil.TEMP + '/' + path, doctype='tex', shell=shell, figdir=figure, plot=matplotlib)
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout
            logger.log('weaver.weave', 'Pweave output:\n' + fileutil.read_temp('weave'))
    except:
        exit('Failed to Pweave file: ' + fileutil.TEMP + '/' + path)