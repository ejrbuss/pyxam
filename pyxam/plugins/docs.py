# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin docs

The docs plugin is used to build local or Github documentation for Pyxam. Documentation is compiled automatically from
a combination of Python source files and markdown docs files into a set of HTML pages. Python docs are treated as
markdown snippets in files and are transformed from markdown to HTML using Pyxam's exam process. Being able to
regenerate the documentation at anytime is useful when changing plugins for instance and you want to be able to look at
a Plugin's documentation.
"""
import os
import re
import pyxam
import config
import options
import fileutil

signature = 'docs builder', 'ejrbuss', 'Builder for Pyxam\'s documentation'

# An HTML string listing all items that should appear in the sidebar of the HTML page
nav = ''
# An HTML string containing links to all items that should appear in the table of contents
table = '<ul>'
# A formattable HTML string for containing all of a page's searcg content
nav_content = '<input type="hidden" id="{}" value="{}">\n'
# A formattable HTML string for adding an item to the navigation list
nav_item = '<li class="searchable" id="#{}"><a href="{}">{}</a></li>\n'
# A formattable HTML string for adding an item to the table of contents
table_item = '<li><a href="{}">{}</a></li>\n'
# A formattable HTML string for adding the start of a subsection to the navigation list
nav_sec_start = '<li class="accordion-toggle"><b><a href="#">{}</a></b><ul class="nav accordion-content">\n'
# A formattable HTML string for adding the start of a subsection to the table of contents
table_sec_start = '<li><a href="#">{}</a><ul>\n'
# An HTML string to denote the end of a subsection in the navigation list
nav_sec_end = '</ul></li>'
# An HTML string to denote the end of a subsection in the table of contents
table_sec_end = '</ul></li>'


def load():
    """
    Loads the following [options](%/Modules/options.html):
     - `gitdocs -gdocs` Builed Pyxam's documentation for use on Github
     - `docs -docs` Build Pyxam's documentation for use locally

    If this option is supplied Pyxam's docs are rebuilt. Docs are built by:
     - Finding the paths to the documentation source, module files, and plugin files
     - Copying all docstrings from module files and plugin files to the documentation build directory
     - Copying all files from the documentation source to documentation build directory
     - Converting all markdown files in the documentation build directory to HTML
    """
    global url, nav
    options.add_option('docs', '-docs', 'Build Pyxam\'s documentation for use locally', False, bool)
    options.add_option('gitdocs', '-gdocs', 'Build Pyxam\'s documentation for use on Github', False, bool)
    if options.state.docs() or options.state.gitdocs():
        if options.state.gitdocs():
            url = config.git_docs
        else:
            url = config.local_docs
        # Get paths, use the full path each time in case abspath changes / to \\ on windows
        plugins = os.path.abspath(__file__.replace('docs.py', ''))
        modules = os.path.abspath(__file__.replace('docs.py', '') + '..')
        docs = os.path.join(os.path.abspath(__file__.replace('docs.py', '')), '..', '..', 'docs', 'source')
        build = os.path.abspath(docs.replace('source', 'build'))
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
    Parses and processes the docstrings from all python files in the given directory and copies them to the given build
    directory. Each file is added as an item to the navigation list and table of contents under a section with the given
    name.

    :param name: The name of the navigation and table of contents section
    :param directory: The directory to load documentation from
    :param build: The build directory
    """
    global nav, table
    nav += nav_sec_start.format(name)
    table += table_sec_start.format(name)
    if not os.path.exists(build + '/' + name):
        os.mkdir(build + '/' + name)
    for file in sorted(os.listdir(directory)):
        path = directory + '/' + file
        if os.path.isfile(path) and path.endswith('.py') and '__init__' not in path:
            docstrings = re.findall(
                r'((((((def)|(class))\s[^\n]*?:\s*)?"{3}.*?)"{3})|(\n#[^\n]*\n[^\n]* =))',
                fileutil.read(path), re.DOTALL
            )
            parsed = '\n***\n'.join([format_docstring(doc[0]) for doc in docstrings])
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


def format_docstring(docstring):
    """
    Formats a docstring.

    :param docstring: The docstring to parse
    :return: A documentation ready string
    """
    if re.match(r'\n#[^\n]*\n[^\n]* =', docstring, re.DOTALL):
        docstring = re.sub(r'\n#(.*?)\n(.*?)=', r'**\2**<br />\1', docstring)
        return docstring
    # Remove comment quotes
    docstring = re.sub(r'"{3}', '', docstring)
    # Remove *args and **kwargs
    docstring = re.sub(r'\*args, \*\*kwargs', 'args, kwargs', docstring)
    # Format function/class signature
    docstring = re.sub(r'^((def)|(class))\s+([^\s]*?)\(([^\n]*?)\):', r'**\4**(*\5*)\n', docstring, 1)
    # Remove empty parameters
    docstring = re.sub(r'\(\*\*\)\n', '()\n', docstring)
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
    Load a documentation file from the folder docs. Files will be copied to the build directory relative to docs. Any
    directories found within the docs directory will be loaded in their own subsection of the navigation and table of
    contents where the name of the section is the name of the directory.

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
        elif os.path.isdir(path) and not file.startswith('.'):
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
    pyxam.pyxam.start([
        '-w',           # Disable weaving
        '-f', 'html',   # Convert to HTML
        '-o', build,    # Output to the build directory
        '-t', 'doc',    # Title the file doc
        '-htt', config.template_directory + '/docs.html', doc   # Use the docs template
    ])
    buffer = fileutil.read(build + '/doc_v1.html')
    fileutil.remove(doc)
    fileutil.remove(build + '/doc_v1.html')
    fileutil.write(
        doc.replace('.md', '.html'),
        buffer
            .replace('<!-- nav -->', nav)
            .replace('<!-- table -->', table + '</ul>')
            .replace('%/', url + '/')
    )