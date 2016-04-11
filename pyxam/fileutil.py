# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module fileutil

This Module provides helper functions for working with files.
"""
import distutils.dir_util
import parser_composer
import logging
import options
import shutil
import time
import os


def build_files():
    """
    Finds the absolute file path for the template, tmp directory, and out directory and updates their options to point
    to their absolute path. Also creates the tmp and out directories if necessary. Warns user if tmp is going to be
    overridden as this will delete any leftover files. Finally changes the current working directory to tmp.
    """
    # Get absolute paths
    options.state.template(os.path.abspath(options.state.template()))
    options.add_option('cwd', '', 'The original CWD', os.getcwd(), str)
    os.chdir(os.path.abspath(os.path.dirname(options.state.template())))
    if os.path.abspath(options.state.out()) != options.state.out():
        options.state.out(options.state.cwd() + '/' + options.state.out())
    if os.path.abspath(options.state.tmp()) != options.state.tmp():
        options.state.tmp(options.state.cwd() + '/' + options.state.tmp())
    if os.path.abspath(options.state.figure()) != options.state.figure():
        options.state.figure(options.state.tmp() + '/' + options.state.figure())
    logging.info('Fixed paths')
    # Overwrite warning
    if os.path.isdir(options.state.tmp()) and not options.state.api() and \
            input('Temporary directory already exists. Continue anyways? (y/n)') != 'y':
        exit('Cancelling operation.')
    # Build tmp directory
    if not os.path.exists(options.state.tmp()):
        os.mkdir(options.state.tmp())
    else:
        cleanup()
        if not os.path.exists(options.state.tmp()):
            os.mkdir(options.state.tmp())
    # Build out directory
    if not os.path.exists(options.state.out()):
        os.mkdir(options.state.out())
    # Change current working directory
    options.state.cwd(options.state.tmp())
    logging.info('Built directories')


def export():
    """
    Copies all .cmp files and figures from the tmp directory to the out directory. Files are renamed with their title,
    postfix, correct extension and solution tag if the solutions option is set.
    """
    for file in with_extension('.cmp'):
        move(
            file,
            options.state.out() + '/' +
            options.state.title() + '_' +
            os.path.basename(file[:-4]) +
            ('_solutions' if options.state.solutions() else '') +
            '.' + parser_composer.get_extension()
        )
    # Export figures
    copy_figure()


def cleanup():
    """
    Removes the temporary directory and resets the current working directory.
    """
    remove(options.state.tmp())
    wait_on_io(lambda: os.path.exists(options.state.tmp()))
    # Reset current working directory so plugins can be unloaded
    options.state.cwd(os.curdir)


def get_extension(file):
    """
    Get the file extension for a file.
    :param file: The path of the file to get the extension of
    :return: The extension
    """
    return file.split('.')[-1]


def with_extension(ext):
    """
    Find all files in the current working directory that match the given extension or extensions.

    :param ext: The extension or extensions to match
    :return: a list of files that end in the provided extension or extensions
    """
    if type(ext) == str:
        return [options.state.cwd() + '/' + file for file in os.listdir(options.state.cwd()) if file.endswith(ext)]
    return sum((with_extension(e) for e in ext), [])


def read(file):
    """
    Read a string from a file.

    :param file: The relative or absolute path to the file to read
    :return: The string contents of the file
    """
    logging.info('Reading file: ' + file)
    with open(file, 'r') as reader:
        return reader.read()


def write(file, src):
    """
    Write a string to a file.

    :param file: The relative or absolute path to the file to write to
    :param src: The string to write to the file
    """
    logging.info('Writing file: ' + file)
    with open(file, 'w') as writer:
        writer.write(src)


def copy_figure():
    """
    Copy the figure directory to the out directory along with its children.
    """
    if os.path.isdir(options.state.figure()) and os.listdir(options.state.figure()):
        logging.info('Copying figures out')
        figure = options.state.out() + '/' + os.path.basename(options.state.figure())
        if not os.path.exists(figure):
            os.mkdir(figure)
        distutils.dir_util.copy_tree(options.state.figure(), figure)


def remove(file):
    """
    Remove a list of files or individual file. If removing a directory all contents of that directory will also be
    removed. When the debug flag is set no files will be removed.

    :param file: The file or files to remove
    """
    if options.state.debug():
        return
    if type(file) == str:
        logging.info('Removing file or directory: ' + file)
        if os.path.isfile(file):
            os.remove(file)
        else:
            shutil.rmtree(file)
    else:
        [remove(f) for f in file]


def move_template(dest):
    """
    Copy the template file to a specified destination. This will update the option and create a new directory if
    necessary.

    :param dest: The new template file destination
    """
    logging.info('Moving template from' + options.state.template() + ' to ' + dest)
    if not os.path.exists(os.path.dirname(dest)):
        os.mkdir(os.path.dirname(dest))
    write(dest, read(options.state.template()))
    options.state.template(dest)


def move(src, dest):
    """
    Moves a file from src to destination.

    :param src: The relative or absolute path for the file or directory to move
    :param dest: The relative or absolute path for the file's destination
    """
    logging.info('Moving ' + src + ' to ' + dest)
    if not os.path.exists(os.path.dirname(dest)):
        os.mkdir(os.path.dirname(dest))
    os.rename(src, dest)


def is_bin(file):
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


def wait_on_io(fn, timeout=5):
    """
    Wait on an io function to finish with a specified timeout. Will wait for the timeout or for the function to return
    False.

    :param fn: The io function to wait on
    :param timeout: The maximum time to wait
    """
    if options.state.debug():
        logging.info('io skipped while in debug')
        return
    logging.info('Waiting on io...')
    start = time.time()
    while fn():
        if time.time() - start > timeout:
            raise TimeoutError('Timed out while waiting on io')
    logging.info('io finished')

