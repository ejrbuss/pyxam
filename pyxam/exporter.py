# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module exporter

This module is responsible for copying files from the tmp directory to the out directory, calling the selector, and
reading any csv population data associated with this Pyxam call.



The stages of the export process are managed with file extensions. All files that end with .cmp (short for compiled)
will be renamed with either a number or letter depending on whether the `alphabetize` flag has been set and the
extension .mix. These files are then passed to the selector for mixing along with csv data. The selector is expected to
add any necessary .mix files. At this point all .mix files are copied to the out directory with the extension specified
by the compile format.
"""
import formatter
import fileutil
import logging
import options
import csv
import os


# A map of all currently loaded selectors
_selectors = {}


def export():
    """
    Mix the composed files with the specified selector then copy all mixed files to the out directory with the
    appropriate names. If any files are in the figure directory they are copied out as well.
    """
    files = fileutil.with_extension('.cmp')
    # Name file versions
    for n, file in enumerate(files):
        fileutil.mv(file, options.state.cwd() + '/' + (chr(n + ord('A')) if options.state.alphabetize() else str(n + 1)) + '.mix')
    # Mix files
    _selectors[options.state.method()](
        fileutil.with_extension('.mix'),
        csv_read(options.state.population())
    )
    for file in fileutil.with_extension('.mix'):
        fileutil.mv(
            file,
            options.state.out() + '/' +
            options.state.title() + '_' +
            os.path.basename(file[:-4]) +
            ('_solutions' if options.state.solutions() else '') +
            '.' + formatter.get_extension()
        )
    if os.path.isdir(options.state.figure()) and os.listdir(options.state.figure()):
        fileutil.copy_figure()


def csv_read(file):
    """
    Attempts to read the provided CSV file.

    :param file: The csv file to read
    :return: a list of dictionaries containing `number` and `name` entries
    """
    #TODO fail-safe if no columns could be identified
    if file is None:
        return []
    file = options.state.cwd() + '/' + file if os.path.exists(options.state.cwd() + '/' + file) else file
    try:
        with open(file) as file:
            rows = list(csv.reader(file))
            cols = rows[0]
            name = []
            id = []
            for i in range(len(cols)):
                if cols[i].lower().replace(' ', '') in ['firstname', 'surname', 'lastname', 'studentname']:
                    name.append(i)
                if cols[i].lower().replace(' ', '') in ['studentid', 'id', 'identificatinonumber']:
                    id.append(i)
            return [{
                'number': ' '.join(rows[i + 1][j] for j in range(len(rows[i + 1])) if j in name),
                'name': ' '.join(rows[i + 1][j] for j in range(len(rows[i + 1])) if j in id)
            } for i in range(len(rows) - 1)]
    except Exception:
        logging.warning('Unable to parse csv file')
        return []


def add_selector(name, selector):
    """
    Add a selector to the selector list.

    :param name: The name of the selector being added
    :param selector: The selector to add
    """
    _selectors[name] = selector

