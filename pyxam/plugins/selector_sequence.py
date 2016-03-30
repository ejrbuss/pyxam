# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import exporter
import options
import fileutil
import shutil
import os


signature = 'sequence selector', 'ejrbuss', 'round robin selector'
# Plugin signature


def mix(files, data):
    """
    Selects exams in round robin sequence
    """
    logging.info('Performing sequence mixing')
    if not options.state.api():
        print('Performing round robin mixing of', len(files), 'exam versions among', len(data), 'students.\n')
    # Fix template files
    # Mix data
    for n, row in enumerate(data):
        n = str(chr(n % len(files) + ord('A')) if options.state.alphabetize() else n % len(files) + 1)
        fileutil.write(
            options.state.cwd() + '/' + n + '_' + row['name'].replace(' ', '_') + '_' + row['number'] + '.mix',
            fileutil.read(options.state.cwd() + '/' + n + '.mix').
                replace('$tudent__name', ' ' + row['name']).
                replace('$tudent__number', ' ' + row['number'])
        )
    for file in files:
        fileutil.write(
            file,
            fileutil.read(file).
                replace('$tudent__name', '').
                replace('$tudent__number', '')
        )


def load():
    # Add sequence selector
    exporter.add_selector('sequence', mix)
    # Return signature
    return signature


def unload():
    pass
