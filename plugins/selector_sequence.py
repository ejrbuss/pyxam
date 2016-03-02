# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import exporter
import options
import fileutil
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

    # Mix data
    for n, row in enumerate(data):
        n = str(chr(n % len(files) + ord('A')) if options.state.alphabetize() else n % len(files) + 1)
        fileutil.write(
            n + '_' + row['name'] + row['number'] + '.mix',
            fileutil.read(n + '.mix').
                replace('$tudent__name', row['name']).
                replace('$tudent__number', row['number'])
        )



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
