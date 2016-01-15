# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import os
import re
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
        files = [name for name in os.listdir(fileutil.TEMP) if os.path.isfile(fileutil.TEMP + '/' + name)
                 and not name.endswith(core.SOLUTIONS + '.tex') and name.endswith('.tex')]
        for name in files:
            insert_data(name, [])
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
        for name in files:
            insert_data(name, [])


def insert_data(file, row):
    """
    Insert CSV data into the \Pconst{STUDENT}, \Pconst{FIRSTNM}, \Pconst{LASTNM} and \Pconst{NUMBER} commads.
    Student names and numbers are assumed to be seperated by commas.

    :param file: The file to read and insert into
    :param row: The csv data
    :return: None
    """
    first = ''
    last = ''
    number = ''
    for item in row:
        if item == '':
            continue
        if re.match(r'.*[0-9].*', item):
            number = item
        elif first == '':
            first = item
        else:
            last = item
    split = first.lstrip().split(' ')
    if len(split) > 1 and last == '':
        last = split[len(split) - 1]
        first = split[0]
    buffer = fileutil.read_temp(file)
    buffer = templater.parse_constant(buffer, 'STUDENT', first + ' ' + last)
    buffer = templater.parse_constant(buffer, 'FIRSTNM', first)
    buffer = templater.parse_constant(buffer, 'LASTNM', last)
    buffer = templater.parse_constant(buffer, 'NUMBER', number)
    if first == '':
        fileutil.write_temp(file, buffer)
    elif number == '':
        fileutil.write_temp(file[:-4] + '-' + first + ' ' + last + '.tex', buffer)
    else:
        fileutil.write_temp(file[:-4] + '-' + number + '.tex', buffer)