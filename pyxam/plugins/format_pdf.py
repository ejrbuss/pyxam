# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
# Plugin format_pdf

Allows for files to be exported to PDF or DVI. Uses [lib_loader](%/Modules/lib_loader.html) to call `pdflatex` from
the command line and compile LaTeX files. Example usage:
```
$ ./pyxam.py -f pdf my_file.tex
```
"""
import os
import config
import options
import fileutil
import lib_loader
import process_list
import parser_composer


signature = 'PDF support', 'ejrbuss', 'PDF export support'

# Saves the originally specified format
compile_format = ''


def load():
    """
    Adds two dummy formats to the formatter, `pdf` and `dvi`. Hooks `pdf_bypass` to after `post_status` in the
    [process_list](%/Modules/process_list.html) to ensure that arguments from the command line and from the template
    file are both loaded. The bypass function checks to see if either PDF or DVI formats have been requested. Loads the
    following [options](%/Modules/options.html):
     - `recomps -r` The number of LaTeX recompilations

    :return: plugin signature
    """
    parser_composer.add_format(
        name='pdf',
        extensions=['pdf'],
        description='PDF export support',
        format={}
    )
    parser_composer.add_format(
        name='dvi',
        extensions=['dvi'],
        description='DVI export support',
        format={}
    )
    process_list.run_after('post_status', pdf_bypass)
    options.add_option('recomps', '-r', 'The number of LaTeX recompilations',  config.recomps, int)
    return signature


def pdf_bypass():
    """
    Saves the originally specified format and then checks if either the PDF or DVI format have been requested. When
    selected the format is changed to tex and `pdf_compile` hooks to after `export` to compile the final set of tex
    files.
    """
    global compile_format
    compile_format = options.state.format()
    if options.state.format() in ['pdf', 'dvi']:
        options.state.format('tex')
        process_list.run_after('export', pdf_compile)


def pdf_compile():
    """
    Compiles any tex files in the out directory to PDF or DVI depending on what `compile_format` is set to. All
    additional files (aux, log, tex) are removed once compilation completes.
    """
    options.state.cwd(options.state.out())
    options.post('Compiling', len(fileutil.with_extension('.tex')), 'files.')
    for file in fileutil.with_extension('.tex'):
        if compile_format == 'dvi':
            fileutil.write(file, '%&latex\n' + fileutil.read(file))
        try:
            fileutil.remove(file.replace('.tex', '.pdf'))
        except:
            pass
        for i in range(options.state.recomps()):
            lib_loader.pdflatex(file)
    fileutil.remove(fileutil.with_extension(['.aux', '.log', '.tex']))
    options.post('Finished compiling.\n')





