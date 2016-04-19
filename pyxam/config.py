# Author: Eric Buss <ebuss@ualberta.ca> 2016
import os
import filters
import logging
import collections

"""
# Module config

This module can be used to set various configuration settings for running Pyxam.

## Directories

The following configuration options allow you to set the paths to the different components of the Pyxam system.

The pyxam_directory should point to the source directory. By default that will be the parent directory of this file.
"""
pyxam_directory = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
"""
The plugin directory should point to the plugins folder. By default this will be located in a directory named plugins in
the source directory.
"""
plugin_directory = pyxam_directory + '/plugins'
"""
The template_directory should point to a folder containing template HTML files used for exporting to HTML. By default
this will be located in a directory named templates in the source directory.
"""
template_directory = pyxam_directory + '/templates'
"""
The local_docs should point to the build directory for your local documentation. By default this will be located in the
docs/build directory one level up from the source directory.
"""
local_docs = os.path.dirname(pyxam_directory) + '/docs/build'
"""
The git_docs should point to the rawgit url for viewing documentation. By default this should be
https://rawgit.com/username_of_repo_owner/repo/branch/docs/build
"""
git_docs = 'https://rawgit.com/balancededge/pyxam/master/docs/build'
"""
## Formatter

The following configuration options relate to parsing and formatting.

The default_filters should be a list of functions to apply to a parsed ast prior to parser post processing. By default:
 - Comments are removed
 - Unknowns are popped (unknowns are replaced with their first recognized child)
 - Consecutive strings are homogenized (combined)
 - Question types are transformed (ex. multichoice to multiselect)
 - The builtins pyxamnumerical and pyxamcalcualted are removed
"""
default_filters=[
    lambda ast: filters.remove_name(ast, 'comment'),
    filters.pop_unknowns,
    filters.homogenize_strings,
    filters.transform_questions,
    lambda ast: filters.remove_name(ast, 'pyxamnumerical'),
    lambda ast: filters.remove_name(ast, 'pyxamcalculated')
]
"""
## Formatting

The following configuration options relate to formatting of various auto-generated strings.

The filename is the postfix format for exported files. This will appear after the title of the exam followed by an
underscore. The exam version, student name, and student number can all be specified.
"""
filename = 'v{version}_{name}_{number}'
"""
The numerical_format defines the default format of numerical answers. The solution, tolerance (as an absolute value) and
upper and lower bounds can all be specified.
"""
numerical_format = '{solution} with a tolerance of {tolerance}({upper}-{lower})'
"""
The numerical_format_no_tolerance defines the format of numerical answers when the tolerance is zero.
"""
numerical_format_no_tolerance = '{solution}'
"""
The calculated_format defines the default format of calculated answers. The solution, tolerance (as an absolute value)
and upper and lower bounds can all be specified.
"""
calculated_format = '{solution} with a tolerance of {tolerance}({upper}-{lower})'
"""
The calculated_format_no_tolerance defines the format of calclated answers when the tolerance is zero.
"""
calculated_format_no_tolerance = '{solution}'
"""
## CSV

The following configuration options relate to reading in CSV files.


Strings used to identify columns in a csv files that match a student name
"""
first_name_column_identifiers = ['firstname']
"""
"""
last_name_column_identifiers = ['lastname', 'surname']
"""
"""
name_column_identifiers = ['studentname', 'name']
"""
Strings used to identify columns in a csv files that match a student number
"""
number_column_identifiers = ['studentid', 'id', 'identificationnumber']
"""
"""
placeholder = collections.defaultdict(lambda: '')
placeholder['tex'] = '\hrulefill'
placeholder['pdf'] = '\hrulefill'
"""
## Logging

The following configuration options relate to logging.

The default_logging defines the default logging level.
"""
default_logging = logging.WARNING
"""
The logging_format defines the default format for logging messages.
"""
logging_format='%(levelname)s@%(module)s.%(funcName)s(): %(message)s'
"""
## Options

The following configuration options relate to command line options

The default out directory.
"""
out = 'out'
"""
The default tmp directory.
"""
tmp = 'tmp'
"""
The default figure directory.
"""
fig = 'fig'
"""
The default number of exam versions.
"""
number = 1
"""
The default exam title.
"""
title = 'exam'
"""
The default output format.
"""
format = 'tex'
"""
The default shell to run python through.
"""
shell = 'python'
"""
The default CSV mixing method.
"""
method = 'sequence'
"""
Set whether exams are numerated or alphabetized.
"""
alphabetize = False
"""
Set whether pweave is disabled by default.
"""
noweave = False
"""
Set whether debug mode is disabled by default.
"""
debug = False
"""
Set whether solutiosn are enabled by default.
"""
solutions = False
"""
Set the default number of LaTeX recompilations.
"""
recomps = 1
"""
Set the default random seed.
"""
seed = 0 # random.randint()

