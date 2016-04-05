# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module mixer

"""
import re
import os
import csv
import config
import options
import logging
import fileutil


# A map of all currently loaded methods
_methods = {}


global_vars = """
<%
class pyxam:
    examnumber = {}
    examversion = "{}".strip()
    studentname = "{}".strip()
    studentnumber = "{}".strip()

    def importquestion(path):
        import fileutil
        print(fileutil.read(path))

    def args(args):
        import options
        import shlex
        options.load_options(shlex.split(args))

import random
import config
random.seed(pyxam.examnumber + config.seed)
%>
"""

def setup():
    """
    Mix the composed files with the specified method then copy all mixed files to the out directory with the
    appropriate names. If any files are in the figure directory they are copied out as well.
    """
    for n in range(options.state.number()):
        mix(n, {'name':'','number':''})
    _methods[options.state.method()](options.state.number(), csv_read(options.state.population()))


def csv_read(file):
    """
    Attempts to read the provided CSV file.

    :param file: The csv file to read
    :return: a list of dictionaries containing `number` and `name` entries
    """
    try:
        # Try and find path
        file = file if os.path.exists(file) else options.state.cwd() + '/' + file
        with open(file) as file:
            # Get data
            rows = list(csv.reader(file))
            # Get column titles
            cols = rows[0]
            # Name and number col collectors
            name, number = [], []
            # Try and identify name and number columns
            for i in range(len(cols)):
                if cols[i].lower().replace(' ', '') in config.name_column_identifiers:
                    name.append(i)
                if cols[i].lower().replace(' ', '') in config.number_column_identifiers:
                    number.append(i)
            # If no columns were identified fallback to regex detection
            if not name and not number:
                cols = rows[1]
                for i in range(len(cols)):
                    if re.match(r'\d+', cols[i]):
                        number.append(i)
                    else:
                        name.append(i)
            # Build and return data
            return [{
                'number': ' '.join(rows[i + 1][j] for j in range(len(rows[i + 1])) if j in number),
                'name': ' '.join(rows[i + 1][j] for j in range(len(rows[i + 1])) if j in name)
            } for i in range(len(rows) - 1)]
    except:
        if file is not None:
            logging.warning('Unable to parse csv file')
        return []


def mix(n, row):
    """

    :param n:
    :param row:
    :return:
    """
    version = str(chr(n + ord('A')) if options.state.alphabetize() else n + 1)
    fileutil.write(
        options.state.cwd() + '/v{}_{}_{}'.format(version, row['name'], row['number']).strip('_') + '.mix',
        global_vars.format(n, version, row['name'], row['number']) +
        fileutil.read(options.state.template())
    )


def add_method(name, method):
    """
    Add a method to the method list.

    :param name: The name of the method being added
    :param method: The method to add
    """
    _methods[name] = method

#TODO finish