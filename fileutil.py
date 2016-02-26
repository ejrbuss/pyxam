import logging
import os
from shutil import rmtree
from distutils.dir_util import copy_tree
from options import add_option
from options import state


def build_files():
    state.template(os.path.abspath(state.template()))
    add_option('cwd', '', 'The original CWD', os.getcwd(), str)
    os.chdir(os.path.abspath(os.path.dirname(state.template())))
    state.out(os.path.abspath(os.path.curdir) + '/' + state.out())
    state.tmp(os.path.abspath(os.path.curdir) + '/' + state.tmp())
    state.figure(state.tmp() + '/' + state.figure())
    logging.info('Fixed paths')

    if os.path.isdir(state.tmp()) and not state.api() and \
            input('Temporary directory already exists. Continue anyways? (y/n)') != 'y':
        exit('Cancelling operation.')
    if not os.path.exists(state.tmp()):
        os.mkdir(state.tmp())
    if not os.path.exists(state.out()):
        os.mkdir(state.out())
    os.chdir(state.tmp())
    logging.info('Built directories')


def cleanup():
    if not state.debug():
        remove(state.tmp())
    os.chdir(state.cwd())


def read(file):
    logging.info('Reading file: ' + file)
    with open(file, 'r') as reader:
        return reader.read()


def with_extension(extension):
    return [file for file in os.listdir( os.path.curdir ) if file.endswith(extension)]


def write(file, src):
    logging.info('Writing file: ' + file)
    with open(file, 'w') as writer:
        return writer.write(src)


def copy_figure():
    figure = state.out() + '/' + os.path.basename(state.figure())
    if not os.path.exists(figure):
        os.mkdir(figure)
    copy_tree(state.figure(), figure)


def remove(file):
    """
    Remove a file or directory. If removing a directory all contents of that directory will also be removed.

    Raises FileNotFoundError if the os.path does not point to a file or directory
    Raises OSError if os.path points to symbolic link

    :param file:The relative or absolute os.path for the file or directory
    :return: None
    """
    logging.info('Removing file or directory: ' + file)
    if os.path.isfile(file):
        os.remove(file)
    else:
        rmtree(file)

