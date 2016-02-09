import logging
from os import path
from os import mkdir
from os import chdir
from os import getcwd
from os import remove
from os import listdir
from shutil import rmtree
from distutils.dir_util import copy_tree
from options import load_options
from options import add_option
from options import state


def build_files():
    state.template(path.abspath(state.template()))
    add_option('cwd', '', 'The original CWD', getcwd(), str)
    chdir(path.abspath(path.dirname(state.template())))
    state.out(path.abspath(path.curdir) + '/' + state.out())
    state.tmp(path.abspath(path.curdir) + '/' + state.tmp())
    state.figure(state.tmp() + '/' + state.figure())
    logging.info('Fixed paths')

    if path.isdir(state.tmp()) and not state.api() and \
            input('Temporary directory already exists. Continue anyways? (y/n)') != 'y':
        exit('Cancelling operation.')
    if not path.exists(state.tmp()):
        mkdir(state.tmp())
    if not path.exists(state.out()):
        mkdir(state.out())
    chdir(state.tmp())
    logging.info('Built directories')


def cleanup():
    if not state.debug():
        remove(state.tmp())
    chdir(state.cwd())


def read(file):
    logging.info('Reading file: ' + file)
    with open(file, 'r') as reader:
        return reader.read()


def with_extension(extension):
    return [file for file in listdir( path.curdir ) if file.endswith(extension)]


def write(file, src):
    logging.info('Writing file: ' + file)
    with open(file, 'w') as writer:
        return writer.write(src)


def copy_figure():
    figure = state.out() + '/' + path.basename(state.figure())
    if not path.exists(figure):
        mkdir(figure)
    copy_tree(state.figure(), figure)


def remove(file):
    """
    Remove a file or directory. If removing a directory all contents of that directory will also be removed.

    Raises FileNotFoundError if the path does not point to a file or directory
    Raises OSError if path points to symbolic link

    :param file:The relative or absolute path for the file or directory
    :return: None
    """
    logging.info('Removing file or directory: ' + file)
    if path.isfile(file):
        remove(file)
    else:
        rmtree(file)

