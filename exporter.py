#!/usr/bin/env python3
import csv
import re
import os
import options
import fileutil
import formatter
import logging


class ExportError(Exception):
    pass


# A map of all currently loaded selectors
_selectors = {}


def export():
    """
    Mix the composed files with the specified selector then copy all mixed files to the out directory with
    the appropriate names. If any files are in the figure directory they are copied out as well.
    :return: None
    """
    files = fileutil.with_extension('.cmp')
    # Name file versions
    for n, file in enumerate(files):
        os.rename(file, (chr(n + ord('A')) if options.state.alphabetize() else str(n + 1)) + '.mix')
    # Mix files
    _selectors[options.state.method()]['mix'](
        fileutil.with_extension('.mix'),
        csv_read(options.state.population())
    )
    for file in fileutil.with_extension('.mix'):
        os.rename(file, options.state.out() + '/' + options.state.title() + '_' + file[:-3] + formatter.get_extension())
    if os.listdir(options.state.figure()):
        fileutil.copy_figure()


def csv_read(file):
    """
    Attempts to read the provided CSV file.
    :param file: The CSV file
    :return: All the data in the file that matches as either student name or number
    """
    if file is None:
        return []
    file = options.state.cwd() + '/' + file if os.path.exists(options.state.cwd() + '/' + file) else file
    try:
        with open(file) as file:
            return [{
                'number': ' '.join(n for n in row if re.match(r'.*[0-9].*', n)).strip(),
                'name': ' '.join(s for s in row if not re.match(r'.*[0-9].*', s)).strip()
            } for row in csv.reader(file)]
    except Exception as e:
        logging.warning('Unable to parse csv file')
        raise
        return []


def add_selector(selector):
    """
    Add a selector to the selector list.
    :param selector: The selector to add
    :return: None
    """
    if ('name' and 'mix') in selector:
        _selectors[selector['name']] = selector
    else:
        raise ExportError('Invalid signature for selector')

