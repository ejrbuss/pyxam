# Author: Eric Buss <ebuss@ualberta.ca> 2016
import logging
import os
import shutil
import distutils.dir_util
import options


def build_files():
    """
    Find the absolute file path for the template, tmp directory, and out directory and replace their options.
    Create tmp and out if necessary. Warns user if tmp is going to be overridden.
    Change the current working directory to tmp.
    :return: None
    """
    # Get absolute paths
    options.state.template(os.path.abspath(options.state.template()))
    options.add_option('cwd', '', 'The original CWD', os.getcwd(), str)
    os.chdir(os.path.abspath(os.path.dirname(options.state.template())))
    options.state.out(os.path.abspath(os.path.curdir) + '/' + options.state.out())
    options.state.tmp(os.path.abspath(os.path.curdir) + '/' + options.state.tmp())
    options.state.figure(options.state.tmp() + '/' + options.state.figure())
    logging.info('Fixed paths')
    # Overwrite warning
    if os.path.isdir(options.state.tmp()) and not options.state.api() and \
            input('Temporary directory already exists. Continue anyways? (y/n)') != 'y':
        exit('Cancelling operation.')
    # Build tmp directory
    if not os.path.exists(options.state.tmp()):
        os.mkdir(options.state.tmp())
    # Build out directory
    if not os.path.exists(options.state.out()):
        os.mkdir(options.state.out())
    # Change current working directory
    os.chdir(options.state.tmp())
    logging.info('Built directories')


def cleanup():
    """
    When not in debug mode remove all temporary folders.
    :return: None
    """
    if not options.state.debug():
        remove(options.state.tmp())
    # Reset current working directory so plugins can be unloaded
    os.chdir(options.state.cwd())


def with_extension(extension):
    """
    Return a list of files in the current working directory that match the given extension.
    :param extension: The extension to match
    :return: The list of files
    """
    return [file for file in os.listdir(os.path.curdir) if file.endswith(extension)]


def read(file):
    """
    Read a string from a file.
    :param file: The relative or absolute path to the file
    :return: A string representation of the contents of that file
    """
    logging.info('Reading file: ' + file)
    with open(file, 'r') as reader:
        return reader.read()


def write(file, src):
    """
    Write a string to a file.
    :param file: The relative or absolute path to the file
    :param src: The string to write to the file
    :return: None
    """
    logging.info('Writing file: ' + file)
    with open(file, 'w') as writer:
        writer.write(src)


def copy_figure():
    """
    Copy the figure directory to the out directory along with its children.
    :return: None
    """
    logging.info('Copying figures out')
    figure = options.state.out() + '/' + os.path.basename(options.state.figure())
    if not os.path.exists(figure):
        os.mkdir(figure)
    distutils.dir_util.copy_tree(options.state.figure(), figure)


def remove(file):
    """
    Remove a file or directory. If removing a directory all contents of that directory will also be removed.
    :param file: The relative or absolute path for the file or directory
    :return: None
    """
    logging.info('Removing file or directory: ' + file)
    if os.path.isfile(file):
        os.remove(file)
    else:
        shutil.rmtree(file)


def isbin(file):
    """
    Check if a file is a binary file.
    :param file: The file to check
    :return: True if the file is a binary file
    """
    try:
        read(file)
        return False
    except UnicodeDecodeError:
       return True

