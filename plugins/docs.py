# Author: Eric Buss <ebuss@ualberta.ca> 2016
import process_list
import options
import bang
import pyxam
import fileutil

# TODO cleanup
# TODO automate more of the docs
# TODO README generation
# TODO copy finished file to main directory


template = """
\\documentclass[9pt]{extarticle}
\\usepackage[letterpaper, landscape, margin=.5in]{geometry}
\\usepackage{multicol}
\\usepackage{hyperref}
\\pagestyle{empty}
\\begin{document}
\\centering\\section*{Pyxam Cheat Sheet pyxam!version}
\\begin{multicols}{2}
\\raggedright\\subsection*{Running Pyxam}
Usage pyxam.py [Options] template \\\\
{\\bf Command list:} \\\\
\\begin{tabular}{l l l l}
pyxam!options
\\end{tabular} 

For more details see README.md \\\\
\\subsection*{Pyxam Bang Commands}

\\begin{tabular}{l l}
pyxam!commands
\\end{tabular}
\\subsection*{Examples}
\\begin{description}
    \\item See {\\it examples/template.tex} for a simple exam that implements all of Pyxam's features 
    \\item See {\\it examples/exam.tex} for examples of more complex problems 
    \\item See {\\it examples/github.tex} for an introductory guide to github
    \\item See {\\it README.md} for a general overview of the tools and basic usage 
\\end{description}
\\subsection*{Development Tools}
\\begin{description}
    \\item {\\bf Github} \\\\
        The version control system used for Pyxam. Github allows for easy
        management and access of source code. Github can be found at
        \\url{https://github.com/ and the project page} for Pyxam
        can be found at \\url{https://github.com/balancededge/pyxam}.  
    \\item {\\bf Git-Cola} \\\\
        A GUI client for github on Unix systems. A convenient tool when
        working with a larger number of files in sub directories where the
        command line may be less suitable. Git-Cola can be installed through
        Yast.
    \\item {\\bf PyCharm} \\\\
        A Python IDE with all the bells and whistles. PyCharm makes
        programming Python easy and enjoyable whilst also still being one of the
        most responsive editors available. PyCharm Community edition is free
        and can be found at \\url{https://www.jetbrains.com/pycharm/}.
    \\item {\\bf Dillinger.io} \\\\
        A Markdown browser based editor. Dillinge   r is simple and elegant a
        great solution for writing Markdown documents. Dillinger can be found
        at \\url{http://dillinger.io/}.
    \\item {\\bf Emacs } \\\\
        A powerful and configurable text editor. An ideal environment when
        working in a large variety of programming languages and with a large
        number of file formats. Emacs can be installed through Yast.
\\end{description}
\\subsection*{Emacs Shortlist}
\\begin{tabular}{l l}
M-p & Previous shell command \\\\
C-x-C-v RET & Refresh the currently selected buffer \\\\
C-x-1 & Close all windows except the currently selected one \\\\
C-x-2 & Split window vertically \\\\
C-x-3 & Split window horizontally \\\\
C-x-0 & Close the currently selected window \\\\
C-x-k RET & Kill the currently selected buffer \\\\
\\end{tabular}

\\end{multicols}
\\end{document}
"""

plugin = {
    'name': 'docs',
    'author': 'ejrbuss',
    'description': 'auto generate documentation'
}


def load():
    if options.add_option('cheatsheat', '-cht', 'Generate a new cheatsheet', False, bool):
        process_list.run_before('load_template', cheatsheet)
    if options.add_option('readme', '-rd', 'Generate a new README.md file', False, bool):
        process_list.run_before('load_template', readme)
    return plugin


def cheatsheet():
    global template
    template = template.replace('pyxam!version', pyxam.VERSION)
    template = template.replace('pyxam!commands', '\\\\\n'.join([
        'pyxam! {} & {}'.format(
            name, command.__doc__
        ) for name, command in bang.commands.items()
    ]))
    template = template.replace('pyxam!options', '\\\\\n'.join([
        '{} & {} & {} & {}'.format(
            option.name,
            option.flag,
            '[' + option.name + ']' if option.type_ is not bool else '',
            option.description.replace('\n', '\\\\\n & & & ')
        ) for key, option in options._compiled.items() if key.startswith('--')
    ]))

    fileutil.write('examples/cheatsheet.tex', template)
    options.load_options(['examples/cheatsheet.tex', '-f', 'pdf', '-t', 'cheatsheet'])


def readme():
    exit('README generation not implemented')


def unload():
    # TODO use unload function for copying out files to primary folder
    pass
