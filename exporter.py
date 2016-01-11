# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import os
import shutil


# Module Imports


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
    print('TODO pdf')


def dvi():
    print('TODO dvi')


def tex():
    """
    Copy weaved files to OUT directory.

    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        path = fileutil.TEMP + '/' + name
        if os.path.isfile(path) and path.endswith('.tex'):
            fileutil.copy_out(name)
        elif os.path.isdir(path) and len(os.listdir(path)) > 0:
            os.mkdir(fileutil.OUT + '/' + name)
            for figure in os.listdir(path):
                shutil.copy(path + '/' + figure, fileutil.OUT + '/' + name + '/' + figure)


def html():
    print('TODO html')


def moodle():
    print('TODO moodle')