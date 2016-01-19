# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import re
import os
import random


# Module Imports


import logger
import fileutil
import pyxamopts


# Command Class

class Command:

    def __init__(self, buffer, initial, final):
        """
        Initialize Command fields including the initial and final indices, the entire block str, the name,
        any provided arguments and any content of the command.

        :param buffer: The string to read the Command from
        :param initial: The starting block index
        :param final: The ending block index
        :return: A new Command objectrequest
        """
        self.initial = initial
        self.final = final
        self.block = buffer[initial:final]
        self.name = re.search(r'.(.*?)(\[.*?\])?\{.*\}', self.block, re.DOTALL).group(1)
        try:
            self.arg = re.search(r'.*?\[(.*?)\]', self.block, re.DOTALL).group(1)
        except:
            self.arg = ''
        self.content = re.search(r'.*?\{(.*)\}', self.block, re.DOTALL).group(1)

    def clear(self, buffer):
        """
        Remove this Command from the given buffer.
        This should only be called on the buffer that this Command was created from.

        :param buffer: The buffer to remove the request from
        :return: The new buffer
        """
        return buffer[:self.initial] + buffer[self.final:]

    def rewrap(self, buffer, pre, post):
        """
        Rewrap the content of this Command with the given prefix and postfix.
        This should only be called on the buffer that this Command was created from.

        :param buffer: The buffer to remove the request from
        :param pre: The prefix for the content
        :param post: The postfix for the content
        :return: The new buffer
        """
        return buffer[:self.initial] + pre + self.content + post + buffer[self.final:]

    def replace(self, buffer, new):
        """
        Replace the conetent of this Command with a new str.
        This should only be called on the buffer that this Command was created from.

        :param buffer: The buffer to remove the request from
        :param new: The replacement str
        :return: The new buffer
        """
        return buffer[:self.initial] + new + buffer[self.final:]


# Section Class

class Section:

    def __init__(self, buffer, initial, final):
        """
        Initialize Section fields including the initial and final indices, the entire block str, the name,
        any provided arguments and any content of the section.

        :param buffer: The string to read the Section from
        :param initial: The starting block index
        :param final: The ending block index
        :return: A new Section object
        """
        self.initial = initial
        self.final = final
        self.block = buffer[initial:final]
        self.name = re.search(r'.*?\{(.*?)\}.*', self.block, re.DOTALL).group(1)
        try:
            self.arg = re.search(r'.*?\[(.*?)\]', self.block, re.DOTALL).group(1)
        except:
            self.arg = ''
        self.content = re.search(r'/*?\}(.*?)\\end\{' + self.name + r'\}', self.block, re.DOTALL).group(1)

    def clear(self, buffer):
        """
        Remove this Section from the given buffer.
        This should only be called on the buffer that this Section was created from.

        :param buffer: The buffer to remove the request from
        :return: The new buffer
        """
        return buffer[:self.initial] + buffer[self.final:]

    def insert(self, buffer, new):
        return buffer[:self.initial] + '\\begin{' + self.name + '}\n' + new + '\n\\end{' + self.name + '}' + \
               buffer[self.final:]

    def replace(self, buffer, new):
        """
        Replace the conetent of this Section with a new str.
        This should only be called on the buffer that this Section was created from.

        :param buffer: The buffer to remove the request from
        :param new: The replacement str
        :return: The new buffer
        """
        return buffer[:self.initial] + new + buffer[self.final:]

# Utility Methods


def pre_process(buffer):
    """
    Checks str for \Parg command and collects all arguments into a new PyxamOptions compatible instance.

    :param buffer: The str to check
    :return: A PyxamOptions compatible instance
    """
    requests = command_match(buffer, 'Parg')
    args = ''
    for request in requests:
        # Collect arguments
        args = request.content + ' '
    return pyxamopts.init_arg_parser(args.split(' '))


def pimport(buffer, sample):
    """
    Parse the \Pimport statements from a file and replace them with the files their arguments point to.

    :param buffer: The str to parse
    :param sample: The default number of samples for any \Pimport statement without a specified sample number
    :return:
    """
    requests = command_match(buffer, 'Pimport')
    # Loop through imports
    for request in requests:
        # Check if sample number is specified
        if len(request.arg) > 0:
            try:
                sample = int(request.arg)
                logger.log('templater.pimport', 'Changed sample size to: ' + str(sample))
            except:
                logger.log('templater.pimport', 'Failed to parse argument from: ' + request.block, logger.LEVEL.WARNING)
        # Get import files
        files = walk(request.content.split(',')[0])
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
                buffer = request.replace(buffer, '\n' + fileutil.read(file))
                # Prevent the next file from writing over the first
                request.final = request.initial
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


def shuffle(buffer, rearrange):
    """
    Rearrange multiple choice questions.

    :param buffer: The str to rearrange the questions in
    :param rearrange: a flag for disabling rearrangement
    :return: The rearranged buffer
    """
    if not buffer:
        return buffer
    for section in section_match(buffer, 'choices'):
        choices = section.content.split('\n')
        while '' in choices:
            choices.remove('')
        tmp = choices[:]
        while tmp == choices:
            random.shuffle(choices)
        buffer = section.insert(buffer, '\n'.join(choices))
    return buffer


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
    requests = command_match(buffer, 'Pconst')
    for request in requests:
        if request.content == old:
            buffer = request.replace(buffer, new)
    return buffer


def clean(buffer):  # !!!!!!!!!! to be exteneded !!!!!!!!!!!
    """
    Removes the \Parg command from the buffer.
    Extend in the future to help cleanup imported questions.

    :param buffer: The str to clean
    :return: The cleaned str
    """
    # Reverse the list so it can be correctly removed back to front
    requests = command_match(buffer, 'Parg')
    for request in requests:
        buffer = request.clear(buffer)
    return buffer


def command_match(buffer, command):
    """
    Returns a list of Command objects that match the command.
    The list is reversed so that matched objects can be easily deleted.

    :param buffer: The str to match from
    :param command: The command to match
    :return: A list of requests
    """
    requests = []
    matched = [(m.start(1), m.end(1)) for m in
        re.finditer(r'(\\' + command + '(\[.*?\])?\{((\\})|([^}]))*?})', protect(buffer))]
    for pair in matched:
        requests.append(Command(buffer, pair[0], pair[1]))
    return requests[::-1]


def section_match(buffer, name):
    """
    Returns a list of Section objects that match the name.
    The list is reversed so that matched objects can be easily deleted.

    :param buffer: The str to match from
    :param name: The section to match
    :return: A list of requests
    """
    requests = []
    matched = [(m.start(1), m.end(1)) for m in
               re.finditer(r'(\\begin(\[.*?\])?\{' + name + r'\}(.|\n)*?\\end\{' + name + r'\})', protect(buffer))]
    for pair in matched:
        requests.append(Section(buffer, pair[0], pair[1]))
    return requests[::-1]


def protect(buffer):
    """
    Replace parseable code with whitespace if that code is in a verbatim block or comment.

    :param buffer: The buffer to protect
    :return: The protected buffer
    """
    buffer = re.sub(r'%.*', lambda m: ' '*len(m.group()), buffer)
    buffer = re.sub(r'\\verb[^ ]*]', lambda m: ' '*len(m.group()), buffer)
    buffer = re.sub(r'\\verb!? *[^ ]*', lambda m: ' '*len(m.group()), buffer)
    buffer = re.sub(r'\\begin\{verbatim}(.|\n)*?\\end\{verbatim}', lambda m: ' '*len(m.group()), buffer)
    return buffer