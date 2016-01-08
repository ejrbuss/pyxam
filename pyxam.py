#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca>

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

    NAME the base name of the exam

\Pimport{ file }
    cmd_args.template = cmd_args.template()
    FILENAME [rep=1] will copy in rep number of the file
    provided

    DIR [rep=nsamp] [-r] will copy in rep number of random
        questions from the directory. If the repeat flag is
        set the questions will be allowed to repeat.

    FILENAME|FILENAME|... [rep=1] [-r] will copy in rep
        number of random question from the given list

"""



__version__= '1.0.0'

#
# Imports
#

import os as _os
import re as _re
import sys as _sys
import shutil as _shutil
import argparse as _argparse
import subprocess as _subprocess

try:
    import matplotlib as _matplotlib
except:
    print('matplotlib is not installed. Please install to continue.')
    exit()

import export_tex as _export_tex
import export_pdf as _export_pdf
import export_html as _export_html
import export_moodle as _export_moodle

#
# Global vars
#

TMP_DIR = []

class default:
    template = ''
    solutions = False
    number = 1
    lettered = False
    sample = 1
    scramble = False
    out = 'out'
    temp = 'pyxam_tmp'
    figure = 'figures'
    name = 'exam'
    format = 'pdf'
    shell = 'python'
    matplotlib = False
    clean = False
    students = None

#
# Main and pyxam
#

def pyxam(args):
    required = check_dependencies(['tex', 'pdflatex', 'pweave'])
    if required != None:
        print(required, ' could not be found. Please install to continue.')
        exit()
    if len(_sys.argv) == 1:
        print("This is Pyxam, enter Pyxam -h for help")
        exit()
    parser = _argparse.ArgumentParser(prog='Pyxam', usage='Pyxam [options] template')
    parser.add_argument('template', nargs=1, 
                        help="""Template file location""")
    parser.add_argument('-s', '--solutions', action='store_true', default=None, 
                        help="""Produce a copy of solutions for each exam
                        created""")
    parser.add_argument('-n', '--number', type=int, nargs='?', 
                        help='The number of exams to create')
    parser.add_argument('-l', '--lettered', action='store_true', default=None,  
                        help="""Have exam files labelled by letter rather
                        than number""")
    parser.add_argument('-S', '--sample', type=int, nargs='?', 
                        help="""The default number of questions that will be
                        sampled when selecting questions from a directory""")
    parser.add_argument('-c', '--scramble', action='store_true', default=None,  
                        help="""Scramble the order of questions""")
    parser.add_argument('-o', '--out', nargs='?', 
                        help="""The output directory""")
    parser.add_argument('-t', '--temp', nargs='?', 
                        help="""The temporary directory used while creating
                        exam(s)""")
    parser.add_argument('-F', '--figure', nargs='?', 
                        help=("""The name of the directory created to store any
                        figures needed for the exam"""))
    parser.add_argument('-nm', '--name', nargs='?', 
                        help="""The base name for the exam""")
    parser.add_argument('-f', '--format', nargs='?',
                        help="""The format of the output file. Either pdf, html, 
                        or moodle""")
    parser.add_argument('-sh', '--shell', nargs='?',
                        help=""""The shell to run code through: python, epython
                        ipython, matlab, octave, or julia""")
    parser.add_argument('-m', '--matplotlib', action='store_true', default=None, 
                        help="""Disable matplotlib when using pweave""")
    parser.add_argument('-C', '--clean', action='store_true', default=None, 
                        help="""Disable cleanup of messy question tags""")
    parser.add_argument('-st', '--students', nargs='?',
                        help="""CSV file with student names """)
    # Build cmd args and template args
    if _sys.argv == args:
        cmd_args = parser.parse_args()
    else:
        cmd_args = parser.parese(args)
    buffer, tmp_args = pre_process_template(cmd_args.template)
    tmp_args = parser.parse_args(tmp_args)
    # Process args
    process_args(cmd_args, tmp_args)
    # Process
    create_tmp_dir(cmd_args.temp)
    # buffer = fill_template(buffer, cmd_args.sample)
    # buffer = scramble_template(buffer, cmd_args.scramble)
    write(cmd_args.temp + '/' + cmd_args.name, buffer)
    for n in range(cmd_args.number):
        name = cmd_args.temp + '/' + cmd_args.name + str(chr(n + ord('A')) 
                   if cmd_args.lettered else n)
        write(name, buffer)
        pweave(name, cmd_args.matplotlib, cmd_args.figure, cmd_args.shell)
    for file in _os.listdir(cmd_args.temp) :
        if file.endswith('.tex'):
            # replace(file,s, v, i)
            export(file, cmd_args.format, cmd_args.temp, cmd_args.out)
    if _os.listdir(cmd_args.figure) == []:
        remove_dir(cmd_args.figure)
    remove_tmp_dir()

#
# Workhorse
#

def check_dependencies(required):
    """
    Checks list of process names (required) as callable. The
    first process that cannot be called is returned.
    """
    for process in required:
        try:
            _subprocess.check_output([process, '--version'])
        except OSError:
            return process

def pre_process_template(template):
    """Checks template for the \Parg{} command. Collects all
    instances and returns a buffer with those instances
    removed along with a String of all arguments from
    \Parg{}. Takes the file to read as template (template)
    
    Will print an error message and exit if template does
    not exist
    """
    try:
        buffer = read(template)
        matches = tex_match(buffer, 'Parg', True)[::-1]
        pairs = tex_match(buffer, 'Parg')
        args = ''
        for pair in pairs:
            args = args + buffer[pair[0]:pair[1]] + ' '
            for pair in matches:
                buffer = buffer[:pair[0]] + buffer[pair[1]:]
                return buffer, args.split()
        return buffer, None
    except FileNotFoundError:
        print('Could not find template file.')
        exit()

def process_args(cmd, tmp):
    """
    Builds a complete arg list from the command line 
    arguments, any arguments specified by the template and
    the default arguments.

    Command line arguments are preffered over template 
    arguments which are preffered over default arguments.
    """
    cmd.template = sanitize(cmd.template)
    cmd.solutions = process_arg(cmd.solutions, tmp.solutions, default.solutions)
    cmd.number = process_arg(cmd.number, tmp.number, default.number)
    cmd.lettered = process_arg(cmd.lettered, tmp.lettered, default.lettered)
    cmd.sample = process_arg(cmd.sample, tmp.sample, default.sample)
    cmd.scramble = process_arg(cmd.scramble, tmp.scramble, default.scramble)
    cmd.out = process_arg(cmd.out, tmp.out, default.out)
    cmd.temp = process_arg(cmd.temp, tmp.temp, default.temp)
    cmd.figure = process_arg(cmd.figure, tmp.figure, default.figure)
    cmd.name = process_arg(cmd.name, tmp.name, default.name)
    cmd.format = process_arg(cmd.format, tmp.format, default.format)
    cmd.shell = process_arg(cmd.shell, tmp.shell, default.shell)
    cmd.matplotlib = process_arg(cmd.matplotlib, tmp.matplotlib, default.matplotlib)
    cmd.clean = process_arg(cmd.clean, tmp.clean, default.clean)
    cmd.students = process_arg(cmd.students, tmp.students, default.students)

def process_arg(cmd, tmp, default):
    """
    Returns the final arg from an option between a command
    line argument, template argument, and default argument.

    Command line arguments are preffered over template 
    arguments which are preffered over default arguments.
    """
    if cmd is not None:
        return cmd
    elif tmp is not None:
        return tmp
    else:
        return default

def fill_template(buffer, nsamp):
    # str = tex_match(buffer, 'Pimport')
    # while str != None:
    #   buffer = replace(str, parse_import(str, nsamp)
    #    str = tex_match(buffer, 'Pimport')
    # return buffer
    print('TODO fill_template')

def scramble_template(buffer, scram):
    # if(scram)
    #    questions = tex_match(buffer, '\question')
        # remove questions from buffer but keep track of slots
        # reinsert in random order
    # return buffer
    print('TODO scramble_template')

def clean_template(buffer, cln):
    # if cln:
    #    print('TODO')
    # return buffer
    print('TODO clean_template')

def pweave(file, matplotlib, figure, shell):
    """
    Call pweave with command line options on file (file). Options
    include disabling matplotlib (matplotlib), the figure directory
    (figure) and the shell used for parsing code (shell).
    """
    args = ['pweave', file, '-f', 'tex', '-F', figure]
    if matplotlib:
        args.append( '-m' )
    out = _subprocess.call(args)

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

def export(file, fmt,temp, out):
    if not _os.path.exists(out):
        _os.makedirs(out)
    if fmt == 'pdf':
        _export_pdf.export(file, temp, out)
    # if fmt == pdf:
    #   call pdflatex# call pweave with repsepctive args
    # translate fout into useable format !moodle
    # if fmt == hmtl
    #   copy over
    # if fmt == moodle

#
# Utility methods
#

def sanitize(buffer):
    """
    Sanitize to string. Turns the argument into a valid 
    filename string.
    """
    if isinstance(buffer, str):
        return buffer
    try:
        return str(buffer[0])
    except:
        return str(buffer)

def tex_match(buffer, prefix, m=False):
    """Returns a list of tuples which indicate the starting and
    ending indeces for arguments that are contained in the
    latex formatted command prefix.

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

    This will still have conflicts with Strings in Pexpr,
    but should parse all other commands fine.

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
    Opens and reads file as a String. Returns String with
    newlines intact.

    Will throw a FileNotFoundError if the file does not
    exist Will throw a IsADirectoryError if the file is a
    directory

    """
    print('Reading from ', file)
    with open(_os.path.abspath(sanitize(file)).replace('\\ ', ' '), 'r') as reader:
        buffer = reader.read()
    return buffer

def write(file, buffer):
    """
    Writes a buffer to a directory (file) with the filename
    (name).  If the s flag is set than a second file will be
    written with the \printanswers command added and
    CONST_SOLUTION_POSTFIX appended to the filename
    """
    print('Writing to ', file)
    with open(_os.path.abspath(sanitize(file)), 'w') as writer:
        writer.write(buffer)

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
    Create a temporary directory (file). Adds directory to a
    list of temporary directories to be deleted when
    remove_tmp_dir is called
    """
    print('Creating tmp directory: ', file)
    TMP_DIR.append(file)
    if not _os.path.exists(file):
        _os.makedirs(file)

def remove_tmp_dir():
    """
    Removes all temporary directories created via
    create_tmp_dir.  This will also delete all files
    contained by those directories
    """
    print('Removing tmp dirs: ', TMP_DIR)
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
    pyxam(_sys.argv)
