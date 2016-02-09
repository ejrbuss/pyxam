from exporter import  add_selector
from options import state
from fileutil import read
from fileutil import write

plugin = {
    'name': 'Sequence Selector',
    'author': 'ejrbuss',
    'description': 'Selects exams in a round robin sequence for the provided class list'
}


def mix(files, data):
    for n, file in enumerate(files):
        write((chr(n + ord('A')) if state.alphabetize() else str(n + 1)) + '.mix', read(file))
    for n, row in enumerate(data):
        n = str(chr(n % len(files) + ord('A')) if state.alphabetize() else n % len(files) + 1)
        if row['number'] != '':
            write(n + '_' + (row['number'] if row['number'] != '' else row['name']) + '.mix', read(file))


def load():
    add_selector({
        'name': 'sequence',
        'description': 'Selects exams in round robin sequence',
        'mix': mix
    })
    return plugin


def unload():
    pass
