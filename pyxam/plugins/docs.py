# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin docs

The docs plugin is used to build the documentation for Pyxam quickly and easily from a combination of documentation
source files and python docstrings. All documentation is written in markdown and then converted to HTML by this plugin.
"""
import fileutil
import options
import shutil
import os
import re


signature = 'docs builder', 'ejrbuss', 'Builder for Pyxam\'s documentation'


def load():
    """
    Loads the doc plugin.

    **localdocs** `-ld`, `-localdocs`, `--localdocs` *(bool) False*

    This flag determines whether documentation pages will link to repo pages or to files on your local computer.

    **docs** `-docs`, `--docs` *(bool) False*

    If this option is supplied Pyxam's docs are rebuilt. Docs are built by:
     - Finding the paths to the documentation source, module files, and plugin files
     - Copying all docstrings from module files and plugin files to the documentation source directory
     - Converting all markdown files in the documentation source directory to HTML
     - Perform post processing to add a javascript search bar and sidebar along with minor changes to HTML
     - Copying those files to the documentation build directory
    It can be useful to regenerate the docs if you have added a new Plugin and want to read its documentation.
    """
    options.add_option('localdocs', '-ld', 'Generate documentation for local use', False, bool)
    if options.add_option('docs', '-docs', 'Build Pyxam\'s documentation source', False, bool):
        # Get paths, use the full path each time in case abspath changes / to \\ on windows
        plugins = os.path.abspath(__file__.replace('docs.py', ''))
        modules = os.path.abspath(__file__.replace('docs.py', '') + '..')
        docs = os.path.abspath(__file__.replace('docs.py', '') + '../../docs/source')
        # Copy Plugin docstrings
        get_docs(docs + '/Plugins', plugins)
        # Copy Module docstrings
        get_docs(docs + '/Modules', modules)
        # Compile docs
        compile_docs(docs)
        # Exit
        exit('Docs successfully recompiled')
    return signature


def get_docs(docs, directory):
    """
    Copies all python docstrings from directory to docs.

    :param docs: The directory where the docstrings will be copied to
    :param directory: The directory whose python files while be scraped for docstrings
    """
    # TODO tabbing
    # TODO markdown to html
    # TODO javascript and css wrapper
    for file in os.listdir(directory):
        path = directory + '/' + file
        # If file is python file other than __init__
        if os.path.isfile(path) and path.endswith('.py') and file != '__init__.py':
            buffer = fileutil.read(path)
            # Get docstrings
            docstrings = re.findall(r'(((def[^\n]*:\s*)?"{3}.*?)"{3})', buffer, re.DOTALL)
            # remove triple quotes
            docstrings = [re.sub(r'"{3}', '', doc[0]) for doc in docstrings]
            # Transform function headers
            docstrings = [re.sub(r'def (.*?)\((.*?)\):', r'**\1**(*\2*)\n', doc) for doc in docstrings]
            # Convert list to buffer
            buffer = '\n***\n'.join(docstrings)
            # Reformat *Kills sub lists TODO better parsing
            buffer = re.sub(r'\n {4}', '\n', buffer)
            # Remove any empty paramters
            buffer = buffer.replace('(**)\n', '()')
            # Convert parameter definitions
            buffer = re.sub(r':param\s*(.*?):(.*?)', r'\n\n`\1` \2', buffer)
            # Convert return statements
            buffer = re.sub(r':return:(.*?)', r'\n\n**returns** \1', buffer)
            # Write to docs
            fileutil.write(docs + '/' + file.replace('.py', '.md'), buffer)


def compile_docs(docs):
    """
    Converts all markdown files found in docs to HTML and then copies them to the build directory. All folders are run
    recursively.

    :param docs: The documentation directory to compile
    :return: test
    """
    if not os.path.exists(docs.replace('source', 'build')):
        os.mkdir(docs.replace('source', 'build'))
    for file in os.listdir(docs):
        path = docs + '/' + file
        if os.path.isfile(path) and path.endswith('.md'):
            compile_doc(path)
        elif os.path.isdir(path):
            compile_docs(path)


def compile_doc(doc):
    """
    Converts the given file from markdown to HTML and then copies it to the build directory.

    :param doc: The file to compile
    """
    if not os.path.exists(doc.replace('source', 'build')):
        open(doc.replace('source', 'build'), 'w').close()
    shutil.copy(doc, doc.replace('source', 'build'))