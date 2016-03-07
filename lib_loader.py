# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import libs.pweave
import options
import fileutil
import subprocess
import os


class LibError(Exception):
    pass


def weave():
    # TODO Pweave formats
    for n in range(options.state.number()):
        src, path = fileutil.read(options.state.template()), 'template_' + str(n) + '.tex'
        # fileutil.write(path, src)
        # continue
        fileutil.write(path, src)
        try:
            libs.pweave.weave(path, doctype='tex', figdir=options.state.figure(), shell=options.state.shell())
            logging.info('Weaved ' + str(n + 1) + ' of ' + str(options.state.number()))
        except:
            raise
            raise LibError('Failed to Pweave file: ' + options.state.tmp() + '/' + str(n))


def gs(path):
    """
    Convert pdf image file to png using ghostscript
    :param name:
    :return:
    """
    try:
        with open(os.devnull, 'r') as stdin:
            subprocess.check_output(['gs', '-sDEVICE=pngalpha', '-sOutputFile=' + path[:-3] + 'png', path], stdin=stdin)
    except:
        exit('Ghostscript call failed')
    logging.info('Used ghostscript to convert ' + path + ' to png')
    return path[:-3] + 'png'
