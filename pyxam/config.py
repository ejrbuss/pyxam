"""
# Module config
"""
import os
import filters
import logging

# Directories

# Source directory
pyxam_directory = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
# Plugin directory
plugin_directory = pyxam_directory + '/plugins'
# Library directory
lib_directory = pyxam_directory + '/libs'
# HTML template directory
template_directory = pyxam_directory + '/templates'
# Local docs directory
local_docs = os.path.dirname(pyxam_directory) + '/docs/build'
# Git docs directory
git_docs = 'https://rawgit.com/balancededge/pyxam/master/docs/build'

# Parser

# Default filters run after parsing
default_filters=[
    lambda ast: filters.remove_partial(ast, 'comment'),
    filters.pop_unknowns,
    filters.homogenize_strings,
    filters.transform_questions
]

# CSV

# Strings used to identify columns in a csv files that match a student name
name_column_identifiers = ['firstname', 'surname', 'lastname', 'studentname']
# Strings used to identify columns in a csv files that match a student number
number_column_identifiers = ['studentid', 'id', 'identificationnumber']
# csv file name format
csv_filename = '{n}_{name}_{number}.mix'
# Default string to replace with student name
student_name = '$tudent__name'
# Default string to replace with student number
student_number = '$tudent__number'
# Default string to replace test version
version_number = '$est__version'
# Logging

# Default logging level
default_logging = logging.WARNING
# Logging output format
logging_format='%(levelname)s@%(module)s.%(funcName)s(): %(message)s'

# Options

# Default out directory
out = 'out'
# Default tmp directory
tmp = 'tmp'
# Default figure directory
fig = 'fig'
# Default number of exam versions
number = 1
# Default exam title
title = 'exam'
# Default output format
format = 'tex'
# Default code shell
shell = 'python'
# Default CSV mixing method
method = 'sequence'
# Alphabetize rather than enumerate exams flag
alphabetize = False
# Debug flag
debug = False
# Solutions falg
solutions = False


