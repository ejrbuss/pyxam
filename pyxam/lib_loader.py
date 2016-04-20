# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module lib_loader

Module for interacting with external modules and libraries.
"""
import os
import sys
import pweave
import options
import logging
import fileutil
import subprocess


class LibError(Exception):
    pass


def weave(path):
    stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        pweave.weave(path, doctype='tex', figdir=options.state.figure(), shell=options.state.shell())
    except:
        raise LibError('Failed to Pweave file: ' + path)
    sys.stdout = stdout


def gs(file):
    """
    Calls ghostscript on a pdf image file to convert it to png.
    :param file: The path to the pdf image file
    :return: The new new path to the png file
    """
    try:
        with open(os.devnull, 'r') as stdin:
            subprocess.check_output(['gs', '-sDEVICE=pngalpha', '-sOutputFile=' + file[:-3] + 'png', file], stdin=stdin)
    except:
        raise LibError('Ghostscript call failed on file: ' + file)
    logging.info('Used ghostscript to convert ' + file + ' to png')
    return file[:-3] + 'png'


def pdflatex(file):
    """
    Calls pdflatex on a LaTeX file to compile it. By default no output is shown and no user input is allowed. If this
    fails the compilation is attempted again but this time pdflatex is run in interactive mode to allow the user to see
    what issues there may be.
    :param file: The path to the LaTeX file to compile
    """
    try:
        with open(os.devnull, 'r') as stdin:
            subprocess.check_output(['pdflatex', '-shell-escape', file], stdin=stdin, cwd=options.state.out())
    except:
        pass
    if not any(os.path.isfile(file[:-3] + extension) for extension in ['pdf', 'dvi']):
        options.post('Failed to compile latex file: ' + file + '\n' + 'Running pdflatex in interactive mode...')
        subprocess.call(['pdflatex', '-shell-escape', file], cwd=options.state.out())

