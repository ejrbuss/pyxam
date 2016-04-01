# Author: Eric Buss <ebuss@ualberta.ca> 2016
"""
Plugin format_html

"""
import os
import re
import xml
import options
import filters
import fileutil
import formatter
import collections


# HTML format by ejrbuss: Format for exporting HTML files
signature = 'html format', 'ejrbuss', 'Format for exporting html files'


# Map of LaTeX math symbols to their HTML code counterparts
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
    """
    Performs two modifications to the intermediate.
     - HTML requires listitem tokens be wrapped in a containing element. [filters.wrap_lists](%/Modules/fitlers.html) is
     called to place a list token around all consecutive listitem tokens.
     - Converts images to a base64 encoded string to appear directly in the HTML source.
     - Verbatim blocks have leading whitespaced evenly removed to help formatting in the case where verbatim blocks are
     being read in from formatted source

    :param intermediate: The intermediate to process
    :return: The processed intermediate
    """
    intermediate.ast = filters.wrap_lists(intermediate.ast)
    intermediate.ast = filters.img64(intermediate.ast)
    intermediate.ast = filters.untab_verb(intermediate.ast)
    return intermediate
#TODO finish

def composer_postprocessor(src):
    """
    Performs a number of transformations to the source to create a more comprehensive appearance in html:
     - Converts LaTeX symbols to html codes
     - Convers markdown images [img](url) into `img` tags
     - Converts markdown links [label](url) into `a` tags
     - Converts two consecutive newlines into a `br` tag
     - Converts three consecutive newlines into two `br` tags
    Additionally the provided source is loaded into a template and solutions are made visible if the flag is set.
    :param src: The source to process
    :return: The processed source
    """
    # Regex replacements
    src = re.sub(r'\\sqrt\{(.*?)\}', r'&radic;\1', src)
    # String replacements
    for symbol in math:
        src = src.replace(symbol, math[symbol])
    src = re.sub(r'\[img]\((.*?)\)', r'<img src="\1">', src)
    src = re.sub(r'\[([^\[\]\n]+)\]\(([^()\n]+)\)', r'<a href="\2">\1</a>', src)
    src = re.sub(r'\n{3}', '<br /><br />', src)
    src = re.sub(r'\n{2}', '<br />', src)
    if options.state.solutions():
        src = src.replace('display:none', '')
        src = src.replace('display:visible', 'display:none')
    return fileutil.read(
        options.state.htmltemplate()
     ).replace('<!-- content -->','<div class="content">' + src + '</div>')


def load():
    options.add_option(
        'htmltemplate', '-htt',
        'Specify an HTML template file',
        os.path.abspath(os.path.dirname(__file__) + '/../templates/exam.html'),
        str
    )
    formatter.add_format(
        name='html',
        extensions=['html'],
        description=signature[2],
        composer_preprocessor=composer_preprocessor,
        composer_postprocessor=composer_postprocessor,
        left_paren='<div',
        right_paren='</div>',
        # Use an OrderedDict to preserve token order
        format=collections.OrderedDict([
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
            ('center', ['<div class="center">', (), '</div>', '.']),
            ('emphasis3', ['<i><b>', (), '</b></i>', '.']),
            ('emphasis2', ['<br /><b>', (), '</b>', '.']),
            ('emphasis1', ['<i>', (), '</i>', '.']),
            ('verbython', ['<pre class="verb-python">', (), '</pre>', '.']),
            ('verbblock', ['<pre class="verb-block">', (), '</pre>', '.']),
            ('verbexpr', ['<pre class="verb-expr">', (), '</pre>', '.']),
            ('newline', ['<br />', '.'])
        ])
    )
    # Return signature
    return signature



