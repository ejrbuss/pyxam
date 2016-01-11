# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import os
import shutil


# Module Imports


import logger


# Global Variables


TEMP = ''
OUT = ''


# Util Methods


def make_cwd(path):
    """
    Change the CWD to the directory of a given file.

    Raises FileNotFoundError if the path does no point to a file

    :param path: The path to a file
    :return: None
    """
    logger.log('fileutil.read', 'Setting CWD to: ' + os.path.dirname(path))
    os.chdir(os.path.dirname(path))


def read(path):
    """
    Open and read a file as a str.

    Raises FileNotFoundError if the path does not point to a file
    Raises ADirectoryError if the path points to a directory on posix (linux) systems
    Raises PermissionError if the path points to a directory on nt (windows) systems

    :param path: The relative or absolute path for the file
    :return: A str representation of the file contents
    """
    logger.log('fileutil.read', 'Reading file: ' + path)
    with open(os.path.abspath(path.replace('\\ ', ' ')), 'r') as reader:
        buffer = reader.read()
    return buffer


def write(path, buffer):
    """
    Open and write a str to a file.

    Raises IOError if the path points to an unwritable file
    Raises TypeError if the buffer is not a str

    :param path: The relative or absolute path for the file
    :param buffer: The str to write to file
    :return: None
    """
    logger.log('fileutil.write', 'Writing to file: ' + path)
    with open(os.path.abspath(path.replace('\\ ', ' ')), 'w') as writer:
        writer.write(buffer)


def remove(path):
    """
    Remove a file or directory. If removing a directory all contents of that directory will also be removed.

    Raises FileNotFoundError if the path does not point to a file or directory
    Raises OSError if path points to symbolic link

    :param path:The relative or absolute path for the file or directory
    :return: None
    """
    logger.log('fileutil.remove', 'Removing file or directory: ' + path)
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)


def make_temp(path):
    """
    Create a TEMP directory.

    :param path: The relative or absolute path for the directory
    :return: None
    """
    logger.log('fileutil.make_tmp', 'Creating temporary directory: ' + path)
    global TEMP
    TEMP = path
    if not os.path.exists(path):
        os.mkdir(path)


def make_out(path):
    """
    Create an OUT directory.

    :param path: The relative or absolute path for the directory
    :return: None
    """
    logger.log('fileutil.make_out', 'Creating output directory: ' + path)
    global OUT
    OUT = path
    if not os.path.exists(path):
        os.mkdir(path)


def copy_out(path):
    """
    Copy a file from the TEMP directory to the OUT directory.
    If either TEMP or OUT has been created the other will point to the CWD.

    Raises Error if both TEMP and OUT have not been created

    :param path: The relative path to the file within TEMP
    :return: None
    """
    logger.log('fileutil.copy_out', 'Copying file out: ' + path)
    shutil.copy(TEMP + '/' + path if len(TEMP) > 0 else path, OUT + '/' + path if len(OUT) > 0 else path)


def remove_temp():
    """
    Remove the TEMP directory and all its content.

    Raises Error if TEMP has not been created or is set to the CWD

    :return: None
    """
    logger.log('fileutil.remove_temp', 'Removing temporary directory: ' + TEMP)
    if len(TEMP) == 0:
        raise shutil.Error('No TEMP directory')
    remove(TEMP)


def read_temp(path):
    """
    Open and read a file as a str from the TEMP directory.

    Raises FileNotFoundError if the path does not point to a file
    Raises ADirectoryError if the path points to a directory on posix (linux) systems
    Raises PermissionError if the path points to a directory on nt (windows) systems

    :param path: The relative or absolute path to file within TEMP
    :return: A str representation of the file contents
    """
    return read(TEMP + '/' + path)


def write_temp(path, buffer):
    """
    Open and write a str to a file from the TEMP directory.

    Raises IOError if the path points to an unwritable file
    Raises TypeError if the buffer is not a str

    :param path: The relative or absolute path for the file within TEMP
    :param buffer: The str to write to file
    :return: None
    """
    write(TEMP + '/' + path, buffer)