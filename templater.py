# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import re
import os
import random


# Module Imports


import logger
import fileutil
import pyxamopts


# Utility Methods


def pre_process(buffer):
    """
    Checks str for \Parg command and collects all arguments into a new PyxamOptions compatible instance.

    :param buffer: The str to check
    :return: A PyxamOptions compatible instance
    """
    parsed = tex_match(buffer, 'Parg')
    args = ''
    for pair in parsed:
        # Collect arguments
        args = args + buffer[pair[0]:pair[1]] + ' '
    return pyxamopts.init_arg_parser(args.split(' '))


def pimport(buffer, sample):
    """
    Parse the \Pimport statements from a file and replace them with the files their arguments point to.

    :param buffer: The str to parse
    :param sample: The default number of samples for any \Pimport statement without a specified sample number
    :return:
    """
    # Get the full matched str, reverse the list so it can be correctly inserted into
    unparsed = tex_match(buffer, r'Pimport(\[[0-9]+\])?', True)[::-1]
    # Loop through imports
    for pair in unparsed:
        # Get just the argument str
        command = buffer[pair[0]:pair[1]]
        logger.log('templater.pimport', 'Importing: ' + command)
        arg = tex_match(command, r'Pimport(\[[0-9]+\])?')
        arg = command[arg[0][0]:arg[0][1]]
        # Check if sample number is specified
        if '[' in command:
            try:
                sample = int(re.search('\[([0-9]+)\]', command).group(1))
                logger.log('templater.pimport', 'Changed sample size to: ' + str(sample))
            except:
                logger.log('templater.pimport', 'Failed to parse argument from: ' + command, logger.LEVEL.WARNING)
        # Get import files
        files = walk(arg.split(',')[0])
        logger.log('templater.pimport', 'Matched files: ' + str(files))
        removed = []
        # Insert files
        if len(files) > 0:
            for n in range(sample):
                # Check if out of files to sample
                if len(files) == 0:
                    files = files + removed
                    print(' * WARNING * questions repeated:', sample, '>', len(files))
                file = random.choice(files)
                files.remove(file)
                removed.append(file)
                buffer = buffer[:pair[0]] + '\n' + fileutil.read(file) + buffer[pair[1]:]
                # Prevent the next file from writing over the first
                pair = (pair[0], pair[0])
    return buffer


def walk(arg):
    """
    Finds the specified files to import.
    Paths separated by '|' will all be added to the list.
    Paths that are directories will have their full file contentents added to the list.

    Exits if file cannot be found or file is symbolic link

    :param arg: The path argument
    :return: A list of files to import
    """
    paths = []
    try:
        for path in arg.split('|'):
            if os.path.isfile(path):
                paths.append(path)
            else:
                for file in os.listdir(path):
                    if os.path.isfile(path + '/' + file):
                        paths.append(path + '/' + file)
    except:
        exit('Failed to import files from argument: ' + arg)
    return paths


def parse_constant(buffer, old, new):
    """
    Replace a \Pconst command with a new value.

    :param buffer: The str to perform the replacements on
    :param old: The argument of \Pconst
    :param new: The replacement value
    :return: The str with the replacements made
    """
    logger.log('templater.parse_constant', 'Replacing ' + old)
    # Reverse the list so it can be correctly removed back to front
    unparsed = tex_match(buffer, 'Pconst', True)[::-1]
    for pair in unparsed:
        command = buffer[pair[0]:pair[1]]
        arg = tex_match(command, 'Pconst')
        arg = command[arg[0][0]:arg[0][1]]
        if arg == old:
            buffer = buffer[:pair[0]] + new + buffer[pair[1]:]
    return buffer


def clean(buffer):  # !!!!!!!!!! to be exteneded !!!!!!!!!!!
    """
    Removes the \Parg command from the buffer.
    Extend in the future to help cleanup imported questions.

    :param buffer: The str to clean
    :return: The cleaned str
    """
    # Reverse the list so it can be correctly removed back to front
    unparsed = tex_match(buffer, 'Parg', True)[::-1]
    for pair in unparsed:
        buffer = buffer[:pair[0]] + buffer[pair[1]:]
    return buffer


def tex_match(buffer, command, unparsed=False):
    """
    Returns a list of tuples which indicate the starting and ending indices for matches.
    If the flag is not set the match is the arguments for the given command.
    If the flag is set the match is the command and argument together.

    :param buffer: The str to match from
    :param command: The command to match
    :param unparsed: Flag for returning the entire command with its args
    :return: A list of starting and ending indices
    """
    parsed = []
    # Match the first group to skip the look behind checks
    buffer = verb(buffer)
    matched = [(m.start(1), m.end(1)) for m in
        re.finditer(r'(\\' + command + '\{((\\})|([^}]))*?})', buffer)]
    if unparsed:
        return matched
    for pair in matched:
        match = re.search('{', buffer[pair[0]:])
        parsed.append((pair[0] + match.start() + 1, pair[1] - 1))
    return parsed

def verb(buffer):
    buffer = re.sub(r'%.*', lambda m: ' '*len(m.group()), buffer)
    buffer = re.sub(r'\\verb[^ ]*]', lambda m: ' '*len(m.group()), buffer)
    buffer = re.sub(r'\\verb!? *[^ ]*', lambda m: ' '*len(m.group()), buffer)
    buffer = re.sub(r'\\begin\{verbatim}(.|\n)*?\\end\{verbatim}', lambda m: ' '*len(m.group()), buffer)
    return buffer