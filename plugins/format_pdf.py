import os
from subprocess import call
from subprocess import check_output
from process_list import run_before
from options import state
from options import add_option
from formatter import add_format
from fileutil import read
from fileutil import write
from fileutil import remove
from fileutil import with_extension

# TODO move functions to lib_loader
# TODO cleanup
# TODO DVI support


plugin = {
    'name': 'pdf support',
    'author': 'ejrbuss',
    'description': 'pdf export support for LaTeX documents'
}


pdf_compile_flag = False


def load():
    add_option('recomps',     '-r',   'The number of LaTeX recompilations',  1,          int)
    run_before('load_template', pdf_bypass)
    run_before('export', pdf_compile)
    return plugin


def pdf_bypass():
    add_format({
        'name': 'pdf',
        'extensions': ['pdf', 'pdf'],
        'description': plugin['description'],
        'format': {}
    })
    global pdf_compile_flag
    if state.format() == 'pdf':
        pdf_compile_flag = True
        state.format('tex')


def pdf_compile():
    if pdf_compile_flag:
        state.format('pdf')
        for file in with_extension('.cmp'):
            for i in range(state.recomps()):
                try:
                    with open(os.devnull, 'r') as stdin:
                        check_output(['pdflatex', '-shell-escape', file], stdin=stdin)
                    check_compiled(['pdf', 'dvi'], file)
                except:
                    print('Failed to compile latex file: ' + file)
                    print('Running pdflatex in interactive mode...')
                    call(['pdflatex', '-shell-escape', file])
        for file in with_extension('.cmp'):
            remove(file)
        for file in with_extension('.pdf'):
            pre, ext = os.path.splitext(file)
            os.rename(file, pre + '.cmp')
    return


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
        compiled = compiled or path.isfile(name[:-3] + extension)
    if not compiled:
        print('Failed to compile latex file: ' + name)
        print('Running pdflatex in interactive mode...')
        call(['pdflatex', '-shell-escape', name])


def unload():
    pass



