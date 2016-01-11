# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports

import io
import os
import sys
import shutil
import subprocess


# Module Imports


import pweave
import logger
import fileutil


# Global Variables


FORMAT_LIST = ['pdf', 'dvi', 'tex', 'moodle']


# Utility Methods


def switch(fmt):
    """
    Send off a call to the correct exporter and export files to the OUT directory.

    :param fmt: The export format
    :return: None
    """
    if fmt == 'dvi': dvi()
    elif fmt == 'tex': tex()
    elif fmt == 'html': html()
    elif fmt == 'moodle': moodle()
    else: pdf()


def pdf():
    """
    Compile LaTeX files to pdf and copy pdf files to OUT directory.

    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            out = open(fileutil.TEMP + '/compile', 'w')
            try:
                try:
                    subprocess.call(['pdflatex', name], cwd=fileutil.TEMP, stdout=out)
                    export('.pdf')
                finally:
                    out.close()
                    logger.log('exporter.pdf', 'pdflatex output:\n' + fileutil.read_temp('compile'))
            except:
                exit('Failed to compile latex file: ' + fileutil.TEMP + '/' + name)


def dvi():
    """
    Compile LaTeX files to dvi and copy dvi files to OUT directory.

    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            fileutil.write_temp(name, '%&latex\n' + fileutil.read_temp(name))
    pdf()
    export('dvi')



def tex():
    """
    Copy weaved files to OUT directory.

    :return: None
    """
    export('.tex')
    for name in os.listdir(fileutil.TEMP):
        path = fileutil.TEMP + '/' + name
        if os.path.isdir(path) and len(os.listdir(path)) > 0:
            os.mkdir(fileutil.OUT + '/' + name)
            for figure in os.listdir(path):
                shutil.copy(path + '/' + figure, fileutil.OUT + '/' + name + '/' + figure)


def html():
    """
    Calls Pweave html exporter.
    This does not translate LaTex.
    This is not currently a valid export.

    Exits if Pweave throws an Exception

    :return: None
    """
    logger.log('exporter.html', 'HTML is not currently a functional export.', logger.LEVEL.WARNING)
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            old_stdout = sys.stdout
            sys.stdout = open(fileutil.TEMP + '/weave', 'w')
            try:
                try:
                    pweave.weave(fileutil.TEMP + '/' + name, doctype='html')
                    export('.html')
                finally:
                    sys.stdout.close()
                    sys.stdout = old_stdout
                    logger.log('weaver.weave', 'Pweave output:\n' + fileutil.read_temp('weave'))
            except:
                exit('Failed to Pweave file: ' + fileutil.TEMP + '/' + name)


def moodle():
    print('TODO moodle')


def export(extension):
    """
    Move all files with the specified extension from TEMP to OUT.

    :param extension: Files with this extension will be moved
    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith(extension):
            fileutil.copy_out(name)