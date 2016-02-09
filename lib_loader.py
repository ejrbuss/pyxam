import logging
from libs import pweave
from options import state
from fileutil import read
from fileutil import write


class LibError(Exception):
    pass


def weave():
    # TODO Pweave formats
    for n in range(state.number()):
        src, path = read(state.template()), 'template_' + str(n)
        write(path, src)
        #try:
        logging.info('Weaved ' + str(n + 1) + ' of ' + str(state.number()))
        pweave.weave(path, doctype='tex', figdir=state.figure(), shell=state.shell())
        #except:
        #    raise LibError('Failed to Pweave file: ' + state.tmp() + '/' + str(n))
