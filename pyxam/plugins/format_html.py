# Author: Eric Buss <ebuss@ualberta.ca> 2016
import options
import formatter
import collections
import filters
import fileutil
import os
import re

signature = 'html format', 'ejrbuss', 'Format for viewing and producing html files'


math = {
    '\\theta':      '&theta;',
    '\\pi':         '&pi;',
    '\\tau':        '&tau;',
    '\\omega':      '&omega;',
    '\\phi':        '&phi;',
    '\\emptyset':   '&phi;',
    '\\int_':       '&int;',
    '\\sum_':       '&sum;',
    '+/-':          '&#177;'
}


def composer_preprocessor(intermediate):
    intermediate.ast = filters.wrap_lists(intermediate.ast)
    intermediate.ast = filters.img64(intermediate.ast)
    intermediate.ast = filters.untab_verb(intermediate.ast)
    return intermediate


def composer_postprocessor(src):
    # Regex replacements
    src = re.sub(r'\\sqrt\{(.*?)\}', r'&radic;\1', src)
    # String replacements
    for symbol in math:
        src = src
    src = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', src)
    src = re.sub(r'\n{2}', '<br />', src)
    if options.state.solutions():
        src = src.replace('display:none', '')
        src = src.replace('display:visible', 'display:none')
    return fileutil.read(
        os.path.dirname(options.state.htmltemplate())
     ).replace('<!-- content -->', src)


def load():
    options.add_option(
        'htmltemplate', '-htt',
        'Specify an HTML template file',
        os.path.abspath(__file__).replace('\\', '/') + '/../templates/exam.html',
        str
    )
    formatter.add_format({
        'extensions': ['html', 'html'],
        'description': signature[1],
        # Assign processors
        'parser_preprocessor': filters.pass_through,
        'parser_postprocessor': filters.pass_through,
        'composer_preprocessor': composer_preprocessor,
        'composer_postprocessor': composer_postprocessor,
        'left_paren': '<div',
        'right_paren': '</div>',
        # Use an OrderedDict to preserve token order
        'format': collections.OrderedDict([
            ('comment', ['<!--', (), '-->', '.']),
            ('questions', ['<div class="questions">', (), '</div>', '.']),
            ('$', ['<span class="latex"> ', (), ' </span>', '.']),
            ('title', ['<div class="title">', (), '</div>', '.']),
            ('solution', ['<div class="solution">', (), '</div>', '.']),
            ('img', ['<img alt="Embedded Image" src="data:image/png;base64,', (), '">', '.']),
            ('choice', ['<div class="choice">', (), '</div>', '.']),
            ('correctchoice', ['<div class="correctchoice">', (), '</div>', '.']),
            ('tolerance', [' tolerance ', (), '.']),
            ('verbatim', ['<pre class="verbatim">', (), '</pre>', '.']),
            ('true', ['<div class=True>True</div>', '.']),
            ('false', ['<div class=False>False</div>', '.']),
            ('h3', ['<h3>', (), '</h3>', '.']),
            ('h2', ['<h2>', (), '</h2>', '.']),
            ('h1', ['<h1>', (), '</h1>', '.']),
            ('list', ['<ul>', (), '</ul>', '.']),
            ('listitem', ['<li>', (), '</li>']),
            ('hr', ['<hr />', '.']),
            ('emphasis3', ['<i><b>', (), '</b></i>', '.']),
            ('emphasis2', ['<br /><b>', (), '</b>', '.']),
            ('emphasis1', ['<i>', (), '</i>', '.']),
            ('verbython', ['<pre class="verb-python">', (), '</pre>', '.']),
            ('verbblock', ['<pre class="verb-block">', (), '</pre>', '.']),
            ('verbexpr', ['<pre class="verb-expr">', (), '</pre>', '.']),
            ('quote', ['<div class="quote">', (), '</div>', '.'])
        ])
    })
    # Return signature
    return signature


def unload():
    pass



