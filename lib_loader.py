# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import libs.pweave
import options
import fileutil


class LibError(Exception):
    pass


def weave():
    # TODO Pweave formats
    for n in range(options.state.number()):
        src, path = fileutil.read(options.state.template()), 'template_' + str(n)
        fileutil.write(path, src)
        try:
            logging.info('Weaved ' + str(n + 1) + ' of ' + str(options.state.number()))
            libs.pweave.weave(path, doctype='tex', figdir=options.state.figure(), shell=options.state.shell())
        except:
            raise LibError('Failed to Pweave file: ' + options.state.tmp() + '/' + str(n))
