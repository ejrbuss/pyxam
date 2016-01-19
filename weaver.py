# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports

import os
import sys


# Module Imports


import pweave
import fileutil
import templater


def weave(path, figure, shell):
    """
    Parse and run Python code using Pweave.
    Replaces \Pexpr{ ... } with <%= ... %>.
    Replaces \Pexprs{ ... } with <% ... %>.
    Replaces \Pverb{ ... } with <<>>= ... @.
    Replaces \Pblock{ ... } with <<echo=False>> ... @
    Replaces \Pfig{ ... } with <<fig=True,echo=False>> ... @

    Exits if Pweave throws an Exceptions

    :param path: The path to the file to Pweave
    :param matplotlib: If True disables MatPlotLib
    :param figure: The name of the figure directory
    :param shell: The shell to use to parse
    :return: None
    """
    buffer = fileutil.read_temp(path)
    buffer = tonoweb(buffer, 'Pexpr', '<%= ', ' %>')
    buffer = tonoweb(buffer, 'Pexprs', '<% ', ' %>')
    buffer = tonoweb(buffer, 'Pverb', '<<>>=\n', '\n@')
    buffer = tonoweb(buffer, 'Pblock', '<<echo=False>>=\n', '\n@')
    buffer = tofigure(buffer)
    fileutil.write_temp(path, buffer)
    try:
        pweave.weave(fileutil.TEMP + '/' + path, doctype='tex', figdir=figure, shell=shell)
    except:
        exit('Failed to Pweave file: ' + fileutil.TEMP + '/' + path)


def tofigure(buffer):
    requests = templater.command_match(buffer, 'Pfig')
    for request in requests:
        caption = request.arg
        buffer = request.rewrap(buffer, '<<fig=True,caption=\'' + caption + '\',echo=False>>=', '\n@')
    return buffer


def tonoweb(buffer, command, pre, post):
    """
    Replace LaTeX formattting with noweb formatting.

    :param buffer: The buffer to replace formatting on
    :param command: The name of the LaTeX command
    :param pre: The prefix noweb expression
    :param post: The postfix noweb expression
    :return: The new buffer
    """
    requests = templater.command_match(buffer, command)
    for request in requests:
        buffer = request.rewrap(buffer, pre, post)
    return buffer