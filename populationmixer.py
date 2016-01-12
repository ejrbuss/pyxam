# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import os
import csv
import random


# Module Imports


import core
import logger
import fileutil
import templater


# Global Variables


METHOD_LIST = ['random', 'sequence']


# Selector Class


class Selector:

    def __init__(self, items, method):
        """
        Initialize a selector with a specified item set and selection method.

        :param items: The items to select from
        :param method: The selection method name
        :return: A new Selector
        """
        self.files = items
        self.method = method
        self.index = 0

    def next(self):
        """
        Return the next selected item based on the initialize selection method.

        :return: The next item
        """
        if self.method == 'random':
            return random.choice(self.files)
        if self.method == 'sequence':
            self.index += 1
            return self.files[(self.index - 1) % len(self.files)]


# Utility Methods


def mix(path, method):
    """
    Take the generated exams and distribute them among a set of students specified by a CSV file.

    Prints a warning if the CSV file is invalid

    :param path: The relative or absolute path to the CSV file
    :param method: The distribution method, see METHOD_LIST
    :return: None
    """
    if path is None:
        return
    if not os.path.isfile(path):
        logger.log('populationmixer.mix', 'The path provided does not point to a file', logger.LEVEL.WARNING)
        print(' * Warning * Invalid CSV file')
        return

    with open(path) as file:
        files = [name for name in os.listdir(fileutil.TEMP) if os.path.isfile(fileutil.TEMP + '/' + name)
                 and not name.endswith(core.SOLUTIONS + '.tex') and name.endswith('.tex')]
        selector = Selector(files, method)
        reader = csv.reader(file)
        for row in reader:
            name = selector.next()
            insert_data(name, row)


def insert_data(file, row):
    """
    Insert CSV data into the \Pconst{STUDENT} and \Pconst{STUDNUM} tags of a file.
    The assumed format is either
    $STUDENT
    $STUDENT
    ...
        or
    $STUDENT, $STUDNUM
    $STUDENT, $STUDNUM
    ...
    If no student number is provided the tag will be removed from the file.
    If no student number is provided the file will be written to a file with a -$STUDENT appended to the filename.
    If a student number is provided the file will be written to a file with a -#STUDNUM append to the filename.

    :param file: The file to read and insert into
    :param row: The csv data
    :return: None
    """
    if len(row) < 1:
        return
    if row[0] == '':
        return
    buffer = fileutil.read_temp(file)
    buffer = templater.parse_constant(buffer, 'STUDENT', row[0])
    # Check for trailing commas
    if len(row) > 1 and row[1] != '':
        buffer = templater.parse_constant(buffer, 'STUDNUM', row[1])
        fileutil.write_temp(file[:-4] + '-' + row[1] + '.tex', buffer)
    else:
        buffer = templater.parse_constant(buffer, 'STUDNUM', '')
        fileutil.write_temp(file[:-4] + '-' + row[0] + '.tex', buffer)