#!/usr/bin/env python
# Author: Eric Buss <ejrbuss@ualberta.ca>

"""Exam Generator
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

import sys as _sys
import argparse as _argparse

#
# Main and pyxam
#

def main():
    # if args == 1
    #   print type help
    #   exit
    # args = process_args(pre_process_template(template))
    # args = process_args(sys.args)
    # pyxam( args )
    pyxam( 'somefile.tex' )

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
    buffer = read(template)
    buffer = fill_template(buffer, nsamp)
    buffer = clean_template(buffer, cln)
    buffer = scramble_template(buffer, scram)
    write(buffer, tout, s)
    # for( i : n )
        pweave(tout, f, m, fout)
        replace(tout, v, i)
        tout = rename(tout, name, v, i, s)
        expot(file, f)

#
# Workhorse
#

def process_args(args_list)
    # for item : args_list
    #   if lookup item matches
    #   assign global var

def pre_process_template(template):
    str = tex_match(read(template), 'Parg')
    # create list of arg

def fill_template(buffer, nsamp):
    str = tex_match(buffer, 'Pimport')
    while str != None:
    #   buffer = replace(str, parse_import(str, nsamp)
        str = tex_match(buffer, 'Pimport')
    return buffer

def clean_template(buffer, cln):
    if cln:
        print('TODO')
    return buffer

def scramble_template(buffer, scram):
    if(scram)
        questions = tex_match(buffer, '\question')
        # remove questions from buffer but keep track of slots
        # reinsert in random order
    return buffer

def pweave(tout, f, m, fout):
    # call pweave with repsepctive args
    # translate fout into useable format !moodle

def replace(tout, v, n, students):
    # if v:
    #   replace(tex_match(read(tout), 'Pconst'), n -> alpha )
    # else
    #   replace(tex_match(read(tout), 'Pconst'), n )

def rename(tout, name, v, n, s ):
    # if v:
    #   rename tout to name + s + v -> alpha
    # else
    #   rename tout to name + s + v
    # where s = '' if false and = '_solutions' if true
    # return renamed

def export(file, fmt):
    # if fmt == pdf:
    #   call pdflatex
    # if fmt == hmtl
    #   copy over
    # if fmt == moodle
        print('TODO')

# 
# Utility classes
#

class student:
    def __init__(self, name, number=0):
        self.name = name
        self.number = number

#
# Utility functions
#

def tex_match(buffer, prefix):
    # for character buffer 
    #   if !quote && {} are balanced check prefix
    # return (start_index, end_index + 1)

def read(file):
    # handle io
    # return buffer

def write(file, buffer, s):
    # if s:
    #   write buffer to file twice once for sol and que
    # else
    #   write buffer to file once

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

if __name__ == '__main__':
    main()
