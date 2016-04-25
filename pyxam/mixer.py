# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module mixer

Mixes and weaves the template file.
"""
import re
import os
import csv
import config
import options
import logging
import fileutil
import lib_loader


# A map of all currently loaded methods
_methods = {}


# The inline code placed at the start of every weaved file
inline = fileutil.read(config.pyxam_directory + '/inline.py')


def setup():
    """
    Mix the composed files with the specified method then copy all mixed files to the out directory with the
    appropriate names. If any files are in the figure directory they are copied out as well.
    """
    for n in range(options.state.number()):
        mix(n, {'first': '', 'last': '', 'name': '','number': ''}, default=True)
    _methods[options.state.method()](options.state.number(), csv_read(options.state.population()))
    options.post('Template successfully weaved.')


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
            first, last, name, number = [], [], [], []
            # Try and identify name and number columns
            for i in range(len(cols)):
                if cols[i].lower().replace(' ', '') in config.first_name_column_identifiers:
                    first.append(i)
                elif cols[i].lower().replace(' ', '') in config.last_name_column_identifiers:
                    last.append(i)
                elif cols[i].lower().replace(' ', '') in config.name_column_identifiers:
                    name.append(i)
                elif cols[i].lower().replace(' ', '') in config.number_column_identifiers:
                    number.append(i)
            # If no columns were identified fallback to regex detection
            name = name + first + last
            if not name and not number:
                cols = rows[1]
                for i in range(len(cols)):
                    if re.match(r'\d+', cols[i]):
                        number.append(i)
                    else:
                        name.append(i)
            # Build and return data
            return [{
                'number': ' '.join(rows[i + 1][j] for j in range(len(rows[i + 1])) if j in number).strip(),
                'first': ' '.join(rows[i + 1][j] for j in range(len(rows[i + 1])) if j in first).strip(),
                'last': ' '.join(rows[i + 1][j] for j in range(len(rows[i + 1])) if j in last).strip(),
                'name': ' '.join(rows[i + 1][j] for j in range(len(rows[i + 1])) if j in name).strip()
            } for i in range(len(rows) - 1)]
    except:
        if file is not None:
            logging.warning('Unable to parse csv file')
        return []


def mix(n, row, default=False):
    """
    Takes an exam version and row of data and prepares a file for the formatter. If weaving is enabled a .mix with the
    correct name is weaved with the inline code at the start of the file. If weaving is disabled a .tex file is prepared
    for the formatter directly.

    :param n: The exam version
    :param row: The row of data
    """
    logging.info(str(row))
    version = str(chr(n + ord('A')) if options.state.alphabetize() else n + 1)
    if options.state.noweave():
        fileutil.write(
            options.state.cwd() + '/' + config.filename.format(version=version, name=row['name'].replace(' ', '_').strip(), number=row['number']).strip('_') + '.tex',
            fileutil.read(options.state.template())
        )
    else:
        path = options.state.cwd() + '/' + config.filename.format(version=version, name=row['name'].replace(' ', '_').strip(), number=row['number']).strip('_') + '.tex'
        fileutil.write(
            path,
            '<%\n' + inline
                .replace('{number}', str(n))
                .replace('{version}', str(version))
                .replace('{student_first_name}', config.placeholder[options.state.format()]  if default else str(row['first']))
                .replace('{student_last_name}', config.placeholder[options.state.format()]  if default else str(row['last']))
                .replace('{student_name}', config.placeholder[options.state.format()] if default else str(row['name']))
                .replace('{student_number}', config.placeholder[options.state.format()]  if default else str(row['number'])) +
            '\n%>' + fileutil.read(options.state.template())
        )
        lib_loader.weave(path)
        fileutil.write(
            path,
            '<%\n' + inline
                .replace('{number}', str(n))
                .replace('{version}', str(version))
                .replace('{student_first_name}', config.placeholder[options.state.format()]  if default else str(row['first']))
                .replace('{student_last_name}', config.placeholder[options.state.format()]  if default else str(row['last']))
                .replace('{student_name}', config.placeholder[options.state.format()] if default else str(row['name']))
                .replace('{student_number}', config.placeholder[options.state.format()]  if default else str(row['number'])) +
            '\n%>' + fileutil.read(options.state.cwd() + '/' + config.filename.format(version=version, name=row['name'].replace(' ', '_'), number=row['number']).strip('_') + '.tex')
        )
        lib_loader.weave(path)


def add_method(name, method):
    """
    Add a method to the method list.

    :param name: The name of the method being added
    :param method: The method to add
    """
    _methods[name] = method
