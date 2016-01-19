# Author: Eric Buss <ebuss@ualberta.ca> 2016
# Python Imports

import os
import re
import shutil
import subprocess


# Module Imports


import parser
import logger
import fileutil
import templater


# Global Variables


# List of valid export formats
FORMAT_LIST = ['pdf', 'dvi', 'tex', 'html', 'moodle']


# Utility Methods


def switch(options):
    """
    Pre process export files.
    Send off a call to the correct exporter and export files to the OUT directory.

    :param fmt: The export format
    :param interactive: Flag for LaTex to be interactive
    :return: None
    """
    # Pre processing
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            buffer = fileutil.read_temp(name)
            buffer = templater.parse_constant(buffer, 'STUDENT', '')
            buffer = templater.parse_constant(buffer, 'STUDNUM', '')
            fileutil.write_temp(name, buffer)
    # Dispatch
    if options.format == 'dvi':
        logger.log('exporter.switch', 'Exporting to dvi')
        dvi(options)
    elif options.format == 'tex':
        logger.log('exporter.switch', 'Exporting to tex')
        tex()
    elif options.format == 'html':
        logger.log('exporter.switch', 'Exporting to html')
        html()
    elif options.format == 'moodle':
        logger.log('exporter.switch', 'Exporting to moodle')
        moodle()
    elif options.format == 'pdf':
        logger.log('exporter.switch', 'Exporting to pdf')
        pdf(options)
    else:
        # Invalid format
        logger.log('exporter.switch', 'No format provided', logger.LEVEL.WARNING)
        print(' * Warning * No export format provided')
        tex()


def pdf(options):
    """
    Compile LaTeX files to pdf and copy pdf files to OUT directory.

    Exits if a file fails to compile
       *This may be changed in the future as this will leave the TEMP directory, which is useful for debugging but not
        pretty on the eyes

    :param options: Flag for LaTex to be interactive
    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            try:
                if options.interactive:
                    for i in range(options.recompilation):
                        logger.log('exporter.pdf', 'Running pdflatex with interaction enabled')
                        with open(os.devnull, 'r') as stdin:
                            subprocess.call(['pdflatex', '-shell-escape', name], cwd=fileutil.TEMP, stdin=stdin)
                        check_compiled(['pdf', 'dvi'], name)
                else:
                    for i in range(options.recompilation):
                        logger.log('exporter.pdf', 'Running pdflatex silently')
                        with open(os.devnull, 'r') as stdin:
                            subprocess.check_output(['pdflatex', '-shell-escape', name], cwd=fileutil.TEMP, stdin=stdin)
                        check_compiled(['pdf', 'dvi'], name)
                export('.pdf')
                export('.dvi')
            except:
                check_compiled(['pdf', 'dvi'], name)


def dvi(options):
    """
    Compile LaTeX files to dvi and copy dvi files to OUT directory.

    :param options: Flag for LaTex to be interactive
    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            # Write %&latex to start of file to force dvi export
            fileutil.write_temp(name, '%&latex\n' + fileutil.read_temp(name))
    pdf(options)


def tex():
    """
    Copy weaved files to OUT directory.

    :return: None
    """
    export('.tex')
    for name in os.listdir(fileutil.TEMP):
        path = fileutil.TEMP + '/' + name
        if os.path.isdir(path) and len(os.listdir(path)) > 0:
            os.mkdir(fileutil.OUT + '/' + name)
            for figure in os.listdir(path):
                shutil.copy(path + '/' + figure, fileutil.OUT + '/' + name + '/' + figure)


def html():
    """
    Compile LaTeX files to html and copy html files to OUT directory.

    Exits if a file fails to compile
       *This may be changed in the future as this will leave the TEMP directory, which is useful for debugging but not
        pretty on the eyes

    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            try:
                subprocess.call(['ht', 'latex', name], cwd=fileutil.TEMP)
                export('.html')
            except:
                exit('Failed to compile latex file: ' + fileutil.TEMP + '/' + name)


def moodle():
    """
    Overall structure
    question
    multiple choice
    true false
    short anser
    numerical response
    essay
    put question content between $$ ... $$
    :return:
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith('.tex'):
            buffer = '<?xml version="1.0"\n<quiz>\n'
            for question in parser.parse(fileutil.TEMP + '/' + name):
                buffer += question.to_xml()
            buffer += '<\quiz>'
            fileutil.write_temp(name[:-3] + 'xml', buffer)
    export('xml')


def export(extension):
    """
    Move all files with the specified extension from TEMP to OUT.

    :param extension: Files with this extension will be moved
    :return: None
    """
    for name in os.listdir(fileutil.TEMP):
        if os.path.isfile(fileutil.TEMP + '/' + name) and name.endswith(extension):
            fileutil.copy_out(name)


def check_compiled(extensions, name):
    """
    Check that a file with name compiled to one of the specified extensions. If the file does not compile
    lacheck is is run on the original file.

    :param extensions: The extensions to look for
    :param name: The name of the original file
    :return: None
    """
    compiled = False
    for extension in extensions:
        compiled = compiled or os.path.isfile(fileutil.TEMP + '/' + name[:-3] + extension)
    if not compiled:
        print('Failed to compile latex file: ' + fileutil.TEMP + '/' + name)
        print('Running pdflatex in interactive mode...')
        subprocess.call(['pdflatex', '-shell-escape', name], cwd=fileutil.TEMP)