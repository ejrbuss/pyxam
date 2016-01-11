# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import os
import sys
import enum
import time
import textwrap


# Module Imports
import fileutil


# LEVEL Class

class LEVEL(enum.Enum):
    SILENT = 0
    CRITICAL = 1
    WARNING = 2
    INFO = 3


# Global variables


DEBUG = LEVEL.SILENT
OUT = sys.stdout


# Utility Methods


def log(caller, message, level=LEVEL.INFO):
    """
    Write a log message.

    :param caller: A str in the format file.method ex. logger.log
    :param message: A str message to log
    :param level: The logger.LEVEL of this particular message
    :return: None
    """
    if level == LEVEL.CRITICAL:
        exit(message)
    if DEBUG.value >= level.value:
        OUT.write(level.name + '@' + caller + ':\n')
        for line in message.split('\n'):
            OUT.write('\t' + line + '\n')


def to_file(name=str(time.time()) + '.log', directory='logs'):
    """
    Write logs to file.

    :param name: The name of the file, by default this is the current system time
    :param directory: The name of the directory to write to, by default this is 'CWD/logs'
    :return: None
    """
    if not os.path.exists(directory):
        os.mkdir(directory)
    fileutil.write(directory + '/' + name, OUT.getvalue())
