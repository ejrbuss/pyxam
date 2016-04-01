# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module exporter

This module is responsible for copying files from the tmp directory to the out directory, calling the method, and
reading any csv population data associated with this Pyxam call.



The stages of the export process are managed with file extensions. All files that end with .cmp (short for compiled)
will be renamed with either a number or letter depending on whether the `alphabetize` flag has been set and the
extension .mix. These files are then passed to the method for mixing along with csv data. The method is expected to
add any necessary .mix files. At this point all .mix files are copied to the out directory with the extension specified
by the compile format.
"""
import re
import os
import csv
import config
import options
import logging
import fileutil
import formatter


# A map of all currently loaded methods
_methods = {}


def export():
    """
    Mix the composed files with the specified method then copy all mixed files to the out directory with the
    appropriate names. If any files are in the figure directory they are copied out as well.
    """
    files = fileutil.with_extension('.cmp')
    # Name file versions
    for n, file in enumerate(files):
        fileutil.move(file, options.state.cwd() + '/' + (chr(n + ord('A')) if options.state.alphabetize() else str(n + 1)) + '.mix')
    # Get files and data
    files, data = fileutil.with_extension('.mix'), csv_read(options.state.population())
    options.post('Performing', options.state.method(), 'mixing of', len(files), 'exam versions among', len(data), 'students.')
    # Mix files
    _methods[options.state.method()](len(files), data)
    # Remove constants fro mthe unmixed files
    for file in files:
        fileutil.write(
            file,
            fileutil.read(file)
                .replace(config.student_name, '')
                .replace(config.student_number, '')
                .replace(config.version_number, '')
        )
    # Export files
    for file in fileutil.with_extension('.mix'):
        fileutil.move(
            file,
            options.state.out() + '/' +
            options.state.title() + '_' +
            os.path.basename(file[:-4]) +
            ('_solutions' if options.state.solutions() else '') +
            '.' + formatter.get_extension()
        )
    # Export figures
    fileutil.copy_figure()


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
    n = str(chr(n + ord('A')) if options.state.alphabetize() else n + 1)
    fileutil.write(
        options.state.cwd() + '/' + config.csv_filename.format(n=n, name=row['name'], number=row['number']),
        fileutil.read(options.state.cwd() + '/' + n + '.mix')
            .replace(config.student_name, ' ' + row['name'])
            .replace(config.student_number, ' ' + row['number'])
            .replace(config.version_number, ' ' + n)
    )


def add_method(name, method):
    """
    Add a method to the method list.

    :param name: The name of the method being added
    :param method: The method to add
    """
    _methods[name] = method

#TODO finish