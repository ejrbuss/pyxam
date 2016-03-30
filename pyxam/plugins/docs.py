# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin docs

The docs plugin is used to build the documentation for Pyxam quickly and easily from a combination of documentation
source files and python docstrings. All documentation is written in markdown and then converted to HTML by this plugin.
"""
import fileutil
import options
import config
import pyxam
import os
import re

# Docs builder by ejrbuss: Builder for Pyxam's documentation
signature = 'docs builder', 'ejrbuss', 'Builder for Pyxam\'s documentation'

# Navigation javascript
nav = ''
# Table of contents
table = '<ul>'
# Navigation search content
nav_content = '<input type="hidden" id="{}" value="{}">\n'
# Navigation item
nav_item = '<li class="searchable" id="#{}"><a href="{}">{}</a></li>\n'
# Table item
table_item = '<li><a href="{}">{}</a></li>\n'
# Navigation section start
nav_sec_start = '<li class="accordion-toggle"><b><a href="#">{}</a></b><ul class="nav accordion-content">\n'
# Table section start
table_sec_start = '<li><a href="#">{}</a><ul>\n'
# Navigation section end
nav_sec_end = '</ul></li>'
# Table section end
table_sec_end = '</ul></li>'


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
    global url, nav
    options.add_option('docs', '-docs', 'Build Pyxam\'s documentation source', False, bool)
    options.add_option('gitdocs', '-gdocs', 'Generate documentation for use on github', False, bool)
    if options.state.docs() or options.state.gitdocs():
        if options.state.gitdocs():
            url = config.git_docs
        else:
            url = config.local_docs
        # Get paths, use the full path each time in case abspath changes / to \\ on windows
        plugins = os.path.abspath(__file__.replace('docs.py', ''))
        modules = os.path.abspath(__file__.replace('docs.py', '') + '..')
        docs = os.path.abspath(__file__.replace('docs.py', '') + '../../docs/source')
        build = docs.replace('source', 'build')
        load_docs(docs)
        load_source('Modules', modules, build)
        load_source('Plugins', plugins, build)
        # Compile docs
        compile_docs(build)
        # Exit
        exit('Docs successfully recompiled')
    return signature


def load_source(name, directory, build):
    """
    Loads the documentation from a source directory.

    :param name: The name of the navigation section
    :param directory: The directory to load documentation from
    :param build: The build directory
    """
    global nav, table
    nav += nav_sec_start.format(name)
    table += table_sec_start.format(name)
    if not os.path.exists(build + '/' + name):
        os.mkdir(build + '/' + name)
    for file in os.listdir(directory):
        path = directory + '/' + file
        if os.path.isfile(path) and path.endswith('.py') and '__init__' not in path:
            docstrings = re.findall(r'((((def\s+.*?:\s*)?"{3}.*?)"{3})|(\n#[^\n]*\n[^\n]* =))', fileutil.read(path), re.DOTALL)
            parsed = '\n***\n'.join([parse_docstring(doc[0]) for doc in docstrings])
            parsed += '\n***\nView the [source](%/../../pyxam/{})'.format(
                path.replace(os.path.dirname(os.path.dirname(__file__)), '')
            )
            fileutil.write(build + '/' + name + '/' + file.replace('.py', '.md'), parsed)
            id = file.replace('.', '_')
            nav += nav_content.format(id, parsed.replace('"', ''))
            nav += nav_item.format(id, '%/' + name + '/' + file[:-3] + '.html', file[:-3])
            table += table_item.format('%/' + name + '/' + file[:-3] + '.html', file[:-3])
    nav += nav_sec_end
    table += table_sec_end


def parse_docstring(docstring):
    """
    Parses and formats a docstring.

    :param docstring: The docstring to parse
    :return: A documentation ready string
    """
    if re.match(r'\n#[^\n]*\n[^\n]* =', docstring, re.DOTALL):
        docstring = re.sub(r'\n#(.*?)\n(.*?)=', r'**\2**<br />\1', docstring)
        return docstring
    # Remove comment quotes
    docstring = re.sub(r'"{3}', '', docstring)
    # Format function signature
    docstring = re.sub(r'^def\s+(.*?)\((.*?)\):', r'**\1**(*\2*)\n\n', docstring, 1, re.DOTALL)
    # Remove empty parameters
    docstring = re.sub(r'\(\*\*\)\n', '()', docstring)
    # Format param
    docstring = re.sub(r':param\s*(.*?):(.*?)', r'<br />`\1` \2', docstring)
    # Format return
    docstring = re.sub(r':return:(.*?)', r'**<br />returns&nbsp;** \1', docstring)
    # Format single line comments
    lines = docstring.split('\n')
    overwrite = False
    while not overwrite:
        for line in lines:
            overwrite = overwrite or (len(line) < 1 or line[0] != ' ')
        if not overwrite:
            lines = [line[1:] for line in lines]
    return '\n'.join(lines)


def load_docs(docs, name=''):
    """
    Load a documentation file.

    :param docs: The directory to load documentation from
    :param name: The name of the navigation section
    """
    global nav, table
    directories = []
    if not os.path.exists(docs.replace('source', 'build')):
        os.mkdir(docs.replace('source', 'build'))
    for file in os.listdir(docs):
        path = docs + '/' + file
        if os.path.isfile(path) and path.endswith('.md'):
            id = file.replace('.', '_')
            nav += nav_content.format(id, re.sub(r'(")|(<!--.*-->)', '', fileutil.read(path)))
            nav += nav_item.format(id, '%/' + name + '/' + file[:-3] + '.html', file[2:-3]
                                   .replace('_', ' ')
                                   .replace('index', 'Overview'))
            table += table_item.format('%/' + name + '/' + file[:-3] + '.html', file[2:-3]
                                   .replace('_', ' ')
                                   .replace('index', 'Overview'))
            fileutil.write(docs.replace('source', 'build') + '/' + file, fileutil.read(path))
        elif os.path.isdir(path):
            directories.append((file, path))
    for file, path in directories:
        nav += nav_sec_start.format(file)
        table += table_sec_start.format(file)
        load_docs(path, name=file)
        nav += nav_sec_end
        table += table_sec_end


def compile_docs(build):
    """
    Converts all markdown files found in docs to HTML and then copies them to the build directory. All folders are run
    recursively.

    :param docs: The documentation directory to compile
    """
    for file in os.listdir(build):
        path = build + '/' + file
        if os.path.isfile(path) and path.endswith('.md'):
            compile_doc(build, path)
        elif os.path.isdir(path):
            compile_docs(path)


def compile_doc(build, doc):
    """
    Converts the given file from markdown to HTML and then copies it to the build directory.

    :param build: The directory of the file to compile
    :param doc: The file to compile
    """
    pyxam.start([
        '-f', 'html',
        '-o', build,
        '-t', 'doc',
        '-htt', config.template_directory + '/docs.html', doc
    ])
    buffer = fileutil.read(build + '/doc_1.html')
    fileutil.remove(doc)
    fileutil.remove(build + '/doc_1.html')
    fileutil.write(
        doc.replace('.md', '.html'),
        buffer
            .replace('<!-- nav -->', nav)
            .replace('<!-- table -->', table + '</ul>')
            .replace('%/', url + '/')
    )