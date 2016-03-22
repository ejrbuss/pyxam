#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Module pyxam

This is the primary script for Pyxam. This script can be run from the command line with Pyxam's options or run in api
mode from another python script. This script also checks Python dependencies for:

`matplotlib` Needed for generating figure images

`numpy` Needed for generating figure images

"""


# TODO finish docs
# TODO tests
# TODO move pweave to dependency
# TODO cleanup
# TODO test html
# TODO org mode
# TODO markdown
# TODO calculated


import sys
import process_list
import options
import bang
import plugin_loader
import fileutil
import lib_loader
import formatter
import exporter 


# Module Dependencies
try:
    import matplotlib
except ImportError:
    exit('matplotlib is required for Pyxam. Please run:\n\t pip install matplotlib')
try:
    import numpy
except ImportError:
    exit('numpy is required for Pyxam. Please run:\n\t pip install numpy')


# Pyxam Version Number
__version__ = 'v0.3.2'


# Pyxam Title String
TITLE = '    ____                           \n' \
        '   / __ \__  ___  ______ _____ ___ \n' \
        '  / /_/ / / / / |/_/ __ `/ __ `__ \\ \n' \
        ' / ____/ /_/ />  </ /_/ / / / / / /\n' \
        '/_/    \__, /_/|_|\__,_/_/ /_/ /_/ \n' \
        '      /____/'


def welcome():
    """
    Prints the Pyxam title and version number when not in api mode.
    """
    if not options.state.api():
        print(TITLE, '\n\n\tLatex Exam Generation.', __version__, '\n\n')


def goodbye():
    """
    Prints a goodbye message when not in api mode.
    """
    if not options.state.api():
        print('Thanks for using Pyxam, have a nice day!')


def start(args, api=True):
    """
    Start Pyxam with a set of options.

    :param args: A list of options provided in command line syntax
    :param api: A flag indicating if Pyxam is being called as an api

    Start adds all needed processes to the option list and then loops % pyxam!link process_list.consume until there are
    no processes left.
    """
    # Clear last session data
    options.clear()
    process_list.clear()
    # Add api option
    options.add_option('api', '-api', 'Run Pyxam in api mode', True, bool, value=api)
    process_list.append([
        options.load_options,
        welcome,
        plugin_loader.load_plugins,
        options.load_template,
        fileutil.build_files,
        bang.run_commands,
        lib_loader.weave,
        formatter.parse,
        formatter.compose,
        exporter.export,
        fileutil.cleanup,
        plugin_loader.unload_plugins,
        goodbye])
    while process_list.ready():
        args = process_list.consume(args)


if __name__ == '__main__':
    # If main start Pyxam with argv and API mode False
    # Slice argv so as not to pass ./Pyxam.py
    start(sys.argv[1:], api=False)


