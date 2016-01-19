#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import sys


# Module Imports


import core
import pyxamopts

# Global Variables


# Version number
VERSION = 'v0.2.3'


# Utility Methods


def print_title():
    """
    Title created with http://patorjk.com/software/taag/#p=display&f=Slant&t=Type%20Something

    :return: None
    """
    print('    ____                           ')
    print('   / __ \__  ___  ______ _____ ___ ')
    print('  / /_/ / / / / |/_/ __ `/ __ `__ \\')
    print(' / ____/ /_/ />  </ /_/ / / / / / /')
    print('/_/    \__, /_/|_|\__,_/_/ /_/ /_/ ')
    print('      /____/                       ')
    print('\n\tLatex Exam Generation.', VERSION, '\n\n')


# Main


def main():
    """
    Pyxam shell entry point. Makes API call to core.pyxam with command line arguments as parameters.

    :return: None
    """
    print_title()
    if len(sys.argv) == 1: exit("This is Pyxam, enter Pyxam -h for help")
    # Remove the first index of sys.arv as ArgumentParser expects a list of arguments not including the program name
    core.pyxam(pyxamopts.init_arg_parser(sys.argv[1:]))


# Run from shell
if __name__ == '__main__':
    main()