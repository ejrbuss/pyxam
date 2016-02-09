import logging
import csv
import re
from os import listdir
from options import state
from fileutil import read
from fileutil import write
from fileutil import copy_figure
from fileutil import with_extension
from formatter import get_extension


class ExportError(Exception):
    pass


_selectors = {}


def export():
    selector = _selectors[state.method()]['mix'](with_extension('.cmp'), csv_read(state.population()))
    for file in with_extension('.mix'):
        write(state.out() + '/' + state.title() + '_' + file[:-3] + get_extension(), read(file))
    if listdir(state.figure()):
        copy_figure()


def csv_read(file):
    try:
        with open(file) as file:
            return [{
                        'number': ' '.join(n for n in row if re.match(r'.*[0-9].*', n)).strip(),
                        'name': ' '.join(s for s in row if not re.match(r'.*[0-9].*', s)).strip()
                    } for row in csv.reader(file)]
    except Exception as e:
        return [{'number': '', 'name': ''}]


def add_selector(selector):
    if ('name' and 'description' and 'mix') in selector:
        _selectors[selector['name']] = selector
    else:
        raise ExportError('Invalid signature for selector')

