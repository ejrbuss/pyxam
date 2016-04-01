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
import os
import re
import options
import logging
import fileutil
import formatter


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
    parser = formatter.get_format(options.state.template())
    logging.info('Using ' + parser['name'] + ' format to process pyxam! in ' + options.state.template())
    buffer = fileutil.read(options.state.template())
    for comment_token in [token for token in parser['format'].values() if 'comment' in token.name]:
        for comment in re.findall(comment_token.regex, buffer, re.DOTALL):
            result = run_command(comment[1])
            buffer = buffer if result is None else buffer.replace(comment[0], result)
    fileutil.move_template(options.state.tmp() + '/template/' + os.path.basename(options.state.template()))
    fileutil.write(options.state.template(), buffer)


def run_command(block):
    # Check if command is in command list
    for name, command in commands.items():
        if block.strip().startswith('pyxam!' + name):
            options.post('Processed', name, 'command.')
            return command(block.strip().replace('pyxam!' + name, '', 1).strip())