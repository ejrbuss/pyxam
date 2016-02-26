#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports
from sys import argv
from process_list import ready
from process_list import append
from process_list import consume
from options import state
from options import add_option
from options import load_options
from options import load_template
from plugin_loader import load_plugins
from plugin_loader import unload_plugins
from fileutil import cleanup
from fileutil import build_files
from lib_loader import weave
from formatter import pyxam_bang
from formatter import parse
from formatter import compose
from exporter import export


# Pyxam Version Number
VERSION = 'v0.3.0'
# Pyxam Title String
TITLE = '    ____                           \n' \
        '   / __ \__  ___  ______ _____ ___ \n' \
        '  / /_/ / / / / |/_/ __ `/ __ `__ \\ \n' \
        ' / ____/ /_/ />  </ /_/ / / / / / /\n' \
        '/_/    \__, /_/|_|\__,_/_/ /_/ /_/ \n' \
        '      /____/'

# TODO constants in template file
# TODO question importing and shuffling
# TODO New readme and automatic documentation


def welcome():
    """
    Prints the Pyxam title and version number when not in api mode.
    :return: None
    """
    if not state.api():
        print(TITLE, '\n\n\tLatex Exam Generation.', VERSION, '\n\n')


def goodbye():
    """
    Prints a goodbye message when not in api mode.
    :return: None
    """
    if not state.api():
        print('Thanks for using Pyxam, have a nice day!')


def start(options, api=True):
    """
    Start Pyxam with a set of options.
    :param options: A list of options provided in command line syntax
    :param api: A flag indicating if Pyxm is being called as an api, defaults to True
    :return: None
    """
    add_option('api', '-api', 'Run Pyxam in api mode', True, bool, value=api)
    append([load_options, welcome, load_plugins, load_template, pyxam_bang, build_files, weave, parse, compose, export, cleanup, unload_plugins, goodbye])
    while ready():
        options = consume(options)


if __name__ == '__main__':
    # If main start Pyxam with argv and API mode False
    # Slice argv so as not to pass ./Pyxam.py
    start(argv[1:], api=False)


