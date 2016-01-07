#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca>

"""
Exam Generator
Template File Syntax
********************

<<>>
Runnable code block
@

\Parg{}
    Specify any ommand line argument in the Template file

\Pexpr{ runnable code block }

\Pconst{ variable }
    VERSION either numerical or letter version
    STUDENT student name
    SNUMBER student number

\Pimport{ file }
    FILENAME [rep=1] will copy in rep number of the file provided
    DIR [rep=nsamp] [-r] will copy in rep number of random
        questions from the directory. If the repeat flag is set
        the questions will be allowed to repeat.
    FILENAME|FILENAME|... [rep=1] [-r] will copy in rep number of
        random question from the given list
    
"""



__version__= '1.0.0'

#
# Imports
#

import os as _os
import re as _re
import sys as _sys
import argparse as _argparse
import shutil as _shutil

#
# Constants
#

CONST_SOLUTION_POSTFIX = '_solution'

#
# Global vars
#

TMP_DIR = []

#
# Main and pyxam
#

def main():
    # if args == 1
    #   print type help
    #   exit
    # check_dependencies()
    # args = process_args(pre_process_template(template))
    # args = process_args(sys.args)
    # pyxam( args )
    # pyxam( 'somefile.tex' )
    print('TODO main')

def pyxam(template,         # Template file
            s=True,         # Solutions flag
            n=1,            # Number of exams
            v=True,         # Flag for numbered or lettered exams
            nsamp=1,        # Default number of question samples
            scram=False,    # Scramble flag
            out='',         # Ouput directory
            tout='',        # Temporary directory
            fout='figures', # Figures directory
            name='exam',    # Name of exam
            f='pdf',        # Output format
            m=True,         # Use matplotlib flag
            cln=True,       # Perform cleanup on imported questions
            students=None   # A list of students
           ):
    # buffer = read(template)
    # buffer = fill_template(buffer, nsamp)
    # buffer = clean_template(buffer, cln)
    # buffer = scramble_template(buffer, scram)
    # write(buffer, tout, s)
    # for( i : n )
    #    pweave(tout, f, m, fout)
    #    replace(tout, v, i)
    #    tout = rename(tout, name, v, i, s)
    #    expot(file, f)
    print('TODO pyxam')

#
# Workhorse
#

def check_dependencies():
    # check python version needs python3
    # check for tex 
    # check for pdflatex
    # check for pweave
    # check for matplotlib
    print('TODO check_dependencies')

def process_args(args_list):
    # for item : args_list
    #   if lookup item matches
    #   assign global var
    print('TODO process_args')

def pre_process_template(template):
    # str = tex_match(read(template), 'Parg')
    # create list of arg
    print('TODO pre_process_template')

def fill_template(buffer, nsamp):
    # str = tex_match(buffer, 'Pimport')
    # while str != None:
    #   buffer = replace(str, parse_import(str, nsamp)
    #    str = tex_match(buffer, 'Pimport')
    # return buffer
    print('TODO fill_template')

def clean_template(buffer, cln):
    # if cln:
    #    print('TODO')
    # return buffer
    print('TODO clean_template')

def scramble_template(buffer, scram):
    # if(scram)
    #    questions = tex_match(buffer, '\question')
        # remove questions from buffer but keep track of slots
        # reinsert in random order
    # return buffer
    print('TODO scramble_template')

def pweave(tout, f, m, fout):
    # call pweave with repsepctive args
    # translate fout into useable format !moodle
    print('TODO pweave')

def replace(tout, v, n, students):
    # if v:
    #   replace(tex_match(read(tout), 'Pconst'), n -> alpha )
    # else
    #   replace(tex_match(read(tout), 'Pconst'), n )
    print('TODO replace')

def rename(tout, name, v, n, s ):
    # if v:
    #   rename tout to name + s + v -> alpha
    # else
    #   rename tout to name + s + v
    # where s = '' if false and = '_solutions' if true
    # return renamed
    print('TODO rename')

def export(file, fmt):
    # if fmt == pdf:
    #   call pdflatex
    # if fmt == hmtl
    #   copy over
    # if fmt == moodle
    print('TODO export')

#
# Utility methods
#

def tex_match(buffer, prefix, m=False):
    """
    Returns a list of tuples which indicate the starting and ending
    indeces for arguments that are contained in the latex formatted
    command prefix.

    Arguments:
        - buffer -- The String to search
        - prefix -- The prefix command to match
        - m -- if True will return the full match, if false
            this will return only the command arguments

    Example:
    tex_match(r'\command{some argument}', 'command')
    will return

    Regex Used:
    (?:[^\\]|^)(?:\\\\)*\\prefix{(([^{}]*({[^{}]*})*[^{}}]*)*)}
    (?:[^\\]|^) Requires not backslash or start of string
    (?:\\\\)*   Requires even number of backslashes
    (\\prefix{) Requires command syntax
    [^{}]       Requires non curly parens
    [{[^{}]*}]  Allows for dictionaries in Pexpr{}

    This will still have conflicts with Strings in Pexpr, but should
    parse all other commands fine.
    """
    args = []
    matches = [(m.start(), m.end()) for m in
        _re.finditer(r'(?:[^\\]|^)(?:\\\\)*\\' + prefix +
                     r'{(([^{}]*({[^{}]*})*[^{}}]*)*)}', buffer)]
    if m:
        return matches
    for pair in matches:
        m = _re.search('{', buffer[pair[0]:])
        args.append((pair[0] + m.start() + 1, pair[1] - 1))
    return args

def read(file):
    """
    Opens and reads file as a String. Returns String
    with newlines intact.

    Will throw a FileNotFoundError if the file does not exist
    Will throw a IsADirectoryError if the file is a directory
    """
    with open(file, 'r') as reader:
        buffer = reader.read()
    return buffer

def write(file, buffer, s=False):
    """
    Writes a buffer to a directory (file) with the filename (name).
    If the s flag is set than a second file will be written with
    the \printanswers command added and CONST_SOLUTION_POSTFIX 
    appended to the filename
    """
    with open(file + '.tex', 'w') as writer:
        writer.write(buffer)
    if s:
        with open(file + CONST_SOLUTION_POSTFIX + '.tex', 'w') as writer:
            writer.write('\\printanswers\n' + buffer)

def remove_file(file):
    """
    Attempts to remove a file (file).
    
    Will throw a FileNotFoundError if the file does not exist
    Will throw a IsADirecotryError if the file is a directory
    """
    _os.remove(file)

def remove_dir(file):
    """
    Attempts to remove a directory (file). 

    Will throw a FileNotFoundError if the file does not exist
    Will throw a NotADirectoryError if the fill is not a directory
    """
    _shutil.rmtree(file)

def create_tmp_dir(file):
    """
    Create a temporary directory (file). Adds directory to a list
    of temporary directories to be deleted when remove_tmp_dir is
    called
    """
    TMP_DIR.append(file)
    if not _os.path.exists(file):
        _os.makedirs(file)

def remove_tmp_dir():
    """
    Removes all temporary directories created via create_tmp_dir.
    This will also delete all files contained by those directories
    """
    for file in TMP_DIR:
        remove_dir(file)

def parse_import(str, nsamp):
    # check if file or directory
    # if file
    #   check for rep or assign 1
    #   return rep copies of file
    # if file|file
    #   check for rep or assign 1
    #   check for repeat
    #   return rep copies of file check for repeats
    # if dir
    #   check for rep or asisgn nsamp
    #   check for repeat
    #   return rep copies of selected files check for repeats
    print('TODO parse_import')

if __name__ == '__main__':
    main()
