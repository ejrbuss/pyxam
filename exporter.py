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


FORMAT_LIST = ['pdf', 'dvi', 'tex', 'html', 'moodle']


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
            try:
                subprocess.call(['pdflatex', name], cwd=fileutil.TEMP)
                export('.pdf')
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
    Compile LaTeX files to html and copy html files to OUT directory.

    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            try:
                subprocess.call(['ht', 'latex', name], cwd=fileutil.TEMP)
                export('.html')
            except:
                exit('Failed to compile latex file: ' + fileutil.TEMP + '/' + name)


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