# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import exporter
import options
import shutil
import os


# Plugin signature
plugin = {
    'name': 'Sequence Selector',
    'author': 'ejrbuss',
    'description': 'Selects exams in a round robin sequence for the provided class list'
}


def mix(files, data):
    """
    Selects exams in round robin sequence
    """
    logging.info('Performing sequence mixing')
    # Name file versions
    for n, file in enumerate(files):
        os.rename(file, (chr(n + ord('A')) if options.state.alphabetize() else str(n + 1)) + '.mix')
    # Mix data
    for n, row in enumerate(data):
        n = str(chr(n % len(files) + ord('A')) if options.state.alphabetize() else n % len(files) + 1)
        shutil.copy(n + '.mix', n + '_' + (row['number'] if row['number'] != '' else row['name']) + '.mix')


def load():
    # Add sequence selector
    exporter.add_selector({
        'name': 'sequence',
        'mix': mix
    })
    # Return signature
    return plugin


def unload():
    pass
