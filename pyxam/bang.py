# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module bang

This module prepossesses the template file runs all inline commands prior to weaving.

Commands can be thought of in the same way as preprocessor directives in c. Commands appear in comments. When a command
name is recognized the contents of the comment are replaced with the result of a function that corresponds to that
command. Commands can have arguments but importantly are not reprocessed. All commands should appear in a comment block
of the format being worked with and must be preceded with the `pyxam!` prefix to avoid confusion.



An example usage of a mock comman        x = 3d named `cmd`:

```
This is template file
# This is a normal comment
Some more text
# pyxam!cmd
That last comment was a command
```
"""
import fileutil
import formatter
import options
import logging
import re
import os


# A dictionary containing all currently loaded name command pairs
commands = {}


def add_command(name, command):
    """
    Add a name, command pair to commands. This function is meant to be used by plugin files in order to add commands.
    Commands must take an argument which is whatever portion of the comment was not part of the command call. Here is an
    example implementation of a mock command `Hello World` which replaces all instances of `pyxam!hello world` with
    `Hello World!!!`:

    ```python
    import bang

    def hello_world(args):
        return 'Hello World!!!'

    bang.add_command('hello world', hello_world)
    ```

    :param name: The name of the command
    :param command: The command function
    """
    commands[name] = command


def run_commands():
    """
    Parses the template, runs all matched commands. The result of the command replaces the command call in the template.
    The resulting string is copied to the tmp directory and the template option is pointed towards the new file.
    """
    try:
        # Try and find an appropriate parser
        parser = formatter.formats[options.state.template().split('.')[-1]]
    except:
        raise formatter.FormatError('Unknown format')
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
                        buffer = buffer.replace(comment[0], ' ' + command(args.replace(name, '', 1).strip()))
                        break;
    # Move template
    options.state.template(options.state.tmp() + '/template/' + os.path.basename(options.state.template()))
    if not os.path.exists(options.state.cwd() + '/template'):
        os.mkdir(options.state.cwd() + '/template')
    # Write result to new template
    fileutil.write(options.state.template(), buffer)


