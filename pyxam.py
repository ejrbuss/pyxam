# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports


import sys


# Module Imports


import core
import pyxamopts


# Main


def main():
    """
    Pyxam shell entry point. Makes API call to core.pyxam with command line arguments as parameters.

    :return: None
    """
    if len(sys.argv) == 1: exit("This is Pyxam, enter Pyxam -h for help")
    # Remove the first index of sys.arv as ArgumentParser expects a list of arguments not including the program name
    core.pyxam(pyxamopts.init_arg_parser(sys.argv[1:]))


if __name__ == '__main__': main()