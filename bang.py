# Author: Eric Buss <ebuss@ualberta.ca> 2016
import fileutil
import formatter
import options
import logging
import re
import os


# A dict containing all currently loaded name -> command pairs
commands = {}


def add_command(name, command):
    """
    Add a name -> command pair to commands
    :param name: The name of the command
    :param command: The command function
    :return: None
    """
    commands[name] = command


def run_commands():
    """
    Parses the template document, runs all matched commands.
    The result of the command replaces the command call in the docment.
    The resulting string is copied to the tmp directory and used as the template after this point.
    :return: None
    """
    try:
        # Try and find an appropriate parser
        parser = formatter.formats[options.state.template().split('.')[-1]]
    except:
        raise options.FormatError('Unknown format')
    logging.info('Using ' + parser['extensions'][0] + ' format to parse pyxam! in ' + options.state.template())
    # Read the template
    buffer = fileutil.read(options.state.template())
    # Look through tokens and find all comment tokens
    for comment_token in [token for token in parser['format'].values() if 'comment' in token.name]:
        # Find all token matches within the template source irregardless of starting point
        for comment in re.findall(comment_token.regex.replace('^', ''), buffer, re.DOTALL):
            # Check if it is a pyxam! command
            if comment[1].strip().startswith('pyxam!'):
                # Parse the args
                args = comment[1].strip().replace('pyxam!', '')
                # Check if command is in command list
                for name, command in commands.items():
                    if args.startswith(name):
                        # Run command
                        buffer = buffer.replace(comment[0], command(args.replace(name, '', 1).strip()))
                        break;
    # Move template
    options.state.template(options.state.tmp() + '/template/' + os.path.basename(options.state.template()))
    if not os.path.exists('template'):
        os.mkdir('template')
    # Write result to new template
    fileutil.write(options.state.template(), buffer)


